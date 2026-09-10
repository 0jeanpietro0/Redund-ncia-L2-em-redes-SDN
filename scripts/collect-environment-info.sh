#!/usr/bin/env bash
set -euo pipefail

print_command() {
    local label="$1"
    shift
    printf '\n[%s]\n' "${label}"
    if command -v "$1" >/dev/null 2>&1; then
        "$@" 2>&1 || true
    else
        printf 'não disponível\n'
    fi
}

printf '[Data da coleta]\n'
date --iso-8601=seconds

printf '\n[Kernel]\n'
uname -srmo

if [[ -r /etc/os-release ]]; then
    printf '\n[Sistema operacional]\n'
    grep -E '^(NAME|VERSION|VERSION_ID|PRETTY_NAME)=' /etc/os-release || true
fi

print_command 'Python' python3 --version
print_command 'Ryu Manager' ryu-manager --version
print_command 'Mininet' mn --version
print_command 'Open vSwitch' ovs-vsctl --version
print_command 'OpenFlow utility' ovs-ofctl --version
print_command 'VirtualBox' VBoxManage --version

printf '\n[Módulo Python Ryu]\n'
python3 - <<'PY' 2>/dev/null || true
try:
    import importlib.metadata
    print(importlib.metadata.version("ryu"))
except Exception as exc:
    print(f"não disponível: {exc}")
PY
