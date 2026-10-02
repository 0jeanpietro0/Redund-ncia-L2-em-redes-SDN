#!/usr/bin/env bash
set -euo pipefail

printf 'Limpando processos, interfaces e bridges residuais do Mininet...\n'
exec sudo mn -c
