"""Shared model configuration and safe, actionable connection diagnostics."""

from dataclasses import dataclass, field
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


@dataclass(frozen=True)
class ModelConfig:
    api_key: str = field(repr=False)
    model: str = "gpt-4.1-mini"
    base_url: str = "https://api.openai.com/v1"


@dataclass(frozen=True)
class ModelResult:
    text: str | None = None
    code: str = "ready"
    message: str = "The model is configured; no request has been tested yet."

    def status(self):
        return {"code": self.code, "message": self.message}


def _get(mapping, key, default=None):
    try:
        return mapping.get(key, default) if mapping is not None else default
    except Exception:
        # st.secrets can raise when the file/store is missing or malformed.
        return default


def _first(*values):
    return next((value.strip() for value in values
                 if isinstance(value, str) and value.strip()), "")


def load_model_config(secrets=None, environ=None):
    env = os.environ if environ is None else environ
    section = next((_get(secrets, name) for name in ("openai", "OpenAI", "OPENAI")
                    if _get(secrets, name) is not None), {})

    def setting(names, nested, default=""):
        return _first(*[_get(secrets, name) for name in names],
                      *[_get(section, name) for name in nested],
                      *[_get(env, name) for name in names], default)

    return ModelConfig(
        api_key=setting(("OPENAI_API_KEY", "openai_api_key", "API_KEY", "api_key"),
                        ("api_key", "OPENAI_API_KEY", "openai_api_key")),
        model=setting(("OPENAI_MODEL", "openai_model"), ("model", "OPENAI_MODEL"),
                      "gpt-4.1-mini"),
        base_url=setting(("OPENAI_BASE_URL", "openai_base_url"),
                         ("base_url", "OPENAI_BASE_URL"), "https://api.openai.com/v1"),
    )


def configuration_status(config):
    if not config.api_key:
        return ModelResult(code="missing_api_key", message=(
            "No API key was found in the app configuration. The app owner should "
            "set OPENAI_API_KEY in Streamlit app Settings > Secrets and save it."
        ))
    try:
        parsed = urllib.parse.urlsplit(config.base_url)
    except ValueError:
        return ModelResult(code="invalid_configuration", message=(
            "OPENAI_BASE_URL is malformed. The app owner should correct it in Secrets."
        ))
    if (parsed.scheme not in {"https", "http"} or not parsed.hostname
            or parsed.username or parsed.password or parsed.query or parsed.fragment):
        return ModelResult(code="invalid_configuration", message=(
            "OPENAI_BASE_URL is not a valid API base URL. Use a URL without "
            "embedded credentials or query parameters."
        ))
    if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        return ModelResult(code="invalid_configuration", message=(
            "The model endpoint must use HTTPS, except for a local development server."
        ))
    if any(character in config.api_key for character in "\r\n"):
        return ModelResult(code="invalid_configuration", message=(
            "The configured API key contains a line break. The app owner should "
            "correct the key value in Streamlit Secrets."
        ))
    return ModelResult()


def _endpoint(base_url):
    url = base_url.rstrip("/")
    if url.endswith("/chat/completions"):
        return url
    if not urllib.parse.urlsplit(url).path:
        url += "/v1"
    return url + "/chat/completions"


def _http_failure(status, code):
    if status == 401:
        return ModelResult(code="authentication_failed", message=(
            "The model service rejected the configured API key (HTTP 401). "
            "The app owner should check that the key is active and belongs to "
            "the provider configured in OPENAI_BASE_URL."
        ))
    if status == 403:
        return ModelResult(code="permission_denied", message=(
            "The model service denied access (HTTP 403). The app owner should "
            "check the API project's permissions and access to OPENAI_MODEL."
        ))
    if code in {"insufficient_quota", "billing_hard_limit_reached", "billing_not_active"}:
        return ModelResult(code="quota_exhausted", message=(
            "The model API's quota or billing limit has been reached. The app "
            "owner should check the API project's billing and usage limits."
        ))
    if status == 429:
        return ModelResult(code="rate_limited", message=(
            "The model service is temporarily rate-limiting requests (HTTP 429). "
            "Wait briefly and try again."
        ))
    if status == 404 or code == "model_not_found":
        return ModelResult(code="model_or_endpoint_not_found", message=(
            "The configured model or API endpoint was not found. The app owner "
            "should check OPENAI_MODEL, OPENAI_BASE_URL and model access."
        ))
    if status >= 500:
        return ModelResult(code="provider_unavailable", message=(
            "The model service is temporarily unavailable. Please try again shortly."
        ))
    return ModelResult(code="request_rejected", message=(
        f"The model service rejected the request (HTTP {status}). The app owner "
        "should check that OPENAI_MODEL supports the configured Chat Completions endpoint."
    ))


def request_completion(messages, config, opener=None, sleep=None):
    """Return generated text or a safe diagnosis; never expose raw provider errors."""
    status = configuration_status(config)
    if status.code != "ready":
        return status
    open_request = urllib.request.urlopen if opener is None else opener
    pause = time.sleep if sleep is None else sleep
    payload = {"model": config.model, "messages": messages, "max_completion_tokens": 2500}
    transient_retries = 0
    token_compatibility_retry = False
    for _ in range(3):
        request = urllib.request.Request(
            _endpoint(config.base_url), data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {config.api_key}",
                     "Content-Type": "application/json"}, method="POST",
        )
        try:
            with open_request(request, timeout=45) as response:
                body = json.loads(response.read().decode("utf-8"))
            text = body["choices"][0]["message"]["content"]
            if not isinstance(text, str) or not text.strip():
                return ModelResult(code="empty_response", message=(
                    "The model returned no usable answer. Try again; if this "
                    "continues, the app owner should review the model configuration."
                ))
            return ModelResult(text=text.strip(), code="connected",
                               message="The last model request completed successfully.")
        except urllib.error.HTTPError as exc:
            # Read only enough to classify a failure. Never show provider text,
            # headers, URLs or exceptions, which may contain credentials.
            try:
                error_body = json.loads(exc.read(65536).decode("utf-8"))
                error = error_body.get("error", {})
                error = error if isinstance(error, dict) else {}
            except (ValueError, UnicodeError, AttributeError):
                error = {}
            finally:
                exc.close()
            code = error.get("code")
            code = code if isinstance(code, str) else ""
            error_message = str(error.get("message", "")).casefold()
            unsupported_token_option = (
                error.get("param") == "max_completion_tokens"
                or ("max_completion_tokens" in error_message
                    and ("unsupported" in error_message or "not supported" in error_message))
            )
            if exc.code in {400, 422} and unsupported_token_option and not token_compatibility_retry:
                payload["max_tokens"] = payload.pop("max_completion_tokens")
                token_compatibility_retry = True
                continue
            result = _http_failure(exc.code, code)
            if result.code in {"rate_limited", "provider_unavailable"} and transient_retries < 1:
                transient_retries += 1
                pause(1)
                continue
            return result
        except (TimeoutError, urllib.error.URLError, ConnectionError):
            if transient_retries < 1:
                transient_retries += 1
                pause(1)
                continue
            return ModelResult(code="connection_failed", message=(
                "The app could not connect to the model service or the request "
                "timed out. Try again; the app owner should check OPENAI_BASE_URL "
                "and the deployment's outbound network access if it persists."
            ))
        except (ValueError, UnicodeError, KeyError, IndexError, TypeError):
            return ModelResult(code="invalid_response", message=(
                "The configured endpoint returned an unexpected response. "
                "The app owner should check that OPENAI_BASE_URL is a compatible "
                "Chat Completions API endpoint."
            ))
    return ModelResult(code="retry_limit", message="The model request could not complete. Try again shortly.")
