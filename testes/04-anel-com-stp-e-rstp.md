# 04 — Anel convencional com STP e RSTP

> **Arquivos pendentes:** topologias finais em anel com 3 switches e 6 hosts. Nomes recomendados: `topologia_anel_3_switches_6_hosts_stp.py` e `topologia_anel_3_switches_6_hosts_rstp.py`.

## Objetivo

Validar que STP/RSTP eliminam o loop ao colocar pelo menos uma porta redundante fora do encaminhamento normal, mantendo conectividade pela árvore ativa.

Execute STP e RSTP em rodadas separadas e com a limpeza completa entre elas.

## Parte A — STP

### 1. Preparar e iniciar

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh anel-stp)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_stp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 2. Confirmar e aguardar a convergência

```text
mininet> sh ovs-vsctl get bridge s1 stp_enable
mininet> sh ovs-vsctl get bridge s2 stp_enable
mininet> sh ovs-vsctl get bridge s3 stp_enable
mininet> sh ovs-appctl stp/show s1
mininet> sh ovs-appctl stp/show s2
mininet> sh ovs-appctl stp/show s3
```

Repita `stp/show` até que as funções e estados das portas parem de mudar. Não inicie o ensaio durante `listening` ou `learning`.

Grave o estado:

```text
mininet> sh ovs-appctl stp/show s1 > "$PASTA_RESULTADO/stp-s1.txt"
mininet> sh ovs-appctl stp/show s2 > "$PASTA_RESULTADO/stp-s2.txt"
mininet> sh ovs-appctl stp/show s3 > "$PASTA_RESULTADO/stp-s3.txt"
```

### 3. Identificar raiz e porta bloqueada

Registre:

- switch raiz;
- root port de cada switch não raiz;
- designated ports;
- porta em estado de bloqueio/discarding;
- enlace lógico retirado da árvore ativa.

### 4. Testar conectividade

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
```

### 5. Observar a porta bloqueada

Substitua `s3-ethX` pela interface identificada:

```text
mininet> sh timeout 12 tcpdump -nn -e -i s3-ethX arp -w "$PASTA_RESULTADO/porta-bloqueada.pcap" &
mininet> h1 ip neigh flush all
mininet> h1 ping -c 1 10.0.0.3
mininet> sh sleep 2
```

Uma captura pode mostrar um quadro chegando fisicamente à interface bloqueada. Isso **não prova encaminhamento** pelo switch; correlacione a captura com o estado STP e os contadores das demais portas.

### 6. Encerrar

Saia da CLI e execute `./utilitarios/limpar-mininet.sh`.

## Parte B — RSTP

### 1. Preparar uma nova rodada

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh anel-rstp)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_rstp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

### 2. Confirmar RSTP e registrar estados

```text
mininet> sh ovs-vsctl get bridge s1 rstp_enable
mininet> sh ovs-vsctl get bridge s2 rstp_enable
mininet> sh ovs-vsctl get bridge s3 rstp_enable
mininet> sh ovs-vsctl get bridge s1 rstp_status > "$PASTA_RESULTADO/rstp-s1.txt"
mininet> sh ovs-vsctl get bridge s2 rstp_status > "$PASTA_RESULTADO/rstp-s2.txt"
mininet> sh ovs-vsctl get bridge s3 rstp_status > "$PASTA_RESULTADO/rstp-s3.txt"
```

Para cada porta inter-switch identificada com `links`, registre:

```text
mininet> sh ovs-vsctl get port s1-ethX rstp_status
```

Troque switch e interface conforme o mapeamento. Procure uma função `alternate` e estado `discarding` no caminho redundante.

### 3. Repetir os testes de conectividade

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3 | tee "$PASTA_RESULTADO/ping-h1-h3.txt"
mininet> sh ovs-appctl fdb/show s1 > "$PASTA_RESULTADO/fdb-s1.txt"
mininet> sh ovs-appctl fdb/show s2 > "$PASTA_RESULTADO/fdb-s2.txt"
mininet> sh ovs-appctl fdb/show s3 > "$PASTA_RESULTADO/fdb-s3.txt"
```

Encerre e limpe o Mininet.

## Comparação a registrar

| Item | STP | RSTP |
|---|---|---|
| Switch raiz | preencher | preencher |
| Porta/enlace bloqueado | preencher | preencher |
| Perda no `pingall` estável | preencher | preencher |
| RTT médio | preencher | preencher |
| Tempo até estado estável | preencher | preencher |

O Open vSwitch orienta habilitar STP em topologias redundantes para evitar loops, mas também alerta que sua implementação de STP possui limitações; registre a versão exata do OVS usada no experimento.
