#!/usr/bin/env bash
set -euo pipefail

diretorio_script="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
diretorio_repositorio="$(cd -- "${diretorio_script}/.." && pwd)"

comandos_obrigatorios=(
    python3 ryu-manager mn ovs-vsctl ovs-ofctl ovs-appctl
    tcpdump iperf sha256sum git
)
ausente=0

for nome_comando in "${comandos_obrigatorios[@]}"; do
    if command -v "${nome_comando}" >/dev/null 2>&1; then
        printf '[OK] %s\n' "${nome_comando}"
    else
        printf '[AUSENTE] %s\n' "${nome_comando}" >&2
        ausente=1
    fi
done

while IFS= read -r -d '' arquivo_python; do
    python3 -m py_compile "${arquivo_python}"
    printf '[OK] Sintaxe: %s\n' "${arquivo_python#"${diretorio_repositorio}/"}"
done < <(
    find "${diretorio_repositorio}/reproducao/codigo" \
        -type f -name '*.py' -print0 | sort -z
)

if [[ "${ausente}" -ne 0 ]]; then
    printf 'O ambiente ainda não contém todos os comandos necessários.\n' >&2
    exit 1
fi

printf 'Verificação do ambiente concluída.\n'
