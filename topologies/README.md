# Topologias dos ensaios

Todos os scripts utilizam Mininet e Open vSwitch. Os cenários SDN usam OpenFlow 1.3 e um controlador Ryu remoto em `127.0.0.1`.

| Arquivo | Switches/hosts | Tecnologia | Controlador indicado |
|---|---:|---|---|
| `topologia_arp_proxy_v3.py` | 1/4 | SDN | v3.6 |
| `topologia_convencional_v3.py` | 1/4 | OVS standalone | Nenhum |
| `topologia_arp_proxy_2s.py` | 2/4 | SDN | v3.6 |
| `topologia_convencional_2s.py` | 2/4 | OVS standalone | Nenhum |
| `topologia_arp_proxy_anel_3s_6h.py` | 3/6 | SDN em anel | v3.6 ou v3.7 |
| `topologia_convencional_anel_3s_6h_sem_stp.py` | 3/6 | Anel sem prevenção de loop | Nenhum |
| `topologia_convencional_anel_3s_6h_stp.py` | 3/6 | Anel com STP | Nenhum |
| `topologia_convencional_anel_3s_6h_rstp.py` | 3/6 | Anel com RSTP | Nenhum |
| `topologia_malha_rstp.py` | 4/8 | Malha K4 com RSTP | Nenhum |
| `topologia_malha_arp_proxy_v37.py` | 4/8 | Malha K4 SDN | v3.7 |

## Execução

Exemplo SDN:

```bash
# Terminal 1
./scripts/run-controller.sh controller/arp_proxy_v3_7.py

# Terminal 2
./scripts/run-topology.sh topologies/topologia_arp_proxy_anel_3s_6h.py
```

Exemplo convencional:

```bash
./scripts/run-topology.sh topologies/topologia_convencional_anel_3s_6h_rstp.py
```

## Porta do controlador

A topologia inicial de um switch declara a porta 6633. As topologias SDN posteriores declaram 6653. O Ryu 4.34 aceita por padrão a porta oficial 6653 e também mantém um listener de compatibilidade em 6633 quando nenhuma porta é forçada.

Se utilizar outra implementação ou iniciar o Ryu com `--ofp-tcp-listen-port`, confirme que o valor coincide com o script da topologia.

## Malha completa K4

Nos dois scripts de malha:

- cada switch possui dois hosts;
- enlaces host-switch: 100 Mbit/s e 0,2 ms;
- enlaces interswitch: 10 Mbit/s e 1 ms;
- enlaces: s1-s2, s1-s3, s1-s4, s2-s3, s2-s4 e s3-s4.

O roteiro operacional completo está em [`../docs/TEST_PLAN.md`](../docs/TEST_PLAN.md).
