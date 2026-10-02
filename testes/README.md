# Índice dos testes

Os roteiros abaixo transformam os ensaios do TCC em uma sequência repetível. Execute sempre o teste 00 antes de iniciar um cenário e o teste 09 ao terminar.

## Ordem recomendada

| Ordem | Roteiro | Arquivos necessários | Situação atual |
|---:|---|---|---|
| 00 | [Preparação do ambiente](00-preparacao-do-ambiente.md) | OVA ou ambiente manual | Pronto |
| 01 | [SDN — 1 switch e 4 hosts](01-validacao-sdn-1-switch-4-hosts.md) | `arp_proxy_v3.py` e topologia v3 | Executável |
| 02 | [Convencional — 1 switch e 4 hosts](02-validacao-convencional-1-switch-4-hosts.md) | Topologia convencional | Arquivo pendente |
| 03 | [Anel convencional sem STP](03-anel-convencional-sem-stp.md) | Topologia em anel sem STP | Arquivo pendente |
| 04 | [Anel com STP e RSTP](04-anel-com-stp-e-rstp.md) | Topologias STP/RSTP | Arquivos pendentes |
| 05 | [Anel SDN e contenção de ARP](05-anel-sdn-contencao-arp.md) | Controlador v3.6 e topologia SDN | Arquivos pendentes |
| 06 | [Falha e reconvergência](06-falha-e-reconvergencia.md) | STP, RSTP e controlador v3.7 | Arquivos pendentes |
| 07 | [Alta frequência — 5 ms](07-alta-frequencia-5ms.md) | RSTP e controlador v3.7 | Arquivos pendentes |
| 08 | [Malha completa K4](08-malha-completa-k4.md) | Topologias K4 RSTP/SDN | Arquivos pendentes |
| 09 | [Encerramento e consolidação](09-encerramento-e-consolidacao.md) | Evidências da rodada | Pronto |

## Convenções

- **Terminal 1:** controlador Ryu, quando aplicável;
- **Terminal 2:** topologia e CLI do Mininet;
- **Terminal 3:** inspeção externa, capturas ou recuperação do ambiente;
- **pasta da execução:** variável exportada `PASTA_RESULTADO`;
- **nomes pendentes:** nomes recomendados que devem ser ajustados após a inclusão dos arquivos finais.

Crie a pasta de cada execução com:

```bash
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh nome-do-cenario)"
printf '%s\n' "$PASTA_RESULTADO"
```

## Regras para comparação

1. Use a mesma VM ou registre todas as diferenças do ambiente.
2. Reinicie o cenário e execute `sudo mn -c` entre as rodadas.
3. Use os mesmos hosts, endereços, enlaces, intervalos, contagens e duração.
4. Registre o instante da falha em vez de estimá-lo depois.
5. Não compare uma primeira descoberta ARP com tráfego já aquecido sem indicar isso.
6. Preserve a saída bruta; tabelas e gráficos devem ser derivados dela.
7. Não trate o resultado de uma execução isolada como garantia universal.

O Mininet documenta `pingall`, a execução de comandos nos hosts e a alteração de enlaces com `link ... down/up` em seu [guia oficial](https://mininet.org/walkthrough/).
