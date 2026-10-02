# 02 — Validação convencional com 1 switch e 4 hosts

> **Arquivo pendente:** este roteiro ficará executável quando a topologia convencional final for adicionada. Nome recomendado: `topologia_convencional_1_switch_4_hosts.py`.

## Objetivo

Obter uma referência sem controlador SDN usando OVS em modo `standalone`, com os mesmos quatro hosts e endereços do teste 01.

## Passo a passo

### 1. Preparar a rodada

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh convencional-1s4h)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_convencional_1_switch_4_hosts.py"
```

### 2. Iniciar a topologia — sem Ryu

```bash
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 3. Confirmar o modo convencional

```text
mininet> sh ovs-vsctl get-fail-mode s1
mininet> sh ovs-vsctl get bridge s1 stp_enable
mininet> sh ovs-vsctl get bridge s1 rstp_enable
```

Registre `standalone`, STP desativado e RSTP desativado. Com apenas um switch, não há enlace redundante que gere loop.

### 4. Limpar vizinhança e capturar ARP

```text
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 timeout 15 tcpdump -n -e -i h1-eth0 arp -w "$PASTA_RESULTADO/arp-h1.pcap" &
mininet> h1 ping -c 20 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
mininet> h3 ping -c 20 10.0.0.1 | tee "$PASTA_RESULTADO/ping-h3-h1.txt"
mininet> pingall
```

### 5. Registrar tabelas do OVS

```text
mininet> sh ovs-appctl fdb/show s1 > "$PASTA_RESULTADO/fdb-s1.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-s1.txt"
mininet> sh tcpdump -nn -e -r "$PASTA_RESULTADO/arp-h1.pcap" > "$PASTA_RESULTADO/arp-h1.txt"
```

## Comparação com o teste 01

Compare:

- RTT do primeiro pacote e RTT médio;
- perda de pacotes;
- quantidade e direção dos quadros ARP;
- aprendizado tradicional do OVS contra os fluxos definidos pelo controlador;
- parâmetros idênticos de host, enlace e quantidade de pings.

Não atribua uma diferença pequena de RTT à arquitetura sem repetir rodadas e considerar variação do host/VM.

## Encerramento

Saia da CLI e execute:

```bash
./utilitarios/limpar-mininet.sh
```
