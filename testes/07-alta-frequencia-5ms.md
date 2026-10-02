# 07 — Falha com ping a cada 5 ms

> **Arquivos pendentes:** cenário RSTP e cenário SDN com controlador `v3.7`.

## Objetivo

Comparar RSTP e SDN durante uma falha usando intervalo de 5 ms, o que aumenta a resolução da contagem de perdas durante a janela de recuperação.

O teste original utilizou **3.743 pacotes**. A 5 ms, a duração nominal fica próxima de 18,7 segundos.

## Cuidados

- execute somente dentro da VM;
- confirme que o host Mininet permite `ping -i 0.005`;
- use o mesmo enlace e o mesmo instante relativo de falha;
- não execute as duas tecnologias simultaneamente;
- registre uso de CPU se houver suspeita de saturação do hospedeiro.

## Parte A — RSTP

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh failover-rstp-5ms)"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_rstp.py"
./utilitarios/executar-topologia.sh 2>&1 \
  | tee "$PASTA_RESULTADO/topologia.log"
```

Depois que o RSTP estabilizar:

```text
mininet> h1 ping -c 5 10.0.0.3
mininet> h1 env LC_ALL=C ping -D -i 0.005 -c 3743 10.0.0.3 > "$PASTA_RESULTADO/ping.txt" 2>&1 &
mininet> sh sleep 5
mininet> sh date --iso-8601=ns > "$PASTA_RESULTADO/instante-da-falha.txt"
mininet> link s1 s2 down
mininet> sh sleep 15
mininet> link s1 s2 up
mininet> sh top -b -n 1 > "$PASTA_RESULTADO/cpu.txt"
```

## Parte B — SDN v3.7

```bash
./utilitarios/limpar-mininet.sh
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh failover-sdn-v3_7-5ms)"
export CONTROLADOR="reproducao/codigo/controlador/arp_proxy_v3_7.py"
export TOPOLOGIA="reproducao/codigo/topologias/topologia_anel_3_switches_6_hosts_sdn.py"
```

Inicie controlador e topologia em terminais separados. Na CLI:

```text
mininet> h1 ping -c 5 10.0.0.3
mininet> h1 env LC_ALL=C ping -D -i 0.005 -c 3743 10.0.0.3 > "$PASTA_RESULTADO/ping.txt" 2>&1 &
mininet> sh sleep 5
mininet> sh date --iso-8601=ns > "$PASTA_RESULTADO/instante-da-falha.txt"
mininet> link s1 s2 down
mininet> sh sleep 15
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1 > "$PASTA_RESULTADO/fluxos-s1.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s2 > "$PASTA_RESULTADO/fluxos-s2.txt"
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s3 > "$PASTA_RESULTADO/fluxos-s3.txt"
mininet> link s1 s2 up
mininet> sh top -b -n 1 > "$PASTA_RESULTADO/cpu.txt"
```

## Referência histórica dos testes já realizados

Estes valores servem para conferência, não como critério rígido de aprovação:

| Tecnologia | Transmitidos | Recebidos | Perda | RTT médio | RTT máximo |
|---|---:|---:|---:|---:|---:|
| RSTP | 3.743 | 3.741 | 0,053431% | 0,192 ms | 1,600 ms |
| SDN v3.7 | 3.743 | 3.739 | 0,106866% | 0,181 ms | 2,031 ms |

Uma reprodução só é diretamente comparável se mantiver hardware/VM, momento da falha, topologia e versões. Diferenças pequenas podem vir do escalonamento da VM e não da tecnologia de controle.

## Encerramento

Confira o resumo do `ping`, calcule o maior intervalo pelo método do teste 06, saia da CLI e execute `./utilitarios/limpar-mininet.sh`.
