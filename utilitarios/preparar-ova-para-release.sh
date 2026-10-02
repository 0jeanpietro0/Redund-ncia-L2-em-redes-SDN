#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -lt 1 || "$#" -gt 2 ]]; then
    printf 'Uso: %s /caminho/arquivo.ova [diretorio-de-saida]\n' "$0" >&2
    exit 2
fi

caminho_ova="$(readlink -f -- "$1")"

if [[ ! -f "${caminho_ova}" ]]; then
    printf 'Arquivo não encontrado: %s\n' "$1" >&2
    exit 1
fi

nome_ova="$(basename -- "${caminho_ova}")"
diretorio_ova="$(dirname -- "${caminho_ova}")"
diretorio_saida="${2:-${diretorio_ova}/arquivos-da-release}"
tamanho_parte_mib=1900
limite_parte_bytes=$((tamanho_parte_mib * 1024 * 1024))
tamanho_ova_bytes="$(stat -c '%s' -- "${caminho_ova}")"

mkdir -p -- "${diretorio_saida}"

hash_ova="$(sha256sum -- "${caminho_ova}" | awk '{print $1}')"
printf '%s  %s\n' "${hash_ova}" "${nome_ova}" > "${diretorio_saida}/${nome_ova}.sha256"

printf 'OVA: %s\n' "${caminho_ova}"
printf 'Tamanho: %s bytes\n' "${tamanho_ova_bytes}"
printf 'SHA-256: %s\n' "${hash_ova}"

if (( tamanho_ova_bytes < limite_parte_bytes )); then
    printf '\nO arquivo cabe em um único ativo de Release.\n'
    printf 'Envie a OVA original e: %s\n' "${diretorio_saida}/${nome_ova}.sha256"
    exit 0
fi

prefixo_parte="${diretorio_saida}/${nome_ova}."
split \
    --bytes="${tamanho_parte_mib}M" \
    --numeric-suffixes=0 \
    --suffix-length=3 \
    --additional-suffix=.parte \
    -- "${caminho_ova}" "${prefixo_parte}"

(
    cd -- "${diretorio_saida}"
    sha256sum -- "${nome_ova}".*.parte > "${nome_ova}.partes.sha256"
)

printf '\nA OVA foi dividida em partes menores que 2 GiB.\n'
printf 'Diretório dos ativos: %s\n' "${diretorio_saida}"
printf 'Envie todas as partes e os dois arquivos de checksum.\n'
printf 'Remontagem: cat %s.*.parte > %s\n' "${nome_ova}" "${nome_ova}"
