#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "${script_dir}/.." && pwd)"

cd -- "${repo_dir}"
exec ryu-manager controller/arp_proxy_v3.py --observe-links "$@"
