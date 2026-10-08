# Scripts auxiliares

| Script | Uso |
|---|---|
| `preflight.sh` | Verifica comandos necessários e compila todos os arquivos Python |
| `collect-environment-info.sh` | Registra versões do ambiente |
| `run-controller.sh` | Inicia o controlador indicado; usa v3.7 como padrão |
| `run-topology.sh` | Inicia a topologia indicada; usa o anel SDN como padrão |
| `cleanup-mininet.sh` | Executa a limpeza do Mininet |
| `prepare-ova-release.sh` | Calcula SHA-256 e divide uma OVA no Linux |
| `preparar-ova-windows.ps1` | Calcula SHA-256 e cria volumes 7-Zip de 1900 MiB no Windows |

## Controlador

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py
```

Argumentos adicionais são encaminhados ao `ryu-manager`:

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py --verbose
```

## Topologia

```bash
./scripts/run-topology.sh topologies/topologia_malha_arp_proxy_v37.py
```

## Máquina virtual no Windows

Abra o PowerShell e execute:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\preparar-ova-windows.ps1 -OvaPath "C:\CAMINHO\mn.ova"
```

O script requer o 7-Zip quando a OVA ultrapassa 1900 MiB.
