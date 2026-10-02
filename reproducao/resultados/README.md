# Organização dos resultados

Crie uma pasta para cada execução usando data, cenário e tecnologia. Exemplo:

```text
reproducao/resultados/brutos/2026-10-02-anel-sdn-v3_7/
├── COMANDOS.md
├── ambiente.txt
├── commit.txt
├── controlador.log
├── topologia.log
├── ping-h1-h3.txt
├── fluxos-s1.txt
├── fluxos-s2.txt
├── fluxos-s3.txt
└── enlace-interno-s1-ethX.pcap
```

## Resultados brutos

`brutos/` guarda a saída original dos comandos. Logs e capturas podem ficar grandes e, por isso, são ignorados pelo Git. Quando precisarem ser distribuídos, compacte-os e anexe-os à mesma Release da versão do experimento.

Cada pasta deve registrar:

- data e hora da execução;
- commit do código;
- controlador e topologia usados;
- versões do ambiente;
- comandos na ordem em que foram executados;
- momento exato da queda de enlace, quando aplicável;
- saída completa de `ping`, `iperf`, STP/RSTP e fluxos OpenFlow;
- interfaces usadas nas capturas `tcpdump`.

## Resultados consolidados

`consolidados/` recebe arquivos pequenos e revisados, como CSV, tabelas, gráficos e resumos. Para cada cenário, use estes quatro campos:

1. **Resultado:** valores medidos, sem interpretação exagerada;
2. **pequena conclusão:** o que os dados demonstram naquele cenário;
3. **limitações:** o que não pode ser generalizado;
4. **melhorias:** próximos ajustes possíveis.

Não misture resultados de rodadas com parâmetros diferentes. Uma alteração no intervalo do ping, duração do `iperf`, atraso, largura de banda ou instante da falha exige nova identificação da rodada.
