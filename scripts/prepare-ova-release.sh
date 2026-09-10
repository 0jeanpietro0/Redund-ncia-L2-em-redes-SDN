#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -lt 1 || "$#" -gt 2 ]]; then
    printf 'Uso: %s /caminho/arquivo.ova [diretorio-de-saida]\n' "$0" >&2
    exit 2
fi

ova_path="$(readlink -f -- "$1")"

if [[ ! -f "${ova_path}" ]]; then
    printf 'Arquivo não encontrado: %s\n' "$1" >&2
    exit 1
fi

ova_name="$(basename -- "${ova_path}")"
ova_dir="$(dirname -- "${ova_path}")"
asset_dir="${2:-${ova_dir}/release-assets}"
part_size_mib=1900
part_limit_bytes=$((part_size_mib * 1024 * 1024))
ova_size_bytes="$(stat -c '%s' -- "${ova_path}")"

mkdir -p -- "${asset_dir}"

ova_hash="$(sha256sum -- "${ova_path}" | awk '{print $1}')"
printf '%s  %s\n' "${ova_hash}" "${ova_name}" > "${asset_dir}/${ova_name}.sha256"

printf 'OVA: %s\n' "${ova_path}"
printf 'Tamanho: %s bytes\n' "${ova_size_bytes}"
printf 'SHA-256: %s\n' "${ova_hash}"

if (( ova_size_bytes < part_limit_bytes )); then
    printf '\nO arquivo cabe em um único ativo de Release.\n'
    printf 'Envie a OVA original e: %s\n' "${asset_dir}/${ova_name}.sha256"
    exit 0
fi

part_prefix="${asset_dir}/${ova_name}."
split \
    --bytes="${part_size_mib}M" \
    --numeric-suffixes=0 \
    --suffix-length=3 \
    --additional-suffix=.part \
    -- "${ova_path}" "${part_prefix}"

(
    cd -- "${asset_dir}"
    sha256sum -- "${ova_name}".*.part > "${ova_name}.parts.sha256"
)

printf '\nA OVA foi dividida em partes menores que 2 GiB.\n'
printf 'Diretório dos ativos: %s\n' "${asset_dir}"
printf 'Envie todas as partes e os dois arquivos de checksum.\n'
printf 'Remontagem: cat %s.*.part > %s\n' "${ova_name}" "${ova_name}"
