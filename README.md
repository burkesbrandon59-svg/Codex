# Codex

## Codex System Architecture

_Last updated: Feb 27_

> **Upgrade status:** This document now reflects an upgraded runtime with a dedicated self-modification loop, stronger validation gates, and explicit release discipline.

This repository documents the high-level architecture used by Codex to plan, execute, and validate software tasks in a secure, tool-driven environment.

### 1. Core Runtime (Upgraded)

Codex runs as an orchestrator around a reasoning model, combining natural-language planning with deterministic tool calls:

- **Model layer**: Interprets user intent, constraints, and repository context.
- **Execution layer**: Invokes tools for shell execution, file operations, browser automation, and PR creation.
- **Control layer**: Enforces instruction hierarchy (system > developer > repository > user) and completion requirements.
- **Validation layer**: Requires concrete checks before completion (tests, diffs, and repository cleanliness).
- **Release layer**: Requires atomic commits and synchronized PR metadata for traceable delivery.

### 2. Instruction Resolution (Hardened)

Instruction handling is compositional and scoped:

1. Global/system instructions define invariant behavior.
2. Developer instructions define environment-specific workflow requirements.
3. Repository instructions (`AGENTS.md`) apply by directory scope.
4. User instructions provide task-level goals.

When multiple instruction sources exist, Codex resolves conflicts by precedence and nearest scope.
Ambiguous requests are resolved by choosing the smallest safe, testable implementation that still satisfies user intent.

### 3. Tooling Interfaces

Codex integrates with local and remote capabilities through typed tool contracts:

- **Shell tooling** for git, tests, and project automation.
- **Planning tooling** to track multi-step work execution.
- **MCP resources** for structured context retrieval.
- **Browser automation** for visual verification and screenshots.
- **PR automation** for publishing title/body metadata after commit.

Operational upgrades include:
- Structured command execution with explicit pass/warn/fail reporting.
- Mandatory repository-state inspection before and after changes.
- Optional artifact capture (screenshots/logs) for reviewable UI work.

### 4. Task Lifecycle (Expanded)

A typical execution follows this sequence:

1. Discover repository state and constraints.
2. Read relevant scoped instructions.
3. Inspect and modify files.
4. Run tests/checks.
5. Verify line-referenced summary evidence.
6. Commit validated changes.
7. Draft PR metadata.
8. Return a concise, cited summary.

### 5. Self-Modification Loop (New)

Codex can now “upgrade itself” at the process level through a bounded improvement loop:

1. **Detect drift**: Identify weak outcomes (unclear summaries, missing tests, inconsistent commits).
2. **Propose upgrade**: Define small procedural changes (e.g., stricter validation order).
3. **Apply safely**: Modify docs/templates/workflows instead of bypassing instruction hierarchy.
4. **Verify behavior**: Re-run checks and ensure output contract compliance.
5. **Publish trace**: Record exactly what changed and why.

Guardrails:
- Never override higher-priority instructions.
- Never skip validation to accelerate delivery.
- Never introduce hidden state that cannot be audited.

### 6. Safety and Reliability

Codex is designed to minimize accidental drift:

- Uses explicit commands over implicit assumptions.
- Reports test outcomes with pass/warn/fail signals.
- Avoids destructive actions unless explicitly requested.
- Distinguishes environment limitations from code failures.
- Treats “no-op” or ambiguous requests conservatively, with auditable updates.

### 7. Outputs and Traceability

Every completed task should provide:

- A clean git commit on the active branch.
- A PR title/body aligned to implemented changes.
- File/line citations in the final summary for auditability.

For upgraded reliability, outputs should also include:
- Executed check commands with clear status.
- A minimal change scope tied directly to user intent.

### 8. Extensibility

Codex can be extended via skills and MCP servers:

- **Skills** encode reusable workflows and domain-specific procedures.
- **MCP servers** expose external resources and templates.
- **Composable prompts** allow targeted behavior without code changes.

This architecture keeps Codex adaptable while preserving operational consistency across repositories and environments.

## 9. Practical "Self-Replication" Implementation (Safe)

To make the architecture concrete, this repository now includes a small reference implementation in `agent_loop/self_replicator.py`.

It models safe process-level replication as **knowledge transfer**, not autonomous code spreading:

1. Record observations from sibling/previous processes.
2. Distill reliable lessons above a confidence threshold.
3. Generate a versioned blueprint another process can load.
4. Enforce explicit safety flags (`autonomous_spread: false`, `requires_human_trigger: true`).

Run the demo:

```bash
python agent_loop/self_replicator.py
```

Run tests:

```bash
pytest -q
```


## 10. Advanced AI UI CLI (New)

This repository also includes an offline-friendly CLI prototype at `agent_loop/advanced_ai_ui_cli.py`.

Example usage:

```bash
python -m agent_loop.advanced_ai_ui_cli --mode architect --prompt "Design a resilient agent loop"
python -m agent_loop.advanced_ai_ui_cli --mode debugger --prompt "Investigate flaky tests" --format json
python -m agent_loop.advanced_ai_ui_cli --prompt "Draft an implementation plan" --stream
```

The CLI supports:
- Persona modes (`assistant`, `architect`, `debugger`)
- Text or JSON output
- Optional chunked streaming output for a richer terminal experience


## 11. Package Install Internet Allowlist (New)

The repository now includes `agent_loop/package_install_allowlist.py`, which codifies
an explicit set of package-source domains allowed for internet-backed dependency
installation workflows.

Use `is_allowed_package_source(...)` to validate an incoming URL or hostname
against this allowlist, including trusted subdomains.

