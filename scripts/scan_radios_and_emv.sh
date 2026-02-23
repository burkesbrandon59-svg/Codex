#!/usr/bin/env bash
set -euo pipefail

section() {
  printf '\n==== %s ====\n' "$1"
}

have() {
  command -v "$1" >/dev/null 2>&1
}

is_termux() {
  [[ -n "${TERMUX_VERSION:-}" ]] || [[ "${PREFIX:-}" == *"com.termux"* ]] || [[ -d "/data/data/com.termux" ]]
}

section "Environment"
if is_termux; then
  echo "Detected Termux environment."
  cat <<'TERMUX_HINT'
Install/prepare (Termux):
  pkg update && pkg upgrade -y
  pkg install -y root-repo
  pkg install -y termux-api libnfc opensc
  termux-setup-storage

Optional packages (if available on your device/repo):
  pkg install -y bluez iw

Note:
- Android/Termux often cannot do full monitor-mode Wi-Fi scans without root + chipset support.
- Bluetooth and Wi-Fi scans via Termux API require the Termux:API app and Android permissions.
TERMUX_HINT
else
  echo "Detected non-Termux environment."
fi

section "Wi-Fi devices"
if is_termux && have termux-wifi-scaninfo; then
  termux-wifi-scaninfo || true
elif have nmcli; then
  nmcli -f IN-USE,BSSID,SSID,SIGNAL,CHAN,SECURITY device wifi list || true
elif have iw; then
  iw dev || true
  echo "Use: sudo iw dev <iface> scan"
elif is_termux; then
  echo "Use Termux API command: termux-wifi-scaninfo"
  echo "(Requires termux-api package + Termux:API app + location permission)"
else
  echo "Install NetworkManager (nmcli) or iw to scan Wi-Fi targets."
fi

section "Bluetooth devices"
if is_termux && have termux-bluetooth-scan; then
  termux-bluetooth-scan || true
elif have bluetoothctl; then
  echo "Running a short Bluetooth scan (10 seconds)..."
  bluetoothctl --timeout 10 scan on || true
  bluetoothctl devices || true
elif have btmgmt; then
  btmgmt find || true
elif is_termux; then
  echo "Use Termux API command: termux-bluetooth-scan"
  echo "(Requires termux-api package + Termux:API app + nearby-devices permission)"
else
  echo "Install bluez tools (bluetoothctl/btmgmt)."
fi

section "NFC readers and nearby NFC targets"
if have nfc-list; then
  nfc-list || true
else
  echo "Install libnfc tools to use nfc-list."
fi

if have nfc-poll; then
  echo "Polling once for nearby NFC targets..."
  nfc-poll || true
else
  echo "Install libnfc tools to use nfc-poll."
fi

section "PC/SC smartcard readers"
if have opensc-tool; then
  opensc-tool -n || true
else
  echo "Install opensc to enumerate smartcard/NFC readers."
fi

cat <<'NOTE'

NOTE:
- You can discover nearby radio devices (Wi-Fi/Bluetooth/NFC tags).
- For payment cards, consumer tools can usually show card ATR, UID (if available),
  and EMV application labels (for example Visa/Mastercard app labels).
- They cannot legally/reliably reveal private cardholder identity data such as the
  person's name from a contactless tap.

To monitor card insert/tap events on Linux/Termux, run:
  pcsc_scan

To inspect card applications with pcsc-tools:
  scriptor
  > /card
  > /select 315041592e5359532e4444463031

NOTE
