# 08 — Malha completa K4 com 4 switches e 8 hosts

> **Arquivos pendentes:** topologias finais K4 para RSTP e SDN e o controlador usado nessa etapa.

## Objetivo

Avaliar uma topologia densa na qual os 4 switches possuem ligação direta entre si, totalizando 6 enlaces inter-switch. O teste observa quantos caminhos o RSTP retira do encaminhamento normal, como os fluxos concorrentes utilizam a capacidade e como o cenário SDN mantém a malha disponível para caminhos controlados.

## Parâmetros da topologia

| Item | Configuração |
|---|---|
| Switches | `s1`, `s2`, `s3`, `s4` |
| Hosts | `h1` a `h8`, dois por switch |
| Enlaces inter-switch | 6, formando K4 |
| Host ↔ switch | 100 Mbit/s e 0,2 ms |
| Switch ↔ switch | 10 Mbit/s e 1 ms |
| Fluxos concorrentes | `h3 → h5` e `h4 → h7` |

Confirme esses valores no código antes da execução.

## Parte A — K4 com RSTP

### 1. Iniciar

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh k4-rstp)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_k4_8_hosts_rstp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 2. Validar a malha e o RSTP

```text
mininet> net
mininet> links
mininet> dump
mininet> sh ovs-vsctl show > "$PASTA_RESULTADO/ovs-vsctl-show.txt"
mininet> sh ovs-vsctl get bridge s1 rstp_status > "$PASTA_RESULTADO/rstp-s1.txt"
mininet> sh ovs-vsctl get bridge s2 rstp_status > "$PASTA_RESULTADO/rstp-s2.txt"
mininet> sh ovs-vsctl get bridge s3 rstp_status > "$PASTA_RESULTADO/rstp-s3.txt"
mininet> sh ovs-vsctl get bridge s4 rstp_status > "$PASTA_RESULTADO/rstp-s4.txt"
```

Use `ovs-vsctl get port NOME_DA_PORTA rstp_status` em todas as 12 extremidades dos enlaces inter-switch. Conte cada enlace apenas uma vez.

### 3. Testar conectividade

```text
mininet> pingall
mininet> h3 ping -c 20 10.0.0.5 | tee "$PASTA_RESULTADO/ping-h3-h5.txt"
mininet> h4 ping -c 20 10.0.0.7 | tee "$PASTA_RESULTADO/ping-h4-h7.txt"
```

### 4. Registrar contadores antes do `iperf`

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1 > "$PASTA_RESULTADO/portas-s1-antes.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2 > "$PASTA_RESULTADO/portas-s2-antes.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3 > "$PASTA_RESULTADO/portas-s3-antes.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s4 > "$PASTA_RESULTADO/portas-s4-antes.txt"
```

### 5. Executar dois fluxos paralelos

```text
mininet> h5 iperf -s -p 5001 > "$PASTA_RESULTADO/servidor-h5.txt" 2>&1 &
mininet> h7 iperf -s -p 5002 > "$PASTA_RESULTADO/servidor-h7.txt" 2>&1 &
mininet> sh sleep 1
mininet> h3 iperf -c 10.0.0.5 -p 5001 -t 20 -i 1 > "$PASTA_RESULTADO/iperf-h3-h5.txt" 2>&1 &
mininet> h4 iperf -c 10.0.0.7 -p 5002 -t 20 -i 1 > "$PASTA_RESULTADO/iperf-h4-h7.txt" 2>&1 &
mininet> sh sleep 22
```

### 6. Registrar contadores depois

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1 > "$PASTA_RESULTADO/portas-s1-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2 > "$PASTA_RESULTADO/portas-s2-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3 > "$PASTA_RESULTADO/portas-s3-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s4 > "$PASTA_RESULTADO/portas-s4-depois.txt"
mininet> h5 pkill -f 'iperf -s -p 5001'
mininet> h7 pkill -f 'iperf -s -p 5002'
```

## Parte B — K4 com SDN

Prepare uma nova rodada e use os nomes reais dos arquivos finais:

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh k4-sdn)"
export CONTROLADOR="reproducao/codigo/controlador/ARQUIVO_FINAL_DO_CONTROLADOR.py"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_k4_8_hosts_sdn.py"
```

Inicie o Ryu e a topologia. Depois:

1. confirme a descoberta dos 4 switches e dos 6 enlaces;
2. limpe as tabelas ARP dos hosts;
3. capture ARP em pelo menos uma interface de cada enlace interno;
4. execute `pingall` e os pings `h3→h5` e `h4→h7`;
5. repita os dois fluxos `iperf` simultâneos por 20 segundos;
6. salve os contadores de todas as portas antes e depois;
7. salve os fluxos OpenFlow de `s1` a `s4`;
8. identifique os caminhos realmente usados pelos dois fluxos.

Não descreva a utilização de caminhos diferentes como balanceamento de carga sem um algoritmo que distribua tráfego deliberadamente. O objetivo é observar caminhos programáveis e disponibilidade dos enlaces.

## Referência histórica do cenário RSTP

- `s1` atuou como bridge raiz;
- `s2-s3`, `s2-s4` e `s3-s4` ficaram em função Alternate/estado Discarding;
- 3 dos 6 enlaces inter-switch, ou 50%, ficaram fora do encaminhamento normal;
- throughput `h3→h5`: 6,6000 Mbit/s;
- throughput `h4→h7`: 4,7064 Mbit/s;
- agregado registrado: 11,3063 Mbit/s;
- os dois fluxos convergiram pelo enlace `s1-s2`, próximo do limite configurado.

Esses valores precisam ser associados aos logs brutos originais quando eles forem adicionados. Uma nova rodada pode variar.

## Comparação final

| Item | RSTP | SDN |
|---|---:|---:|
| Enlaces inter-switch físicos | 6 | 6 |
| Enlaces fora do encaminhamento normal | preencher | preencher |
| Throughput `h3→h5` | preencher | preencher |
| Throughput `h4→h7` | preencher | preencher |
| Throughput agregado | preencher | preencher |
| ARP observado nos enlaces internos | preencher | preencher |
| Caminhos efetivamente usados | preencher | preencher |

Finalize as duas rodadas com `./utilitarios/limpar-mininet.sh`.
