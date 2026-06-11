import pytest

from tito_gateway.config import TITOGatewayConfig
from tito_gateway.discovery import discover_backend_url


def test_explicit_backend_url_wins_over_environment():
    env = {"TITO_BACKEND_URL": "http://env.example:3000"}

    assert discover_backend_url("localhost:8000", env=env) == "http://localhost:8000"


def test_environment_precedence_is_deterministic():
    env = {
        "OPENAI_BASE_URL": "http://openai.example:8000",
        "SGLANG_BASE_URL": "http://sglang.example:8000",
    }

    assert discover_backend_url(env=env) == "http://openai.example:8000"


def test_missing_backend_url_fails_clearly():
    with pytest.raises(RuntimeError, match="backend URL not found"):
        discover_backend_url(env={})


def test_cli_json_kwargs_parse_to_dict():
    config = TITOGatewayConfig.from_cli_values(
        hf_checkpoint="model",
        backend_url="http://backend",
        chat_template_path=None,
        apply_chat_template_kwargs='{"enable_thinking": false}',
        tito_model="qwen3",
        tito_allowed_append_roles=["tool", "user"],
        session_server_ip="127.0.0.1",
        session_server_port=30000,
        miles_router_timeout=30,
    )

    assert config.apply_chat_template_kwargs == {"enable_thinking": False}
    assert config.tito_allowed_append_roles == ("tool", "user")


def test_invalid_append_role_fails():
    with pytest.raises(ValueError, match="unsupported tito append roles"):
        TITOGatewayConfig(hf_checkpoint="model", tito_allowed_append_roles=("assistant",))
