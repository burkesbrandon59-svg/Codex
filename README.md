# Codex: Nearby Radio Scan Helper

This repo includes a scanner script for:

- Nearby **Wi-Fi** targets
- Nearby **Bluetooth** targets
- Nearby **NFC** readers/targets
- Smartcard/NFC reader enumeration and basic EMV workflow hints

## Quick start (Linux host)

```bash
chmod +x scripts/scan_radios_and_emv.sh
./scripts/scan_radios_and_emv.sh
```

## Quick start (Termux on Android)

```bash
pkg update && pkg upgrade -y
pkg install -y root-repo
pkg install -y termux-api libnfc opensc
termux-setup-storage
chmod +x scripts/scan_radios_and_emv.sh
./scripts/scan_radios_and_emv.sh
```

Also install the **Termux:API** Android app, then grant requested permissions (location for Wi-Fi scan info, nearby devices/Bluetooth where applicable).

> Note: Unrooted Android devices often cannot do full low-level Wi-Fi scanning/monitor mode with `iw`; use `termux-wifi-scaninfo` where available.

## One-liner commands (manual)

### Wi-Fi

Linux:

```bash
nmcli -f IN-USE,BSSID,SSID,SIGNAL,CHAN,SECURITY device wifi list
```

Termux:

```bash
termux-wifi-scaninfo
```

### Bluetooth

Linux:

```bash
bluetoothctl --timeout 10 scan on
bluetoothctl devices
```

Termux:

```bash
termux-bluetooth-scan
```

### NFC

```bash
nfc-list
nfc-poll
```

### Smartcard/NFC reader inventory

```bash
opensc-tool -n
pcsc_scan
```

## About "credit card names by device"

You can often read:

- Reader name
- Card ATR / protocol info
- EMV application labels (app-level labels)

You generally **cannot** legally/reliably retrieve private cardholder identity (like the person's real name) from a standard contactless tap with generic tools.
