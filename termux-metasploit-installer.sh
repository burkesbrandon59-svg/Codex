#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if [[ "$(uname -o 2>/dev/null || true)" != "Android" ]]; then
  echo "This installer is intended for Termux on Android."
  exit 1
fi

if [[ -z "${PREFIX:-}" || "$PREFIX" != *"com.termux"* ]]; then
  echo "Please run this from inside the Termux app."
  exit 1
fi

echo "[1/5] Updating package metadata..."
pkg update -y && pkg upgrade -y

echo "[2/5] Installing base dependencies..."
pkg install -y curl wget git ruby openssl libffi libgmp ncurses-utils unstable-repo

echo "[3/5] Installing Metasploit package from Termux unstable repo..."
pkg install -y metasploit

echo "[4/5] Updating gem dependencies used by Metasploit..."
gem update --system --no-document || true
gem install bundler --no-document || true

echo "[5/5] Initializing Metasploit database (optional)..."
if command -v msfdb >/dev/null 2>&1; then
  msfdb init || true
fi

echo
echo "Metasploit installation finished."
echo "Start with: msfconsole"
