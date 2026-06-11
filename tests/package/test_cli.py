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
    code = main(
        [
            "verify-session-tito-tokenizer",
            "--hf-checkpoint",
            "Qwen/Qwen3-4B",
            "--tito-model",
            "qwen3",
            "--tito-allowed-append-roles",
            "tool",
            "user",
            "--sglang-reasoning-parser",
            "qwen3",
            "--sglang-tool-call-parser",
            "qwen25",
            "--rollout-num-gpus-per-engine",
            "1",
        ]
    )

    assert code == 2
    assert "requires the optional Miles/SGLang session e2e runner" in capsys.readouterr().out


def test_cli_verify_session_help(capsys):
    try:
        main(["verify-session-tito-tokenizer", "--help"])
    except SystemExit as exc:
        assert exc.code == 0

    out = capsys.readouterr().out
    assert "--hf-checkpoint" in out
    assert "--rollout-num-gpus-per-engine" in out
    assert "--assistant-text-threshold" in out


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
