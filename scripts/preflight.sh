#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "${script_dir}/.." && pwd)"

required_commands=(python3 ryu-manager mn ovs-vsctl ovs-ofctl tcpdump iperf git)
missing=0

for command_name in "${required_commands[@]}"; do
    if command -v "${command_name}" >/dev/null 2>&1; then
        printf '[OK] %s\n' "${command_name}"
    else
        printf '[AUSENTE] %s\n' "${command_name}" >&2
        missing=1
    fi
done

mapfile -d '' python_files < <(
    find "${repo_dir}/controller" "${repo_dir}/topologies" \
        -type f -name '*.py' -print0 | sort -z
)

if [[ "${#python_files[@]}" -eq 0 ]]; then
    printf 'Nenhum arquivo Python foi encontrado.\n' >&2
    exit 1
fi

python3 -m py_compile "${python_files[@]}"
printf '[OK] Sintaxe de %d arquivos Python\n' "${#python_files[@]}"

if command -v VBoxManage >/dev/null 2>&1; then
    printf '[OK] VBoxManage\n'
else
    printf '[AVISO] VBoxManage não está disponível; necessário apenas para a VM.\n'
fi

if [[ "${missing}" -ne 0 ]]; then
    printf 'O ambiente não contém todos os comandos necessários para os testes.\n' >&2
    exit 1
fi

printf 'Verificação concluída.\n'
