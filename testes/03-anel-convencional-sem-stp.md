# 03 — Anel convencional sem STP

> **Arquivo pendente:** nome recomendado `topologia_anel_3_switches_6_hosts_sem_stp.py`.

## Objetivo

Demonstrar por que uma topologia Ethernet redundante, sem mecanismo de prevenção de loops, pode gerar tempestade de broadcast, duplicação de quadros, aumento de CPU e perda de conectividade.

## Aviso de segurança

Execute apenas dentro da VM/Mininet. Não replique o anel em uma rede física de produção. Use um único ping, limite tempo e quantidade das capturas e mantenha um terceiro terminal pronto para executar `sudo mn -c`.

## Passo a passo

### 1. Preparar a rodada

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh anel-sem-stp)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_sem_stp.py"
```

### 2. Iniciar a topologia — sem controlador

```bash
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 3. Confirmar que STP e RSTP estão desativados

```text
mininet> sh ovs-vsctl get bridge s1 stp_enable
mininet> sh ovs-vsctl get bridge s2 stp_enable
mininet> sh ovs-vsctl get bridge s3 stp_enable
mininet> sh ovs-vsctl get bridge s1 rstp_enable
mininet> sh ovs-vsctl get bridge s2 rstp_enable
mininet> sh ovs-vsctl get bridge s3 rstp_enable
```

Todos devem retornar `false`.

### 4. Mapear os enlaces internos

```text
mininet> links
mininet> sh ovs-ofctl -O OpenFlow13 show s1
mininet> sh ovs-ofctl -O OpenFlow13 show s2
mininet> sh ovs-ofctl -O OpenFlow13 show s3
```

Anote uma interface de cada enlace do anel. Nos comandos seguintes, substitua `s1-ethX`, `s2-ethX` e `s3-ethX` pelos nomes reais.

### 5. Registrar contadores antes do tráfego

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1 > "$PASTA_RESULTADO/portas-s1-antes.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2 > "$PASTA_RESULTADO/portas-s2-antes.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3 > "$PASTA_RESULTADO/portas-s3-antes.txt"
```

### 6. Iniciar capturas limitadas

```text
mininet> sh timeout 6 tcpdump -nn -e -i s1-ethX -c 5000 arp -w "$PASTA_RESULTADO/anel-s1.pcap" &
mininet> sh timeout 6 tcpdump -nn -e -i s2-ethX -c 5000 arp -w "$PASTA_RESULTADO/anel-s2.pcap" &
mininet> sh timeout 6 tcpdump -nn -e -i s3-ethX -c 5000 arp -w "$PASTA_RESULTADO/anel-s3.pcap" &
```

### 7. Gerar somente um ping

```text
mininet> h1 ip neigh flush all
mininet> h1 timeout 3 ping -c 1 -W 1 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
mininet> sh sleep 2
```

Se a CLI ficar lenta ou a CPU subir fortemente, não insista em novos pings.

### 8. Coletar contadores e encerrar imediatamente

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s1 > "$PASTA_RESULTADO/portas-s1-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s2 > "$PASTA_RESULTADO/portas-s2-depois.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-ports s3 > "$PASTA_RESULTADO/portas-s3-depois.txt"
mininet> sh top -b -n 1 > "$PASTA_RESULTADO/cpu.txt"
mininet> exit
```

No terceiro terminal, caso a CLI não responda:

```bash
./utilitarios/limpar-mininet.sh
```

Execute a limpeza também após uma saída normal.

### 9. Contar os quadros capturados

```bash
for captura in "$PASTA_RESULTADO"/*.pcap; do
  printf '%s: ' "$(basename "$captura")"
  tcpdump -nn -r "$captura" 2>/dev/null | wc -l
done | tee "$PASTA_RESULTADO/contagem-das-capturas.txt"
```

## Evidências esperadas

- um único ARP broadcast reaparece repetidamente nos enlaces;
- as capturas atingem rapidamente o limite definido;
- os contadores de pacotes crescem de forma desproporcional ao único ping;
- pode ocorrer aumento de CPU, erro ou perda de conectividade.

O objetivo não é medir o máximo da tempestade, mas demonstrar a ausência de um mecanismo que interrompa o loop L2.
