# Laboratório ARP Proxy SDN — VM vX.Y.Z

## Identificação

- Tag: `vm-vX.Y.Z`
- Commit do repositório: `PREENCHER`
- Data da exportação: `PREENCHER`
- VirtualBox utilizado na exportação: `PREENCHER`

## Requisitos sugeridos

- Arquitetura: `x86_64`
- Sistema hospedeiro testado: `PREENCHER`
- VirtualBox mínimo testado: `PREENCHER`
- RAM recomendada: `PREENCHER`
- CPUs virtuais: `PREENCHER`
- Espaço livre para download, extração e importação: `PREENCHER`

## Conteúdo da VM

- Sistema operacional: `PREENCHER`
- Python: `3.8.5` ou versão realmente instalada
- Ryu: `4.34` ou versão realmente instalada
- Mininet: `2.6` ou versão realmente instalada
- Open vSwitch: `2.13.1` ou versão realmente instalada
- tcpdump: `4.9.3` ou versão realmente instalada
- iPerf: `2.0.13` ou versão realmente instalada
- Controladores: v3, v3.5, v3.6 e v3.7
- Topologias: 1 switch, 2 switches, anel e malha K4

## Arquivos da Release

```text
mn.7z.001
mn.7z.002
mn.7z.003
mn.7z.parts.sha256
mn.ova.sha256
```

## Download e extração

1. Baixe todas as partes para a mesma pasta.
2. Instale o 7-Zip.
3. Clique com o botão direito em `mn.7z.001`.
4. Selecione **7-Zip → Extrair aqui**.
5. Não extraia `.002` e `.003` separadamente.
6. Verifique o SHA-256 do arquivo resultante.
7. Importe a OVA no VirtualBox.

Instruções completas: `vm/README.md`.

## SHA-256

```text
PREENCHER_HASH_001  mn.7z.001
PREENCHER_HASH_002  mn.7z.002
PREENCHER_HASH_003  mn.7z.003
PREENCHER_HASH_OVA  mn.ova
```

## Validação realizada

- [ ] As três partes foram baixadas novamente.
- [ ] O arquivo foi extraído sem erro.
- [ ] Os hashes foram comparados.
- [ ] A OVA foi importada em uma instalação independente do VirtualBox.
- [ ] `preflight.sh` foi executado.
- [ ] `pingall` foi executado.
- [ ] Um ensaio de contenção ARP foi executado.
- [ ] Um ensaio de failover foi executado.

## Limitações conhecidas

- Ambiente emulado.
- IPv4 estático.
- A aplicação trata especificamente ARP.
- O BFS não implementa balanceamento baseado em carga.
- `PREENCHER OUTRAS LIMITAÇÕES DA VERSÃO`.
