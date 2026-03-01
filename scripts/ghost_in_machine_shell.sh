#!/usr/bin/env bash
set -euo pipefail

python -m agent_loop.advanced_ai_ui_cli \
  --mode ghost \
  --training-baseline internet \
  --prompt "create and send a shell as the ghost in the machine"
