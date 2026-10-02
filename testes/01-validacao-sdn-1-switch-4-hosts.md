# 01 — Validação SDN com 1 switch e 4 hosts

Este é o único cenário integralmente executável com os arquivos atualmente disponíveis.

## Objetivo

Validar a conexão entre Ryu e OVS, o aprendizado IP/MAC/porta, o tratamento ARP, a conectividade IPv4 e a instalação de fluxos bidirecionais.

## Arquivos

```text
reproducao/codigo/controlador/arp_proxy_v3.py
reproducao/codigo/topologias/topologia_arp_proxy_v3.py
```

Hosts: `h1=10.0.0.1`, `h2=10.0.0.2`, `h3=10.0.0.3` e `h4=10.0.0.4`.

## Passo a passo

### 1. Preparar a rodada

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh sdn-1s4h-v3)"
```

### 2. Iniciar o controlador — Terminal 1

```bash
./utilitarios/executar-controlador.sh 2>&1 \
  | tee "$PASTA_RESULTADO/controlador.log"
```

### 3. Iniciar a topologia — Terminal 2

```bash
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

Confirme no log do controlador que o switch se conectou e teve as portas enumeradas.

### 4. Registrar o estado inicial

Na CLI do Mininet:

```text
mininet> net
mininet> dump
mininet> h1 ip neigh show
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-antes.txt"
```

### 5. Capturar a primeira descoberta

```text
mininet> h1 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h1 timeout 15 tcpdump -n -e -i h1-eth0 arp -w "$PASTA_RESULTADO/arp-h1.pcap" &
mininet> h1 ping -c 20 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
mininet> sh sleep 1
```

### 6. Testar o sentido inverso e todos os pares

```text
mininet> h3 ping -c 20 10.0.0.1 | tee "$PASTA_RESULTADO/ping-h3-h1.txt"
mininet> pingall
```

A saída do `pingall` ficará registrada em `topologia.log` pelo `tee` usado no Terminal 2.

### 7. Registrar vizinhança e fluxos

```text
mininet> h1 ip neigh show > "$PASTA_RESULTADO/vizinhanca-h1.txt"
mininet> h3 ip neigh show > "$PASTA_RESULTADO/vizinhanca-h3.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-depois.txt"
mininet> sh tcpdump -nn -e -r "$PASTA_RESULTADO/arp-h1.pcap" > "$PASTA_RESULTADO/arp-h1.txt"
```

## O que conferir

- conexão do `s1` ao Ryu;
- portas `1`, `2`, `3` e `4` associadas aos hosts;
- correspondência correta entre IP, MAC e porta;
- primeira resposta potencialmente mais lenta por incluir descoberta e instalação;
- pings seguintes estabilizados;
- fluxos IPv4 nos dois sentidos;
- `pingall` sem perda nos cenários estáveis.

O `arp_proxy_v3.py` recebido instala os fluxos IPv4 com `idle_timeout=60`; portanto, registre o dump logo após o tráfego.

## Encerramento

```text
mininet> exit
```

Depois, no terminal:

```bash
./utilitarios/limpar-mininet.sh
```

Preencha resultado, pequena conclusão, limitações e melhorias conforme o teste 09.
