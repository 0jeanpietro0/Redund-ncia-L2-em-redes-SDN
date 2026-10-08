# Controladores Ryu

Esta pasta contém a evolução do mecanismo de ARP Proxy desenvolvido no TCC.

| Arquivo | Papel no projeto |
|---|---|
| `arp_proxy_v3.py` | Versão histórica com grafo, BFS e instalação de fluxos IPv4 |
| `arp_proxy_v3_5.py` | Ajustes de descoberta e atualização das portas de borda |
| `arp_proxy_v3_6.py` | Versão consolidada para conectividade e contenção ARP |
| `arp_proxy_v3_7.py` | Versão final dos ensaios de falha, com recomposição de caminhos |

## Versão recomendada

Use a v3.7 para os ensaios finais:

```bash
ryu-manager controller/arp_proxy_v3_7.py --observe-links
```

Ou utilize o script auxiliar:

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py
```

Para reproduzir especificamente os ensaios consolidados de contenção ARP anteriores ao tratamento de falha:

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_6.py
```

## Evolução v3.6 → v3.7

A v3.6 reúne:

- descoberta dinâmica de switches ativos;
- identificação das portas de borda;
- tabela central de hosts com IP, MAC, DPID e porta;
- resposta direta para destino conhecido;
- descoberta de destino desconhecido somente em portas de borda elegíveis;
- cálculo BFS e instalação bidirecional de fluxos IPv4;
- controle de caminhos já instalados para evitar Flow-Mod repetido.

A v3.7 mantém essa base e acrescenta:

- registro da sequência de switches de cada caminho instalado;
- tratamento de `EventOFPPortStatus` e `EventLinkDelete`;
- remoção do enlace indisponível do grafo;
- identificação e limpeza dos fluxos afetados;
- novo cálculo BFS e instalação do caminho alternativo;
- reinserção do enlace no grafo por `EventLinkAdd`.

Quando um enlace retorna, os fluxos recuperados não são migrados automaticamente para o caminho anterior.

## Delimitação

O código trata ARP em uma rede IPv4 local com endereçamento estático. Ele não implementa Proxy ARP clássico entre sub-redes, DHCP, balanceamento de carga orientado por métricas ou controle genérico de todos os tipos de broadcast.
