#!/usr/bin/env bash
set -euo pipefail

diretorio_script="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
diretorio_repositorio="$(cd -- "${diretorio_script}/.." && pwd)"
topologia_padrao="reproducao/codigo/topologias/topologia_arp_proxy_v3.py"
arquivo_topologia="${TOPOLOGIA:-${topologia_padrao}}"

cd -- "${diretorio_repositorio}"

if [[ ! -f "${arquivo_topologia}" ]]; then
    printf 'Topologia não encontrada: %s\n' "${arquivo_topologia}" >&2
    printf 'Defina TOPOLOGIA com o caminho relativo à raiz do repositório.\n' >&2
    exit 1
fi

printf 'Topologia: %s\n' "${arquivo_topologia}"
exec sudo python3 "${arquivo_topologia}" "$@"
