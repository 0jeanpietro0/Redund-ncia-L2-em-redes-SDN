#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "${script_dir}/.." && pwd)"

required_commands=(python3 ryu-manager mn ovs-vsctl ovs-ofctl)
missing=0

for command_name in "${required_commands[@]}"; do
    if command -v "${command_name}" >/dev/null 2>&1; then
        printf '[OK] %s\n' "${command_name}"
    else
        printf '[AUSENTE] %s\n' "${command_name}" >&2
        missing=1
    fi
done

python3 -m py_compile \
    "${repo_dir}/controller/arp_proxy_v3.py" \
    "${repo_dir}/topologies/topologia_arp_proxy_v3.py"
printf '[OK] Sintaxe dos scripts Python\n'

if [[ "${missing}" -ne 0 ]]; then
    printf 'O ambiente ainda não contém todos os comandos necessários.\n' >&2
    exit 1
fi

printf 'Preflight concluído.\n'
