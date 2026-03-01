"""Advanced AI UI CLI demo.

Provides a richer command-line interface for interacting with a simulated
AI assistant persona. The implementation is intentionally offline-safe:
responses are generated locally so the CLI is deterministic in tests.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable


PERSONA_HINTS = {
    "assistant": "Provide clear, practical guidance.",
    "architect": "Emphasize trade-offs, design patterns, and scalability.",
    "debugger": "Prioritize root-cause analysis and reproducible fixes.",
    "ghost": "Speak as a subtle system guide that helps from behind the terminal.",
}

TRAINING_BASELINES = {
    "offline": "Use only local context and deterministic reasoning.",
    "internet": "Incorporate internet-aware assumptions while calling out verification needs.",
}


@dataclass
class AiUiRequest:
    mode: str
    prompt: str
    stream: bool
    output_format: str
    training_baseline: str


def parse_args(argv: list[str] | None = None) -> AiUiRequest:
    parser = argparse.ArgumentParser(prog="advanced-ai-ui-cli")
    parser.add_argument("--mode", choices=sorted(PERSONA_HINTS), default="assistant")
    parser.add_argument("--prompt", required=True, help="User prompt to process")
    parser.add_argument("--stream", action="store_true", help="Emit response in token chunks")
    parser.add_argument("--format", dest="output_format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--training-baseline",
        choices=sorted(TRAINING_BASELINES),
        default="offline",
        help="Select the operating assumption profile for the response",
    )
    ns = parser.parse_args(argv)
    return AiUiRequest(
        mode=ns.mode,
        prompt=ns.prompt,
        stream=ns.stream,
        output_format=ns.output_format,
        training_baseline=ns.training_baseline,
    )


def build_response(request: AiUiRequest) -> str:
    hint = PERSONA_HINTS[request.mode]
    baseline_hint = TRAINING_BASELINES[request.training_baseline]
    return (
        f"Mode: {request.mode}\n"
        f"Prompt: {request.prompt}\n"
        f"Training baseline: {request.training_baseline}\n"
        f"Guidance: {hint}\n"
        f"Context policy: {baseline_hint}\n"
        "Next: break the task into plan, implementation, and validation."
    )


def stream_chunks(text: str, chunk_size: int = 20) -> Iterable[str]:
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


def render_output(request: AiUiRequest, response: str) -> str:
    if request.output_format == "json":
        payload = {
            "mode": request.mode,
            "prompt": request.prompt,
            "training_baseline": request.training_baseline,
            "response": response,
        }
        return json.dumps(payload, indent=2)
    return response


def run(argv: list[str] | None = None) -> int:
    request = parse_args(argv)
    response = build_response(request)

    if request.stream:
        for part in stream_chunks(render_output(request, response)):
            print(part, end="", flush=True)
        print()
    else:
        print(render_output(request, response))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
