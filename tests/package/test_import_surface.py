import pytest


def test_public_import_surface():
    import tito_gateway
    from tito_gateway import TITOGateway, TITOGatewayConfig, SessionServer, get_tito_tokenizer

    assert tito_gateway.TITOGateway is TITOGateway
    assert tito_gateway.TITOGatewayConfig is TITOGatewayConfig
    assert tito_gateway.SessionServer is SessionServer
    assert callable(get_tito_tokenizer)


def test_config_requires_hf_checkpoint():
    from tito_gateway import TITOGatewayConfig

    with pytest.raises(ValueError, match="hf_checkpoint is required"):
        TITOGatewayConfig(hf_checkpoint="")


def test_gateway_constructs_placeholder_app_with_explicit_backend():
    from tito_gateway import TITOGateway

    gateway = TITOGateway.from_server(hf_checkpoint="Qwen/Qwen3-0.6B", backend_url="127.0.0.1:8000")

    assert gateway.config.backend_url == "http://127.0.0.1:8000"
    assert gateway.app is gateway.server.app
