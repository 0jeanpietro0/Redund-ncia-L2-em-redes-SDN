#!/usr/bin/env bash
set -euo pipefail

diretorio_script="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
diretorio_repositorio="$(cd -- "${diretorio_script}/.." && pwd)"

executar_e_mostrar() {
    local rotulo="$1"
    shift
    printf '\n[%s]\n' "${rotulo}"
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

executar_e_mostrar 'Python' python3 --version
executar_e_mostrar 'Ryu Manager' ryu-manager --version
executar_e_mostrar 'Mininet' mn --version
executar_e_mostrar 'Open vSwitch' ovs-vsctl --version
executar_e_mostrar 'Utilitário OpenFlow' ovs-ofctl --version
executar_e_mostrar 'tcpdump' tcpdump --version
executar_e_mostrar 'iperf' iperf --version
executar_e_mostrar 'VirtualBox' VBoxManage --version

printf '\n[Módulo Python Ryu]\n'
python3 - <<'PY' 2>/dev/null || true
try:
    import importlib.metadata
    print(importlib.metadata.version("ryu"))
except Exception as exc:
    print(f"não disponível: {exc}")
PY

printf '\n[Pacote Python Eventlet]\n'
python3 - <<'PY' 2>/dev/null || true
try:
    import importlib.metadata
    print(importlib.metadata.version("eventlet"))
except Exception as exc:
    print(f"não disponível: {exc}")
PY

printf '\n[Commit do repositório]\n'
git -C "${diretorio_repositorio}" rev-parse HEAD 2>/dev/null \
    || printf 'não disponível\n'

printf '\n[Estado do repositório]\n'
if [[ -z "$(git -C "${diretorio_repositorio}" status --porcelain 2>/dev/null)" ]]; then
    printf 'sem alterações locais rastreadas\n'
else
    printf 'existem alterações locais ou não rastreadas; registre-as antes da execução final\n'
fi
