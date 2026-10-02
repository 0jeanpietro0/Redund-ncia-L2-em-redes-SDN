# Topologias Mininet

Coloque neste diretório os scripts exatos das topologias usadas no TCC. Cada arquivo deve deixar explícitos hosts, endereços IP, switches, enlaces, largura de banda, atraso, modo do OVS e versão do OpenFlow.

## Conteúdo atual

| Arquivo | Estado | Uso |
|---|---|---|
| `topologia_arp_proxy_v3.py` | Incluído | SDN com 1 switch e 4 hosts |
| Topologia convencional de 1 switch | Pendente | Referência sem controlador |
| Topologia em anel convencional sem STP | Pendente | Loop L2 e tempestade de broadcast |
| Topologia em anel com STP | Pendente | Comparação com árvore de cobertura |
| Topologia em anel com RSTP | Pendente | Comparação de reconvergência |
| Topologia em anel SDN | Pendente | Contenção de ARP e caminhos redundantes |
| Topologia K4 com RSTP | Pendente | Malha completa, portas bloqueadas e `iperf` |
| Topologia K4 com SDN | Pendente | Malha completa, ARP e utilização dos enlaces |

## Validação ao adicionar uma topologia

```bash
python3 -m py_compile reproducao/codigo/topologias/NOME_DO_ARQUIVO.py
sha256sum reproducao/codigo/topologias/NOME_DO_ARQUIVO.py
```

Antes de publicar, confirme que o script encerra a rede com `net.stop()` mesmo após a CLI e que o roteiro correspondente contém o nome real do arquivo.
