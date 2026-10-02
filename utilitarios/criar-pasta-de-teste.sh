#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 1 ]]; then
    printf 'Uso: %s nome-do-cenario\n' "$0" >&2
    exit 2
fi

cenario="$1"

if [[ ! "${cenario}" =~ ^[a-z0-9][a-z0-9._-]*$ ]]; then
    printf 'Use somente letras minúsculas sem acento, números, ponto, hífen ou sublinhado.\n' >&2
    exit 2
fi

diretorio_script="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
diretorio_repositorio="$(cd -- "${diretorio_script}/.." && pwd)"
identificador="$(date '+%Y-%m-%d-%H%M%S')-${cenario}"
diretorio_resultado="${diretorio_repositorio}/reproducao/resultados/brutos/${identificador}"

mkdir -p -- "${diretorio_resultado}"

git -C "${diretorio_repositorio}" rev-parse HEAD \
    > "${diretorio_resultado}/commit.txt"

"${diretorio_script}/coletar-informacoes-do-ambiente.sh" \
    > "${diretorio_resultado}/ambiente.txt"

{
    printf '# Comandos da execução\n\n'
    printf -- '- Cenário: `%s`\n' "${cenario}"
    printf -- '- Início: `%s`\n' "$(date --iso-8601=seconds)"
    printf -- '- Controlador: `PREENCHER`\n'
    printf -- '- Topologia: `PREENCHER`\n'
    printf -- '- Parâmetros: `PREENCHER`\n\n'
    printf '## Ordem dos comandos\n\n'
    printf '1. `PREENCHER`\n'
} > "${diretorio_resultado}/COMANDOS.md"

printf '%s\n' "${diretorio_resultado}"
