#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "${script_dir}/.." && pwd)"

topology_file="${1:-topologies/topologia_arp_proxy_anel_3s_6h.py}"
if [[ "$#" -gt 0 ]]; then
    shift
fi

if [[ "${topology_file}" != /* ]]; then
    topology_file="${repo_dir}/${topology_file}"
fi

if [[ ! -f "${topology_file}" ]]; then
    printf 'Topologia não encontrada: %s\n' "${topology_file}" >&2
    printf 'Exemplo: %s topologies/topologia_arp_proxy_anel_3s_6h.py\n' "$0" >&2
    exit 1
fi

cd -- "${repo_dir}"
printf 'Iniciando topologia: %s\n' "${topology_file}"
exec sudo python3 "${topology_file}" "$@"
