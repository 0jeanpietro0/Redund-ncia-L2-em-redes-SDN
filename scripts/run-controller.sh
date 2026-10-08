#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "${script_dir}/.." && pwd)"

controller_file="${1:-controller/arp_proxy_v3_7.py}"
if [[ "$#" -gt 0 ]]; then
    shift
fi

if [[ "${controller_file}" != /* ]]; then
    controller_file="${repo_dir}/${controller_file}"
fi

if [[ ! -f "${controller_file}" ]]; then
    printf 'Controlador não encontrado: %s\n' "${controller_file}" >&2
    printf 'Exemplo: %s controller/arp_proxy_v3_7.py\n' "$0" >&2
    exit 1
fi

cd -- "${repo_dir}"
printf 'Iniciando controlador: %s\n' "${controller_file}"
exec ryu-manager "${controller_file}" --observe-links "$@"
