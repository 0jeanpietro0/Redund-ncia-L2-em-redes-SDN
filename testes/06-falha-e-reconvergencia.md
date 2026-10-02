# 06 — Falha de enlace e reconvergência

> **Arquivos pendentes:** topologias em anel STP/RSTP, topologia SDN e controlador `v3.7` com tratamento de `EventOFPPortStatus`/`EventLinkDelete`.

## Objetivo

Comparar a continuidade e a recuperação após a queda do mesmo enlace nos cenários STP, RSTP e SDN.

## Protocolo comum

Em cada tecnologia:

- use 3 switches e 6 hosts no mesmo arranjo físico;
- selecione o enlace `s1-s2`, confirmando antes que ele participa do caminho ativo;
- envie 400 pacotes de `h1` para `h3`, um a cada 100 ms;
- mantenha 5 segundos de linha de base;
- derrube `s1-s2` e mantenha-o inativo até o fim do ping;
- restaure o enlace somente depois de salvar as evidências.

Não reutilize a mesma instância do Mininet entre as tecnologias.

## Parte A — STP

### 1. Iniciar o cenário

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh failover-stp-100ms)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_stp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 2. Esperar STP estabilizar e registrar estados

```text
mininet> sh ovs-appctl stp/show s1 > "$PASTA_RESULTADO/stp-s1-antes.txt"
mininet> sh ovs-appctl stp/show s2 > "$PASTA_RESULTADO/stp-s2-antes.txt"
mininet> sh ovs-appctl stp/show s3 > "$PASTA_RESULTADO/stp-s3-antes.txt"
mininet> h1 ping -c 5 10.0.0.3
```

Confirme que `s1-s2` está no caminho ativo. Se não estiver, escolha um enlace ativo e use exatamente o mesmo enlace nas três tecnologias.

### 3. Executar a falha

```text
mininet> h1 env LC_ALL=C ping -D -i 0.1 -c 400 10.0.0.3 > "$PASTA_RESULTADO/ping.txt" 2>&1 &
mininet> sh sleep 5
mininet> sh date --iso-8601=ns > "$PASTA_RESULTADO/instante-da-falha.txt"
mininet> link s1 s2 down
mininet> sh sleep 36
mininet> sh ovs-appctl stp/show s1 > "$PASTA_RESULTADO/stp-s1-depois.txt"
mininet> sh ovs-appctl stp/show s2 > "$PASTA_RESULTADO/stp-s2-depois.txt"
mininet> sh ovs-appctl stp/show s3 > "$PASTA_RESULTADO/stp-s3-depois.txt"
mininet> link s1 s2 up
```

## Parte B — RSTP

Repita em uma rede limpa:

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh failover-rstp-100ms)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_rstp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

Na CLI:

```text
mininet> h1 ping -c 5 10.0.0.3
mininet> h1 env LC_ALL=C ping -D -i 0.1 -c 400 10.0.0.3 > "$PASTA_RESULTADO/ping.txt" 2>&1 &
mininet> sh sleep 5
mininet> sh date --iso-8601=ns > "$PASTA_RESULTADO/instante-da-falha.txt"
mininet> link s1 s2 down
mininet> sh sleep 36
mininet> sh ovs-vsctl get bridge s1 rstp_status > "$PASTA_RESULTADO/rstp-s1-depois.txt"
mininet> sh ovs-vsctl get bridge s2 rstp_status > "$PASTA_RESULTADO/rstp-s2-depois.txt"
mininet> sh ovs-vsctl get bridge s3 rstp_status > "$PASTA_RESULTADO/rstp-s3-depois.txt"
mininet> link s1 s2 up
```

## Parte C — SDN v3.7

### 1. Iniciar controlador e topologia

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh failover-sdn-v3_7-100ms)"
export CONTROLADOR="reproducao/codigo/controlador/arp_proxy_v3_7.py"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_sdn.py"
```

Terminal 1:

```bash
./utilitarios/executar-controlador.sh 2>&1 \
  | tee "$PASTA_RESULTADO/controlador.log"
```

Terminal 2:

```bash
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 2. Aquecer o caminho e executar a falha

```text
mininet> h1 ping -c 5 10.0.0.3
mininet> h1 env LC_ALL=C ping -D -i 0.1 -c 400 10.0.0.3 > "$PASTA_RESULTADO/ping.txt" 2>&1 &
mininet> sh sleep 5
mininet> sh date --iso-8601=ns > "$PASTA_RESULTADO/instante-da-falha.txt"
mininet> link s1 s2 down
mininet> sh sleep 36
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-s1-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2 > "$PASTA_RESULTADO/fluxos-s2-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3 > "$PASTA_RESULTADO/fluxos-s3-depois.txt"
mininet> link s1 s2 up
```

No log do controlador, procure detecção do enlace removido, limpeza dos fluxos antigos, cálculo do caminho alternativo e instalação dos novos fluxos.

## Cálculo do maior intervalo entre respostas

Após cada rodada:

```bash
awk '/bytes from/ {
  tempo=$1; gsub(/^\[/, "", tempo); gsub(/\]$/, "", tempo)
  if (anterior != "") {
    intervalo=tempo-anterior
    if (intervalo > maior) maior=intervalo
  }
  anterior=tempo
}
END { printf "Maior intervalo entre respostas: %.6f s\n", maior }' \
  "$PASTA_RESULTADO/ping.txt" \
  | tee "$PASTA_RESULTADO/maior-intervalo.txt"
```

Esse valor aproxima a janela de indisponibilidade. Para chamá-lo de tempo de reconvergência, relacione-o ao instante registrado da falha e ao primeiro `echo reply` após a recuperação.

## Métricas

| Métrica | STP | RSTP | SDN v3.7 |
|---|---:|---:|---:|
| Pacotes transmitidos | preencher | preencher | preencher |
| Pacotes recebidos | preencher | preencher | preencher |
| Perda (%) | preencher | preencher | preencher |
| Maior intervalo sem resposta (s) | preencher | preencher | preencher |
| RTT médio (ms) | preencher | preencher | preencher |
| RTT máximo (ms) | preencher | preencher | preencher |

Interprete somente depois de conferir se o enlace derrubado, o momento da falha e os parâmetros foram equivalentes.
