# ARP Proxy em Redes Definidas por Software

Repositório de apoio ao Trabalho de Conclusão de Curso **“ARP Proxy em Redes Definidas por Software: controle da resolução ARP em topologias redundantes”**, de Jean Pietro Oliveira da Silva e Guilherme Coelho Araujo, desenvolvido no curso de Tecnologia em Redes de Computadores do IFSULDEMINAS — Campus Inconfidentes.

O projeto utiliza **Ryu**, **OpenFlow 1.3**, **Open vSwitch** e **Mininet** para controlar a resolução ARP em topologias Ethernet com caminhos redundantes. O objetivo principal é reduzir a propagação indiscriminada de solicitações ARP nos enlaces internos e manter os caminhos físicos disponíveis para decisões programáveis do controlador.

> **Estado do projeto:** os controladores v3.6 e v3.7, as topologias de um switch, dois switches, anel e malha completa K4 estão incluídos. A máquina virtual foi enviada em partes para uma GitHub Release ainda em rascunho; sua publicação, identificação por tag e verificação final permanecem pendentes.

## O que a aplicação faz

1. Aprende o endereço IPv4, MAC, DPID e porta dos hosts.
2. Identifica portas de borda e enlaces entre switches por meio da descoberta de topologia do Ryu.
3. Responde diretamente a uma solicitação ARP quando o destino já é conhecido.
4. Quando o destino é desconhecido, encaminha a descoberta somente às portas de borda elegíveis.
5. Calcula um caminho funcional por busca em largura (BFS) e instala fluxos IPv4 nos switches.
6. Na v3.7, detecta falhas de enlace, remove fluxos afetados e calcula um caminho alternativo.

O termo **ARP Proxy** descreve o mecanismo centralizado desenvolvido no trabalho. Ele não corresponde integralmente ao Proxy ARP clássico da RFC 1027: os hosts permanecem na mesma rede IPv4 e a resposta utiliza o endereço MAC real do destino conhecido.

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| [`controller/`](controller/) | Versões do controlador Ryu |
| [`topologies/`](topologies/) | Topologias Mininet usadas nos ensaios |
| [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) | Passo a passo completo de todos os testes |
| [`docs/OVA_RELEASE_CHECKLIST.md`](docs/OVA_RELEASE_CHECKLIST.md) | Checklist para preparar e publicar a VM |
| [`docs/development/`](docs/development/) | Documentos históricos do desenvolvimento |
| [`docs/references/`](docs/references/) | Materiais acadêmicos utilizados como referência |
| [`scripts/`](scripts/) | Verificação, execução, limpeza e preparação da OVA |
| [`vm/`](vm/) | Importação, integridade e publicação da máquina virtual |

## Controladores

| Arquivo | Finalidade |
|---|---|
| `controller/arp_proxy_v3.py` | Registro histórico da versão inicial |
| `controller/arp_proxy_v3_5.py` | Ajustes de descoberta de portas de borda |
| `controller/arp_proxy_v3_6.py` | Versão consolidada para contenção ARP e conectividade |
| `controller/arp_proxy_v3_7.py` | Versão com detecção de falha e recomposição de caminhos |

Para os ensaios finais de redundância e failover, utilize a **v3.7**. Para reproduzir especificamente os ensaios de contenção ARP descritos com a versão consolidada anterior, utilize a **v3.6**.

## Cenários disponíveis

| Cenário | Arquivo de topologia |
|---|---|
| SDN, 1 switch e 4 hosts | `topologia_arp_proxy_v3.py` |
| Convencional, 1 switch e 4 hosts | `topologia_convencional_v3.py` |
| SDN, 2 switches e 4 hosts | `topologia_arp_proxy_2s.py` |
| Convencional, 2 switches e 4 hosts | `topologia_convencional_2s.py` |
| SDN, anel com 3 switches e 6 hosts | `topologia_arp_proxy_anel_3s_6h.py` |
| Anel sem STP/RSTP | `topologia_convencional_anel_3s_6h_sem_stp.py` |
| Anel com STP | `topologia_convencional_anel_3s_6h_stp.py` |
| Anel com RSTP | `topologia_convencional_anel_3s_6h_rstp.py` |
| Malha K4 com RSTP | `topologia_malha_rstp.py` |
| Malha K4 com SDN e ARP Proxy v3.7 | `topologia_malha_arp_proxy_v37.py` |

Consulte [`topologies/README.md`](topologies/README.md) para a associação entre controladores, topologias e objetivos de cada ensaio.

## Ambiente utilizado

O ambiente registrado no TCC utilizou:

| Componente | Versão registrada |
|---|---|
| Python | 3.8.5 |
| Ryu | 4.34 |
| Mininet | 2.6 |
| Open vSwitch | 2.13.1 |
| tcpdump | 4.9.3 |
| iPerf | 2.0.13 |
| Git | 2.25.1 |

Versões próximas podem funcionar, mas devem ser registradas para que os resultados sejam comparáveis.

## Execução rápida

Clone o repositório e verifique o ambiente:

```bash
git clone https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN.git
cd Redund-ncia-L2-em-redes-SDN
./scripts/preflight.sh
sudo mn -c
```

Para iniciar o anel SDN com a v3.7, abra dois terminais.

Terminal 1 — controlador:

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py
```

Terminal 2 — topologia:

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_anel_3s_6h.py
```

No Mininet:

```text
mininet> net
mininet> links
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

Ao terminar:

```text
mininet> exit
```

```bash
./scripts/cleanup-mininet.sh
```

As topologias SDN usam as portas OpenFlow 6633 ou 6653. O Ryu 4.34, quando iniciado sem forçar uma porta, mantém compatibilidade com ambas. O script de execução não altera essa configuração.

## Reprodução dos testes

O roteiro completo está em [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) e contém:

- preparação e registro do ambiente;
- validação inicial com um switch;
- comparação linear com dois switches;
- anel convencional sem STP/RSTP;
- anel com STP;
- anel com RSTP;
- anel SDN com contenção ARP;
- failover da v3.7;
- comparação de alta frequência a 5 ms;
- malha K4, iPerf paralelo e failover;
- comandos para salvar fluxos, capturas e resultados.

## Síntese dos resultados registrados

- Na topologia linear, não foi observado ARP no enlace interswitch durante o ensaio consolidado com a v3.6; no cenário convencional, o broadcast ARP atravessou o enlace.
- No anel convencional sem STP/RSTP, foram observados flooding, aumento de processamento e perda de conectividade.
- STP e RSTP estabilizaram o anel por meio de uma árvore lógica, mantendo parte da redundância fora do encaminhamento normal.
- No ensaio pareado de 5 ms no anel, o RSTP perdeu 2 de 3743 pacotes e o SDN v3.7 perdeu 4 de 3743 pacotes. O RTT foi tratado somente como métrica complementar.
- Na malha K4, o RSTP deixou 3 dos 6 enlaces interswitch em estado alternate/discarding. No cenário SDN, os seis enlaces permaneceram disponíveis ao controlador.
- No iPerf paralelo da execução registrada, o SDN utilizou caminhos diretos distintos e atingiu 22,70 Mbit/s agregados. Esse valor descreve uma execução específica em ambiente emulado, não uma garantia geral de desempenho.

O projeto **não implementa balanceamento de carga orientado por utilização**. O BFS seleciona caminhos funcionais; a preservação dos enlaces cria uma base para futuras políticas de engenharia de tráfego ou multipath.

## Máquina virtual

A máquina virtual não deve ser adicionada a um commit comum. Ela é distribuída pela página de [Releases](https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN/releases), em partes menores que o limite individual do GitHub.

As instruções para baixar, verificar, extrair e importar no VirtualBox estão em [`vm/README.md`](vm/README.md). A OVA deve permanecer acompanhada de SHA-256 para confirmar que o arquivo baixado é idêntico ao original.

## Limitações

- Avaliação realizada em ambiente emulado e em topologias de pequeno porte.
- Quantidade limitada de repetições em alguns ensaios.
- Endereçamento IPv4 estático.
- Tratamento específico de ARP; a aplicação não controla genericamente todo tráfego broadcast.
- Dependência do controlador e da sinalização OpenFlow para recomposição dos caminhos.
- DHCP redundante, Proxy ARP clássico entre sub-redes e políticas de balanceamento permanecem como trabalhos futuros independentes.

