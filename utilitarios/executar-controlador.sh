#!/usr/bin/env bash
set -euo pipefail

diretorio_script="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
diretorio_repositorio="$(cd -- "${diretorio_script}/.." && pwd)"
controlador_padrao="reproducao/codigo/controlador/arp_proxy_v3.py"
arquivo_controlador="${CONTROLADOR:-${controlador_padrao}}"

cd -- "${diretorio_repositorio}"

if [[ ! -f "${arquivo_controlador}" ]]; then
    printf 'Controlador não encontrado: %s\n' "${arquivo_controlador}" >&2
    printf 'Defina CONTROLADOR com o caminho relativo à raiz do repositório.\n' >&2
    exit 1
fi

printf 'Controlador: %s\n' "${arquivo_controlador}"
exec ryu-manager "${arquivo_controlador}" --observe-links "$@"
