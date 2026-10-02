# 09 — Encerramento e consolidação

Use esta etapa depois de cada cenário para garantir que a evidência seja legível, rastreável e suficiente para uma terceira pessoa repetir o ensaio.

## 1. Encerrar a rede

Na CLI:

```text
mininet> exit
```

Depois:

```bash
./utilitarios/limpar-mininet.sh
```

Confirme que não restaram processos ou bridges do experimento antes da próxima rodada.

## 2. Conferir os arquivos mínimos

```bash
find "$PASTA_RESULTADO" -maxdepth 1 -type f -printf '%f\n' | sort
```

A pasta deve conter, conforme o cenário:

- `COMANDOS.md` preenchido;
- `ambiente.txt` e `commit.txt`;
- hashes do controlador e da topologia;
- log do controlador, quando houver;
- log da topologia;
- saída dos pings;
- estados STP/RSTP ou fluxos OpenFlow;
- capturas e mapeamento das interfaces;
- saída do `iperf`, quando aplicável;
- instante da falha, nos testes de reconvergência.

## 3. Gerar versões textuais das capturas importantes

Exemplo:

```bash
tcpdump -nn -e -tttt -r "$PASTA_RESULTADO/arquivo.pcap" \
  > "$PASTA_RESULTADO/arquivo-pcap.txt"
```

Preserve também o `.pcap` original.

## 4. Preencher a síntese

Copie [MODELO_DE_RESULTADO.md](../reproducao/resultados/MODELO_DE_RESULTADO.md) para a pasta da rodada e preencha:

```bash
cp reproducao/resultados/MODELO_DE_RESULTADO.md \
  "$PASTA_RESULTADO/RESULTADO.md"
```

Separe fatos medidos de interpretação. Use “nos cenários testados” quando a evidência não permitir generalização.

## 5. Gerar checksums da rodada

```bash
(
  cd "$PASTA_RESULTADO"
  find . -maxdepth 1 -type f ! -name CHECKSUMS.sha256 -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    > CHECKSUMS.sha256
)
```

## 6. Consolidar sem apagar os dados brutos

Transfira apenas tabelas, CSV, gráficos e conclusões revisadas para `reproducao/resultados/consolidados/`. Logs e capturas grandes permanecem em `brutos/` ou são anexados à Release.

## 7. Checklist de qualidade

- [ ] Todos os comandos estão na ordem executada.
- [ ] O controlador, a topologia e o commit foram identificados.
- [ ] Os parâmetros dos enlaces foram registrados.
- [ ] A interface de cada captura foi mapeada.
- [ ] O resumo do ping não foi cortado.
- [ ] A falha tem timestamp, quando aplicável.
- [ ] A comparação usa os mesmos parâmetros.
- [ ] Resultado e conclusão estão separados.
- [ ] Limitações e melhorias foram registradas.
- [ ] Não há token, senha, chave ou dado pessoal nos arquivos.
