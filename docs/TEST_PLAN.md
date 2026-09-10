# Plano de reprodução e testes

## 1. Preparação

1. Iniciar a VM ou preparar um Linux compatível.
2. Executar `./scripts/preflight.sh`.
3. Registrar as versões com:

   ```bash
   ./scripts/collect-environment-info.sh | tee environment/versions.txt
   ```

4. Limpar restos de execuções anteriores com `./scripts/cleanup-mininet.sh`.
5. Criar uma pasta própria em `results/raw/AAAA-MM-DD-cenario/` para os arquivos daquela execução.

## 2. Inicialização

Terminal 1:

```bash
./scripts/run-controller.sh 2>&1 | tee results/raw/AAAA-MM-DD-cenario/controller.log
```

Terminal 2:

```bash
./scripts/run-topology.sh
```

Confirmar no log do controlador que o switch se conectou e teve as portas enumeradas.

## 3. Testes básicos do cenário de um switch

No Mininet:

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3
mininet> h3 ping -c 20 10.0.0.1
mininet> h1 arp -n
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

Registrar separadamente o primeiro pacote e os pacotes posteriores quando a análise envolver descoberta/convergência.

## 4. Observação de ARP

Antes de repetir uma descoberta, limpar a entrada ARP apenas no host de teste:

```text
mininet> h1 ip neigh flush all
```

Capturar ARP na interface do host:

```text
mininet> h1 tcpdump -n -e -i h1-eth0 arp
```

Em uma topologia com múltiplos switches, também capturar as interfaces dos enlaces entre switches. O objetivo principal é verificar se os quadros ARP são contidos pelo controlador e não propagados indiscriminadamente pelos enlaces internos.

## 5. Topologia redundante

Este bloco só pode ser executado após a inclusão do script final da topologia redundante.

1. Identificar as interfaces switch-switch com `ovs-vsctl show` e `ovs-ofctl -O OpenFlow13 show <switch>`.
2. Executar `tcpdump` simultaneamente nas portas de borda e nos enlaces internos.
3. Limpar a vizinhança ARP do host de origem.
4. Iniciar um único ping e registrar Packet-In, aprendizado, resposta e instalação de fluxos.
5. Executar `pingall` e testes direcionados.
6. Interromper um enlace controladamente e verificar reconvergência e continuidade.
7. Restaurar o enlace e repetir o ensaio.

## 6. Cenário convencional

Executar os mesmos pares de hosts, quantidade de pacotes e capturas usados no cenário SDN. Não misturar resultados obtidos com parâmetros distintos. Registrar se STP/RSTP está habilitado, porque isso altera a disponibilidade dos caminhos redundantes e a propagação de broadcast.

## 7. Encerramento

1. Salvar logs, dumps de fluxos e capturas.
2. Sair da CLI do Mininet.
3. Executar `./scripts/cleanup-mininet.sh`.
4. Registrar em cada cenário: **Resultado**, **pequena conclusão**, limitações observadas e melhorias possíveis.

## Critérios mínimos

- Ausência de perda de pacotes não explicada nos cenários testados.
- Correspondência entre IP, MAC, DPID e porta aprendidos.
- Instalação de fluxos nos dois sentidos quando aplicável.
- Ausência de propagação ARP indevida pelos enlaces internos observados.
- Logs e parâmetros suficientes para uma terceira pessoa repetir o ensaio.

Os resultados devem ser descritos como válidos para os cenários efetivamente testados, especialmente quando o endereçamento for estático. DHCP continua exigindo tratamento próprio por utilizar broadcast.
