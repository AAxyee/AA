import importlib
import io
import json
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from model_client import (
    ModelConfig, ModelResult, configuration_status, load_model_config, request_completion,
)
from research_design import design_offline_response


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return json.dumps(self.data).encode()


def reply(content="A tailored answer"):
    return FakeResponse({"choices": [{"message": {"content": content}}]})


def http_error(status, code="", param=None, message=""):
    data = json.dumps({"error": {"code": code, "param": param, "message": message}}).encode()
    return urllib.error.HTTPError("https://api.openai.com/v1/chat/completions", status,
                                  "Provider error", {}, io.BytesIO(data))


class ModelClientTests(unittest.TestCase):
    def setUp(self):
        self.config = ModelConfig("test-key-not-a-real-credential")

    def test_top_level_secret_names_are_supported(self):
        for name in ("OPENAI_API_KEY", "openai_api_key", "API_KEY", "api_key"):
            with self.subTest(name=name):
                self.assertEqual(load_model_config({name: "  key  "}, {}).api_key, "key")

    def test_nested_secrets_include_model_and_provider(self):
        config = load_model_config({"openai": {
            "api_key": "key", "model": "my-model", "base_url": "https://example.com/v1"
        }}, {})
        self.assertEqual(config, ModelConfig("key", "my-model", "https://example.com/v1"))

    def test_top_level_secrets_take_precedence_consistently(self):
        config = load_model_config({"OPENAI_MODEL": "selected", "OPENAI_API_KEY": "secret",
                                    "openai": {"model": "nested", "api_key": "nested"}},
                                   {"OPENAI_MODEL": "environment", "OPENAI_API_KEY": "environment"})
        self.assertEqual((config.model, config.api_key), ("selected", "secret"))

    def test_missing_secrets_store_still_allows_environment_configuration(self):
        secrets = MagicMock()
        secrets.get.side_effect = FileNotFoundError("No secrets file")
        self.assertEqual(load_model_config(secrets, {"OPENAI_API_KEY": "env-key"}).api_key,
                         "env-key")

    def test_missing_key_never_makes_an_api_request(self):
        opener = MagicMock()
        result = request_completion([], ModelConfig(""), opener=opener)
        self.assertEqual(result.code, "missing_api_key")
        opener.assert_not_called()

    def test_invalid_endpoint_is_diagnosed_before_request(self):
        for url in ("not a URL", "https://[bad", "https://user:key@example.com/v1",
                    "https://example.com/v1?api_key=secret", "http://example.com/v1"):
            with self.subTest(url=url):
                opener = MagicMock()
                result = request_completion([], ModelConfig("key", base_url=url), opener=opener)
                self.assertEqual(result.code, "invalid_configuration")
                opener.assert_not_called()

    def test_key_is_not_in_configuration_repr(self):
        self.assertNotIn(self.config.api_key, repr(self.config))

    def test_success_builds_valid_request_without_temperature_assumption(self):
        opener = MagicMock(return_value=reply("  My recommendation  "))
        result = request_completion([{"role": "user", "content": "Design a study"}],
                                    self.config, opener=opener)
        self.assertEqual(result.text, "My recommendation")
        self.assertEqual(result.code, "connected")
        req = opener.call_args.args[0]
        self.assertEqual(req.full_url, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(req.get_header("Authorization"), "Bearer " + self.config.api_key)
        self.assertNotIn("temperature", json.loads(req.data))

    def test_full_endpoint_is_not_appended_twice(self):
        opener = MagicMock(return_value=reply())
        request_completion([], ModelConfig("key", base_url="https://example.com/v1/chat/completions"),
                           opener=opener)
        self.assertEqual(opener.call_args.args[0].full_url,
                         "https://example.com/v1/chat/completions")

    def test_authentication_failure_is_not_retried_or_leaked(self):
        opener = MagicMock(side_effect=http_error(401, message="Bad key " + self.config.api_key))
        result = request_completion([], self.config, opener=opener)
        self.assertEqual(result.code, "authentication_failed")
        self.assertNotIn(self.config.api_key, result.message)
        opener.assert_called_once()

    def test_quota_exhaustion_is_distinct_from_rate_limit(self):
        opener = MagicMock(side_effect=http_error(429, code="insufficient_quota"))
        result = request_completion([], self.config, opener=opener)
        self.assertEqual(result.code, "quota_exhausted")
        opener.assert_called_once()

    def test_transient_rate_limit_retries_once_and_recovers(self):
        opener = MagicMock(side_effect=[http_error(429, code="rate_limit_exceeded"), reply()])
        sleep = MagicMock()
        result = request_completion([], self.config, opener=opener, sleep=sleep)
        self.assertEqual(result.code, "connected")
        self.assertEqual(opener.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_persistent_network_failure_has_bounded_retry(self):
        opener = MagicMock(side_effect=urllib.error.URLError("network detail " + self.config.api_key))
        result = request_completion([], self.config, opener=opener, sleep=MagicMock())
        self.assertEqual(result.code, "connection_failed")
        self.assertEqual(opener.call_count, 2)
        self.assertNotIn(self.config.api_key, result.message)

    def test_provider_token_parameter_compatibility_fallback(self):
        opener = MagicMock(side_effect=[http_error(400, param="max_completion_tokens"), reply()])
        result = request_completion([], self.config, opener=opener)
        self.assertEqual(result.code, "connected")
        self.assertIn("max_completion_tokens", json.loads(opener.call_args_list[0].args[0].data))
        second = json.loads(opener.call_args_list[1].args[0].data)
        self.assertIn("max_tokens", second)
        self.assertNotIn("max_completion_tokens", second)

    def test_missing_model_is_diagnosed_without_changing_model(self):
        opener = MagicMock(side_effect=http_error(404, code="model_not_found"))
        result = request_completion([], self.config, opener=opener)
        self.assertEqual(result.code, "model_or_endpoint_not_found")
        opener.assert_called_once()

    def test_empty_and_malformed_responses_do_not_crash(self):
        for response in (reply(None), reply("  "), FakeResponse({"unexpected": "response"})):
            result = request_completion([], self.config, opener=MagicMock(return_value=response))
            self.assertIsNone(result.text)
            self.assertIn(result.code, {"empty_response", "invalid_response"})

    def test_design_fallback_explains_specific_failure(self):
        result = ModelResult(code="quota_exhausted", message="API quota has been reached.")
        text = design_offline_response([("Study design checklist.pdf", "Purpose")], result.status())
        self.assertIn("API quota has been reached", text)
        self.assertNotIn("not configured or could not be reached", text)

    def test_all_app_wrappers_retain_safe_connection_status(self):
        with patch.dict(sys.modules, {"streamlit": MagicMock()}):
            for name in ("streamlit_app", "streamlit_app1", "streamlit_app2"):
                app = importlib.import_module(name)
                ui = MagicMock()
                with patch.object(app, "st", ui), \
                     patch.object(app, "request_completion", return_value=ModelResult(
                         code="authentication_failed", message="Key rejected."
                     )):
                    self.assertIsNone(app.call_llm([]))
                    self.assertEqual(ui.session_state.llm_status["code"], "authentication_failed")


if __name__ == "__main__":
    unittest.main()
