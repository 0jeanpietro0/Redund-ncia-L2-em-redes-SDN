# 05 — Anel SDN e contenção de ARP

> **Arquivos pendentes:** controlador `v3.6` e topologia SDN final com 3 switches e 6 hosts. Nomes recomendados: `arp_proxy_v3_6.py` e `topologia_anel_3_switches_6_hosts_sdn.py`.

## Objetivo

Verificar que a rede redundante permanece conectada sem STP e que os quadros ARP de descoberta não são propagados indiscriminadamente pelos enlaces entre switches.

## Passo a passo

### 1. Preparar a rodada

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh anel-sdn-v3_6)"
export CONTROLADOR="reproducao/codigo/controlador/arp_proxy_v3_6.py"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_sdn.py"
```

### 2. Iniciar o controlador — Terminal 1

```bash
./utilitarios/executar-controlador.sh 2>&1 \
  | tee "$PASTA_RESULTADO/controlador.log"
```

O parâmetro `--observe-links` já é acrescentado pelo utilitário.

### 3. Iniciar a topologia — Terminal 2

```bash
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

Antes do tráfego, confirme no log do Ryu que os três switches e os três enlaces do anel foram descobertos.

### 4. Mapear as interfaces internas

```text
mininet> links
mininet> sh ovs-ofctl -O OpenFlow13 show s1
mininet> sh ovs-ofctl -O OpenFlow13 show s2
mininet> sh ovs-ofctl -O OpenFlow13 show s3
```

Escolha uma interface de cada enlace do anel e substitua `s1-ethX`, `s2-ethX` e `s3-ethX` abaixo.

### 5. Limpar as tabelas de vizinhança

```text
mininet> h1 ip neigh flush all
mininet> h2 ip neigh flush all
mininet> h3 ip neigh flush all
mininet> h4 ip neigh flush all
mininet> h5 ip neigh flush all
mininet> h6 ip neigh flush all
```

### 6. Iniciar capturas ARP

Capture uma porta de borda e uma interface de cada enlace interno:

```text
mininet> h1 timeout 15 tcpdump -nn -e -i h1-eth0 arp -w "$PASTA_RESULTADO/arp-borda-h1.pcap" &
mininet> sh timeout 15 tcpdump -nn -e -i s1-ethX arp -w "$PASTA_RESULTADO/arp-interno-s1.pcap" &
mininet> sh timeout 15 tcpdump -nn -e -i s2-ethX arp -w "$PASTA_RESULTADO/arp-interno-s2.pcap" &
mininet> sh timeout 15 tcpdump -nn -e -i s3-ethX arp -w "$PASTA_RESULTADO/arp-interno-s3.pcap" &
```

O filtro `arp` exclui LLDP. Portanto, a ausência de ARP na captura interna não significa ausência de todo tráfego de controle.

### 7. Gerar descoberta e tráfego

Use um par de hosts em switches diferentes. No cenário originalmente testado:

```text
mininet> h1 ping -c 20 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
mininet> pingall
mininet> sh sleep 2
```

### 8. Registrar fluxos

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-s1.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2 > "$PASTA_RESULTADO/fluxos-s2.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3 > "$PASTA_RESULTADO/fluxos-s3.txt"
```

### 9. Contar ARP por captura

Após os `timeout` terminarem:

```bash
for captura in "$PASTA_RESULTADO"/*.pcap; do
  printf '%s: ' "$(basename "$captura")"
  tcpdump -nn -r "$captura" 2>/dev/null | wc -l
done | tee "$PASTA_RESULTADO/contagem-arp.txt"
```

## Critérios de validação

- a borda registra a solicitação ARP do host;
- os enlaces internos escolhidos não registram flooding ARP durante a descoberta;
- o controlador aprende IP, MAC, DPID e porta;
- o caminho IPv4 é instalado nos switches envolvidos;
- `h1` alcança `h3` e o `pingall` termina sem perda inesperada;
- os enlaces redundantes continuam presentes, sem bloqueio de STP.

Formule a conclusão como válida **nos cenários testados**, com endereçamento estático. A solução não implementa DHCP nem balanceamento de carga.
