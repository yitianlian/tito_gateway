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
    code = main(["verify-session-tito-tokenizer"])

    assert code == 2
    assert "verifier will be enabled" in capsys.readouterr().err


def test_cli_verify_chat_template_help(capsys):
    try:
        main(["verify-chat-template", "--help"])
    except SystemExit as exc:
        assert exc.code == 0

    out = capsys.readouterr().out
    assert "--template" in out
    assert "--tito-allowed-append-roles" in out


def test_cli_verify_chat_template_runs_real_verifier(tmp_path, capsys):
    template = tmp_path / "simple.jinja"
    template.write_text(
        "{%- for message in messages -%}"
        "{{ '<|' + message['role'] + '|>' + (message.get('content') or '') }}"
        "{%- endfor -%}"
        "{%- if add_generation_prompt -%}{{ '<|assistant|>' }}{%- endif -%}"
    )

    code = main(["verify-chat-template", "--template", str(template), "--thinking", "off"])

    captured = capsys.readouterr()
    assert code == 0
    assert "Verdict: PASS - template IS append-only" in captured.out
