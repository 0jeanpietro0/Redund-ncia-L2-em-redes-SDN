# Roteiro completo de reprodução e testes

Este documento reúne os procedimentos usados no TCC **“ARP Proxy em Redes Definidas por Software: controle da resolução ARP em topologias redundantes”**. Todos os comandos partem da raiz do repositório.

## 1. Regras gerais

- Execute apenas uma topologia Mininet por vez.
- Use endereçamento IPv4 estático, como definido nos scripts.
- Inicie o controlador antes das topologias SDN.
- Use `--observe-links` nos cenários com múltiplos switches.
- Antes de cada rodada, execute `sudo mn -c`.
- Utilize o mesmo par de hosts, quantidade de pacotes e instante relativo de falha ao comparar tecnologias.
- Salve comandos, logs, capturas, fluxos e resultados antes de interpretar os dados.
- Trate RTT como métrica complementar; os focos principais são propagação ARP, disponibilidade dos enlaces, continuidade após falha e uso da redundância.
- Descreva as conclusões como válidas **nos cenários testados**, sem generalização para qualquer rede.

O ensaio sem STP/RSTP pode gerar um loop de camada 2. Execute-o somente na máquina virtual ou em outro ambiente isolado, durante poucos segundos e com capturas limitadas.

## 2. Preparação comum

### 2.1 Obter o projeto

```bash
git clone https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN.git
cd Redund-ncia-L2-em-redes-SDN
git status
git rev-parse HEAD
```

### 2.2 Verificar o ambiente

```bash
./scripts/preflight.sh
./scripts/collect-environment-info.sh
```

O ambiente documentado no TCC utilizou Python 3.8.5, Ryu 4.34, Mininet 2.6, Open vSwitch 2.13.1, tcpdump 4.9.3 e iPerf 2.0.13.

### 2.3 Criar uma pasta local para evidências

O repositório não versiona resultados brutos. Crie uma pasta ignorada pelo Git:

```bash
cenario="$(date +%F-%H%M)-nome-do-cenario"
mkdir -p "resultados-locais/$cenario"
./scripts/collect-environment-info.sh | tee "resultados-locais/$cenario/ambiente.txt"
git rev-parse HEAD | tee "resultados-locais/$cenario/commit.txt"
```

Substitua `nome-do-cenario` por uma identificação curta, como `anel-sdn-v37`.

### 2.4 Limpar execuções anteriores

```bash
./scripts/cleanup-mininet.sh
```

Se o script não estiver executável:

```bash
chmod +x scripts/*.sh
```

### 2.5 Conferências dentro do Mininet

Depois de iniciar uma topologia, execute:

```text
mininet> net
mininet> dump
mininet> links
mininet> sh ovs-vsctl show
mininet> sh ovs-ofctl -O OpenFlow13 show s1
```

Repita o último comando para `s2`, `s3` e `s4` quando existirem. O comando `links` e a saída de `ovs-ofctl show` são as fontes para identificar as interfaces interswitch antes de iniciar o `tcpdump`.

## 3. Teste 1 — cenário inicial SDN, 1 switch e 4 hosts

### Objetivo

Validar conexão com o controlador, aprendizado dos hosts, resposta ARP, conectividade e instalação de fluxos antes da introdução de enlaces interswitch.

### Terminal 1 — controlador v3.6

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_6.py 2>&1 | tee resultados-locais/controlador-1s-v36.log
```

### Terminal 2 — topologia

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_v3.py
```

### CLI do Mininet

```text
mininet> pingall
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 ping -c 20 10.0.0.3
mininet> h3 ping -c 20 10.0.0.1
mininet> h1 ip neigh show
mininet> h3 ip neigh show
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

### Registrar

- quatro hosts conectados;
- `pingall` sem perda não explicada;
- associação IP/MAC aprendida;
- primeiro RTT separado dos demais;
- fluxos IPv4 nos dois sentidos;
- mensagens “Flow já instalado”, quando aplicável.

### Referência do TCC

Na execução consolidada com a v3.6, `h1 → h3` respondeu 20/20 e o `pingall` respondeu 12/12. Esses valores são referência histórica, não um critério universal para qualquer ambiente.

## 4. Teste 2 — cenário inicial convencional, 1 switch e 4 hosts

### Objetivo

Criar uma referência equivalente sem controlador SDN.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_convencional_v3.py
```

No Mininet:

```text
mininet> pingall
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 ping -c 20 10.0.0.3
mininet> h3 ping -c 20 10.0.0.1
mininet> h1 ip neigh show
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

Compare somente execuções com o mesmo número de pacotes. Esse cenário valida conectividade, mas não testa contenção ARP em enlaces internos porque possui apenas um switch.

## 5. Teste 3 — topologia linear SDN, 2 switches e 4 hosts

### Objetivo

Verificar se a descoberta ARP permanece fora do enlace entre os switches.

### Terminal 1

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_6.py 2>&1 | tee resultados-locais/controlador-2s-v36.log
```

### Terminal 2

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_2s.py
```

### Identificar o enlace

No Mininet:

```text
mininet> links
mininet> sh ovs-ofctl -O OpenFlow13 show s1
mininet> sh ovs-ofctl -O OpenFlow13 show s2
```

No arquivo atual, o enlace normalmente aparece como `s1-eth3 ↔ s2-eth1`. Confirme antes de capturar; não presuma que os nomes serão iguais após qualquer alteração na topologia.

### Terminais 3 e 4 — capturas

```bash
sudo timeout 30 tcpdump -nn -e -i s1-eth3 arp | tee resultados-locais/arp-s1-eth3.txt
```

```bash
sudo timeout 30 tcpdump -nn -e -i s2-eth1 arp | tee resultados-locais/arp-s2-eth1.txt
```

### Gerar nova descoberta

```text
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 ping -c 20 10.0.0.3
mininet> pingall
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2
```

### Resultado esperado

Conectividade entre hosts de switches diferentes, com ausência de quadros ARP nas interfaces internas durante a descoberta observada. O filtro `arp` não captura LLDP; portanto, ausência de ARP não significa ausência de tráfego de controle.

## 6. Teste 4 — topologia linear convencional, 2 switches e 4 hosts

### Objetivo

Observar a participação do enlace interswitch no domínio de broadcast convencional.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_convencional_2s.py
```

Confirme as interfaces com `links` e abra capturas equivalentes às do teste anterior:

```bash
sudo timeout 30 tcpdump -nn -e -i s1-eth3 arp | tee resultados-locais/arp-conv-s1-eth3.txt
sudo timeout 30 tcpdump -nn -e -i s2-eth1 arp | tee resultados-locais/arp-conv-s2-eth1.txt
```

No Mininet:

```text
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 ping -c 20 10.0.0.3
mininet> pingall
```

O ARP broadcast deve atravessar o enlace. Isso demonstra a extensão do domínio de broadcast; não caracteriza tempestade porque existe apenas um caminho entre os switches.

## 7. Teste 5 — anel convencional sem STP/RSTP

### Objetivo

Demonstrar, de forma curta e controlada, o comportamento de um ciclo de camada 2 sem mecanismo de prevenção de loops.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_convencional_anel_3s_6h_sem_stp.py
```

No Mininet:

```text
mininet> links
mininet> sh ovs-vsctl get bridge s1 stp_enable
mininet> sh ovs-vsctl get bridge s1 rstp_enable
mininet> sh ovs-vsctl get bridge s2 stp_enable
mininet> sh ovs-vsctl get bridge s2 rstp_enable
mininet> sh ovs-vsctl get bridge s3 stp_enable
mininet> sh ovs-vsctl get bridge s3 rstp_enable
```

Identifique uma interface de cada enlace interno. Em terminais separados, limite tempo e quantidade de pacotes:

```bash
sudo timeout 6 tcpdump -nn -e -i INTERFACE_1 -c 5000 arp
sudo timeout 6 tcpdump -nn -e -i INTERFACE_2 -c 5000 arp
sudo timeout 6 tcpdump -nn -e -i INTERFACE_3 -c 5000 arp
```

Gere apenas uma tentativa:

```text
mininet> h1 ip neigh flush all
mininet> h1 ping -c 1 10.0.0.3
```

Se ocorrer tráfego intenso, lentidão da CLI, elevação de CPU ou perda de conectividade, encerre imediatamente:

```bash
sudo mn -c
```

Não transforme esse ensaio em benchmark de tempestade. A finalidade é registrar a instabilidade causada pelo ciclo L2 sem controle.

## 8. Teste 6 — anel convencional com STP

### Objetivo

Observar a estabilização da topologia por formação de uma árvore lógica e bloqueio de uma porta redundante.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_convencional_anel_3s_6h_stp.py
```

No Mininet:

```text
mininet> sh ovs-vsctl get bridge s1 stp_enable
mininet> sh ovs-vsctl get bridge s2 stp_enable
mininet> sh ovs-vsctl get bridge s3 stp_enable
mininet> sh ovs-appctl stp/show s1
mininet> sh ovs-appctl stp/show s2
mininet> sh ovs-appctl stp/show s3
```

Espere até os estados pararem de mudar. Registre:

- switch raiz;
- root ports;
- designated ports;
- porta alternate/blocking;
- tempo aproximado até estabilidade.

Depois:

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3
```

Se capturar uma porta bloqueada, correlacione a captura com o estado STP. Receber fisicamente um quadro na interface não significa que o switch o encaminhou.

## 9. Teste 7 — anel convencional com RSTP

### Objetivo

Usar o RSTP como referência convencional de convergência mais rápida.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_convencional_anel_3s_6h_rstp.py
```

No Mininet:

```text
mininet> sh ovs-vsctl get bridge s1 rstp_enable
mininet> sh ovs-vsctl get bridge s2 rstp_enable
mininet> sh ovs-vsctl get bridge s3 rstp_enable
mininet> sh ovs-vsctl get bridge s1 rstp_status
mininet> sh ovs-vsctl get bridge s2 rstp_status
mininet> sh ovs-vsctl get bridge s3 rstp_status
mininet> links
```

Consulte cada porta interswitch, substituindo o nome:

```text
mininet> sh ovs-vsctl get port s1-ethX rstp_status
```

Valide conectividade:

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3
```

### Failover RSTP a 100 ms

```text
mininet> h1 ping -D -i 0.1 10.0.0.3 > /tmp/ping-rstp-100ms.txt 2>&1 &
mininet> sh sleep 5
mininet> link s1 s2 down
mininet> sh sleep 15
mininet> h1 pkill -INT ping
mininet> sh tail -n 10 /tmp/ping-rstp-100ms.txt
mininet> link s1 s2 up
```

Registre a última resposta antes da falha, a primeira após a recuperação, a quantidade perdida e as mudanças de estado das portas.

## 10. Teste 8 — anel SDN com ARP Proxy v3.6

### Objetivo

Validar conectividade e contenção ARP com os três enlaces do anel disponíveis ao plano de controle.

### Terminal 1

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_6.py 2>&1 | tee resultados-locais/controlador-anel-v36.log
```

### Terminal 2

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_anel_3s_6h.py
```

Confirme no log do Ryu a descoberta de três switches e três enlaces. No Mininet:

```text
mininet> links
mininet> h1 ip neigh flush all
mininet> h2 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h4 ip neigh flush all
mininet> h5 ip neigh flush all
mininet> h6 ip neigh flush all
```

Mapeie uma interface de cada enlace e abra capturas em terminais externos:

```bash
sudo timeout 40 tcpdump -nn -e -i INTERFACE_1 arp
sudo timeout 40 tcpdump -nn -e -i INTERFACE_2 arp
sudo timeout 40 tcpdump -nn -e -i INTERFACE_3 arp
```

Gere tráfego:

```text
mininet> h1 ping -c 20 10.0.0.3
mininet> pingall
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3
```

Registre conectividade, ARP observado em cada enlace e caminhos instalados. Ausência de ARP no filtro não implica ausência de LLDP.

## 11. Teste 9 — failover SDN com ARP Proxy v3.7

### Objetivo

Verificar detecção de falha, remoção de fluxos afetados, recálculo BFS e instalação de caminho alternativo.

### Terminal 1

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py 2>&1 | tee resultados-locais/controlador-anel-v37.log
```

### Terminal 2

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_anel_3s_6h.py
```

No Mininet:

```text
mininet> h1 ping -c 5 10.0.0.3
mininet> h1 ping -D -i 0.1 10.0.0.3 > /tmp/ping-sdn-100ms.txt 2>&1 &
mininet> sh sleep 5
mininet> link s1 s2 down
mininet> sh sleep 15
mininet> h1 pkill -INT ping
mininet> sh tail -n 10 /tmp/ping-sdn-100ms.txt
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3
mininet> link s1 s2 up
```

No log do controlador, procure eventos de porta/enlace indisponível, invalidação do caminho e instalação da alternativa. Na execução histórica registrada no TCC, houve 139/139 respostas no ensaio a 100 ms; uma nova execução pode variar.

## 12. Teste 10 — comparação de failover a 5 ms no anel

### Objetivo

Comparar RSTP e SDN v3.7 com os mesmos parâmetros.

Repita o procedimento uma vez com `topologia_convencional_anel_3s_6h_rstp.py` e outra com `topologia_arp_proxy_anel_3s_6h.py` junto ao controlador v3.7.

Em ambas as execuções:

```text
mininet> h1 ping -D -i 0.005 -c 3743 10.0.0.3 > /tmp/ping-anel-5ms.txt 2>&1 &
mininet> sh sleep 5
mininet> link s1 s2 down
mininet> sh sleep 15
mininet> sh tail -n 10 /tmp/ping-anel-5ms.txt
mininet> link s1 s2 up
```

Use o mesmo atraso antes da queda. Registre:

- pacotes transmitidos, recebidos e perdidos;
- percentual de perda;
- maior sequência de perdas consecutivas;
- instante da última resposta antes da falha;
- instante da primeira resposta após a recuperação;
- RTT médio apenas como dado complementar.

### Referência do TCC

| Cenário | Transmitidos | Recebidos | Perdidos | Perda |
|---|---:|---:|---:|---:|
| SDN + ARP Proxy v3.7 | 3743 | 3739 | 4 | 0,106866% |
| Convencional + RSTP | 3743 | 3741 | 2 | 0,0534331% |

Esses dados correspondem a uma comparação preliminar específica, não a uma garantia estatística.

## 13. Teste 11 — malha completa K4 com RSTP

### Objetivo

Medir quantos enlaces permanecem no encaminhamento normal e observar a concentração dos fluxos na árvore ativa.

```bash
./scripts/cleanup-mininet.sh
./scripts/run-topology.sh topologies/topologia_malha_rstp.py
```

No Mininet:

```text
mininet> links
mininet> pingall
mininet> sh ovs-vsctl get bridge s1 rstp_status
mininet> sh ovs-vsctl get bridge s2 rstp_status
mininet> sh ovs-vsctl get bridge s3 rstp_status
mininet> sh ovs-vsctl get bridge s4 rstp_status
```

Para cada uma das seis ligações interswitch, consulte os dois lados:

```text
mininet> sh ovs-vsctl get port INTERFACE rstp_status
```

No ensaio consolidado, `s1` atuou como raiz e os enlaces `s2-s3`, `s2-s4` e `s3-s4` ficaram alternate/discarding. Confirme o estado da nova execução em vez de assumir que será idêntico.

Antes do iPerf, salve os contadores:

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s4
```

## 14. Teste 12 — malha completa K4 com SDN e ARP Proxy v3.7

### Terminal 1

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py 2>&1 | tee resultados-locais/controlador-malha-v37.log
```

### Terminal 2

```bash
./scripts/run-topology.sh topologies/topologia_malha_arp_proxy_v37.py
```

Confirme quatro switches e seis enlaces no log do Ryu. No Mininet:

```text
mininet> links
mininet> pingall
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s4
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s4
```

Os enlaces host-switch estão configurados em 100 Mbit/s e 0,2 ms. Os seis enlaces interswitch usam 10 Mbit/s e 1 ms.

## 15. Teste 13 — iPerf paralelo na malha K4

Execute exatamente o mesmo conjunto primeiro no RSTP e depois no SDN:

```text
mininet> h5 iperf -s -p 5001 > /tmp/servidor-h5.txt 2>&1 &
mininet> h7 iperf -s -p 5002 > /tmp/servidor-h7.txt 2>&1 &
mininet> sh sleep 1
mininet> h3 iperf -c 10.0.0.5 -p 5001 -t 20 -i 1 > /tmp/iperf-h3-h5.txt 2>&1 &
mininet> h4 iperf -c 10.0.0.7 -p 5002 -t 20 -i 1 > /tmp/iperf-h4-h7.txt 2>&1 &
mininet> sh sleep 22
mininet> sh tail -n 5 /tmp/iperf-h3-h5.txt
mininet> sh tail -n 5 /tmp/iperf-h4-h7.txt
```

Depois, consulte novamente `dump-ports` nos quatro switches. Registre:

- throughput de cada fluxo;
- throughput agregado;
- enlaces percorridos;
- variação dos contadores antes e depois do teste;
- estados RSTP ou fluxos OpenFlow que sustentam a interpretação.

Na execução registrada, o SDN utilizou os caminhos `h3-s2-s3-h5` e `h4-s2-s4-h7`, com 11,67 e 11,03 Mbit/s, totalizando 22,70 Mbit/s. Não descreva isso como balanceamento de carga automático: o BFS não escolhe caminhos com base em utilização, atraso ou largura de banda.

## 16. Teste 14 — failover na malha K4

### Objetivo

Comparar a reação à mesma falha física na malha RSTP e na malha SDN.

Em ambas as tecnologias, use 2000 sondagens e o mesmo atraso relativo:

```text
mininet> h1 ping -D -i 0.005 -c 2000 10.0.0.3 > /tmp/ping-malha-5ms.txt 2>&1 &
mininet> sh sleep 5
mininet> link s1 s2 down
mininet> sh sleep 12
mininet> sh tail -n 10 /tmp/ping-malha-5ms.txt
mininet> link s1 s2 up
```

O valor de cinco segundos deve permanecer igual nas duas rodadas. Registre perdas, janela de interrupção, estados RSTP, mensagens do controlador e caminho após a recuperação.

## 17. Encerramento de cada rodada

Dentro do Mininet:

```text
mininet> exit
```

No terminal:

```bash
./scripts/cleanup-mininet.sh
```

Confirme que não ficaram processos antigos:

```bash
pgrep -af 'ryu-manager|mininet|iperf|tcpdump' || true
```

Finalize manualmente somente os processos pertencentes ao ensaio atual.

## 18. Modelo mínimo de registro

Para cada execução, anote:

```text
Data e hora:
Commit do Git:
Controlador:
Topologia:
Comandos executados:
Par de hosts:
Quantidade e intervalo dos pacotes:
Enlace derrubado e instante relativo:
Capturas realizadas:
Fluxos/estados observados:
Resultado:
Pequena conclusão:
Limitações:
Melhorias ou nova repetição necessária:
```

## 19. Critérios de interpretação

- **Contenção ARP:** verificar quadros efetivamente observados nas interfaces internas; não inferir somente pelo sucesso do ping.
- **Redundância lógica:** contar enlaces disponíveis para encaminhamento no estado estável, diferenciando enlace físico de porta bloqueada.
- **Failover:** comparar perdas e janela de interrupção com os mesmos parâmetros.
- **Throughput:** usar valores de testes com mesma duração e configuração de enlace.
- **Latência:** não usar RTT isoladamente para declarar superioridade.
- **Overhead:** considerar Packet-In, Packet-Out, LLDP, Flow-Mod e processamento do controlador.
- **Escopo:** os resultados foram obtidos em Mininet/Open vSwitch com IPv4 estático e não demonstram substituição universal de STP/RSTP.

## 20. Sequência recomendada para uma reprodução completa

1. Testes 1 e 2 — validar o ambiente básico.
2. Testes 3 e 4 — comparar propagação ARP no enlace linear.
3. Teste 5 — demonstrar de forma controlada o ciclo L2 sem proteção.
4. Testes 6 e 7 — registrar STP e RSTP.
5. Testes 8, 9 e 10 — validar o anel SDN, failover e comparação pareada.
6. Testes 11 a 14 — avaliar disponibilidade dos enlaces, iPerf paralelo e failover na malha K4.
7. Consolidar resultados sem misturar execuções com parâmetros diferentes.
