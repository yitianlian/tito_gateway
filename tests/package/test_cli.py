from tito_gateway.cli import main


def test_cli_top_level_help(capsys):
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0

    assert "Standalone wrapper around Miles TITO" in capsys.readouterr().out


def test_cli_serve_help(capsys):
    try:
        main(["serve", "--help"])
    except SystemExit as exc:
        assert exc.code == 0

    assert "--hf-checkpoint" in capsys.readouterr().out


def test_cli_verify_placeholder_returns_nonzero(capsys):
    code = main(["verify-chat-template"])

    assert code == 2
    assert "verifier will be enabled" in capsys.readouterr().err
