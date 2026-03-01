import json

from agent_loop.advanced_ai_ui_cli import (
    AiUiRequest,
    build_response,
    parse_args,
    render_output,
    run,
)


def test_parse_args_defaults() -> None:
    req = parse_args(["--prompt", "Design a CLI"])
    assert req.mode == "assistant"
    assert req.output_format == "text"
    assert req.stream is False
    assert req.training_baseline == "offline"


def test_json_render_output_contains_fields() -> None:
    req = AiUiRequest(
        mode="architect",
        prompt="Scale this",
        stream=False,
        output_format="json",
        training_baseline="internet",
    )
    payload = json.loads(render_output(req, build_response(req)))
    assert payload["mode"] == "architect"
    assert payload["training_baseline"] == "internet"
    assert "trade-offs" in payload["response"]


def test_ghost_mode_internet_baseline_response() -> None:
    req = AiUiRequest(
        mode="ghost",
        prompt="Create and send a shell as the ghost in the machine",
        stream=False,
        output_format="text",
        training_baseline="internet",
    )
    response = build_response(req)
    assert "Mode: ghost" in response
    assert "Training baseline: internet" in response
    assert "internet-aware" in response


def test_run_streaming_output(capsys) -> None:
    exit_code = run(["--mode", "debugger", "--prompt", "Trace failure", "--stream"])
    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "root-cause" in captured
