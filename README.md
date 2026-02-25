# Codex

## Codex System Architecture

_Last updated: Feb 23_

This repository documents the high-level architecture used by Codex to plan, execute, and validate software tasks in a secure, tool-driven environment.

### 1. Core Runtime

Codex runs as an orchestrator around a reasoning model, combining natural-language planning with deterministic tool calls:

- **Model layer**: Interprets user intent, constraints, and repository context.
- **Execution layer**: Invokes tools for shell execution, file operations, browser automation, and PR creation.
- **Control layer**: Enforces instruction hierarchy (system > developer > repository > user) and completion requirements.

### 2. Instruction Resolution

Instruction handling is compositional and scoped:

1. Global/system instructions define invariant behavior.
2. Developer instructions define environment-specific workflow requirements.
3. Repository instructions (`AGENTS.md`) apply by directory scope.
4. User instructions provide task-level goals.

When multiple instruction sources exist, Codex resolves conflicts by precedence and nearest scope.

### 3. Tooling Interfaces

Codex integrates with local and remote capabilities through typed tool contracts:

- **Shell tooling** for git, tests, and project automation.
- **Planning tooling** to track multi-step work execution.
- **MCP resources** for structured context retrieval.
- **Browser automation** for visual verification and screenshots.
- **PR automation** for publishing title/body metadata after commit.

### 4. Task Lifecycle

A typical execution follows this sequence:

1. Discover repository state and constraints.
2. Read relevant scoped instructions.
3. Inspect and modify files.
4. Run tests/checks.
5. Commit validated changes.
6. Draft PR metadata.
7. Return a concise, cited summary.

### 5. Safety and Reliability

Codex is designed to minimize accidental drift:

- Uses explicit commands over implicit assumptions.
- Reports test outcomes with pass/warn/fail signals.
- Avoids destructive actions unless explicitly requested.
- Distinguishes environment limitations from code failures.

### 6. Outputs and Traceability

Every completed task should provide:

- A clean git commit on the active branch.
- A PR title/body aligned to implemented changes.
- File/line citations in the final summary for auditability.

### 7. Extensibility

Codex can be extended via skills and MCP servers:

- **Skills** encode reusable workflows and domain-specific procedures.
- **MCP servers** expose external resources and templates.
- **Composable prompts** allow targeted behavior without code changes.

This architecture keeps Codex adaptable while preserving operational consistency across repositories and environments.
