# Redundância L2 em redes SDN com ARP Proxy

Este repositório reúne o código, as topologias, os roteiros de teste e os materiais de reprodução do TCC sobre o uso de um **ARP Proxy controlado por SDN** para evitar a propagação indiscriminada de ARP em redes de camada 2 com caminhos redundantes.

A implementação utiliza **Ryu**, **OpenFlow 1.3**, **Open vSwitch** e **Mininet**. O controlador aprende a associação entre IP, MAC, switch e porta dos hosts, responde às solicitações ARP quando o destino já é conhecido e instala os fluxos IPv4 calculados para o caminho selecionado.

> **Estado do repositório:** o snapshot atualmente disponível contém o controlador `v3` e a topologia SDN de 1 switch com 4 hosts. Os arquivos finais usados nos testes de redundância (`v3.6`, `v3.7`, topologias em anel, cenários STP/RSTP e malha K4) ainda precisam ser adicionados. Consulte [ESTADO_DOS_ARTEFATOS.md](ESTADO_DOS_ARTEFATOS.md) antes de tentar reproduzir todo o TCC.

## Comece por aqui

| Objetivo | Documento |
|---|---|
| Entender o que já está disponível | [Estado dos artefatos](ESTADO_DOS_ARTEFATOS.md) |
| Reproduzir com a máquina virtual | [Guia de reprodução](reproducao/README.md) |
| Preparar e publicar a OVA | [Máquina virtual](reproducao/maquina_virtual/README.md) |
| Executar os ensaios | [Índice de testes](testes/README.md) |
| Organizar logs e resultados | [Resultados](reproducao/resultados/README.md) |
| Conferir a origem dos arquivos | [Manifesto de arquivos](documentacao/MANIFESTO_DE_ARQUIVOS.md) |

## Estrutura

```text
.
├── documentacao/                 # TCC, referências, figuras e histórico do desenvolvimento
├── reproducao/
│   ├── ambiente/                 # Inventário das versões do laboratório
│   ├── codigo/
│   │   ├── controlador/          # Aplicações Ryu
│   │   └── topologias/           # Cenários Mininet/OVS
│   ├── maquina_virtual/          # Instruções e área local para a OVA
│   └── resultados/               # Evidências brutas e resultados consolidados
├── testes/                       # Passo a passo de cada ensaio
└── utilitarios/                  # Verificação, execução, coleta e limpeza
```

Os nomes dos diretórios e toda a documentação de apoio estão em português. Nomes próprios de tecnologias e comandos, como `OpenFlow`, `Packet-In`, `ping`, `tcpdump` e `iperf`, foram mantidos por serem termos técnicos.

## Reprodução rápida do cenário disponível

### Pré-requisitos

- Linux compatível ou a OVA do projeto;
- Python 3;
- Ryu;
- Mininet;
- Open vSwitch com OpenFlow 1.3;
- permissões de `sudo` para criar e limpar a rede emulada.

### Execução

1. Verifique o ambiente:

   ```bash
   ./utilitarios/verificar-ambiente.sh
   ```

2. Limpe resíduos de execuções anteriores:

   ```bash
   ./utilitarios/limpar-mininet.sh
   ```

3. No primeiro terminal, inicie o controlador:

   ```bash
   ./utilitarios/executar-controlador.sh
   ```

4. No segundo terminal, inicie a topologia:

   ```bash
   ./utilitarios/executar-topologia.sh
   ```

5. No prompt do Mininet, execute:

   ```text
   mininet> pingall
   mininet> h1 ping -c 20 10.0.0.3
   mininet> h3 ping -c 20 10.0.0.1
   mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

6. Ao terminar, saia da CLI e limpe o ambiente:

   ```bash
   ./utilitarios/limpar-mininet.sh
   ```

O controlador e a topologia disponíveis usam OpenFlow 1.3 e conexão com o Ryu em `127.0.0.1:6633`. O roteiro completo está em [01 — Validação SDN com 1 switch e 4 hosts](testes/01-validacao-sdn-1-switch-4-hosts.md).

## Conjunto de testes documentado

| Nº | Cenário | Finalidade |
|---:|---|---|
| 00 | Preparação | Fixar versões, limpar o ambiente e criar a pasta da execução |
| 01 | SDN, 1 switch e 4 hosts | Validar ARP, conectividade e instalação de fluxos |
| 02 | Convencional, 1 switch e 4 hosts | Criar a referência sem controlador |
| 03 | Anel convencional sem STP | Demonstrar loop L2 e tempestade de broadcast com limites de segurança |
| 04 | Anel com STP e RSTP | Identificar portas bloqueadas e validar conectividade |
| 05 | Anel SDN | Verificar contenção de ARP nos enlaces internos |
| 06 | Falha de enlace | Comparar reconvergência de STP, RSTP e SDN |
| 07 | Ping a cada 5 ms | Comparar perda durante a falha sob maior frequência |
| 08 | Malha completa K4 | Avaliar redundância, portas bloqueadas e fluxos `iperf` paralelos |
| 09 | Encerramento | Consolidar evidências, métricas, conclusão e limitações |

Veja os comandos, a ordem de execução e os critérios de registro em [testes/README.md](testes/README.md).

## Onde adicionar os arquivos finais

- Controladores Ryu: `reproducao/codigo/controlador/`;
- topologias Mininet: `reproducao/codigo/topologias/`;
- versão final do TCC: `documentacao/tcc/`;
- figuras das topologias: `documentacao/figuras/`;
- resultados pequenos e consolidados: `reproducao/resultados/consolidados/`;
- logs e capturas locais: `reproducao/resultados/brutos/`;
- OVA: preparar em `reproducao/maquina_virtual/arquivos/` e publicar como ativo de uma [GitHub Release](https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN/releases).

A OVA, discos virtuais, logs e capturas grandes são ignorados pelo Git para não aumentar o histórico do repositório. O arquivo da VM deve ser distribuído pela Release com checksum SHA-256.

## Limites do trabalho

- A solução cria condições para uso futuro de engenharia de tráfego e múltiplos caminhos, mas **não implementa balanceamento de carga**.
- O LLDP usado por `--observe-links` é tráfego de controle local aos enlaces; ele não equivale a flooding ARP.
- Os resultados devem ser descritos como válidos para os cenários efetivamente testados, com endereçamento IPv4 estático.
- DHCP exige tratamento próprio por utilizar broadcast e não faz parte da implementação atual.

## Integridade e atualização

Ao adicionar um artefato final:

1. atualize [ESTADO_DOS_ARTEFATOS.md](ESTADO_DOS_ARTEFATOS.md);
2. registre a alteração em [HISTORICO_DE_ALTERACOES.md](HISTORICO_DE_ALTERACOES.md);
3. calcule o SHA-256 e atualize o [manifesto](documentacao/MANIFESTO_DE_ARQUIVOS.md);
4. ajuste o roteiro de teste para apontar ao nome real do arquivo;
5. execute a validação em uma VM limpa antes de criar uma versão final.

Os documentos de terceiros permanecem sujeitos aos direitos e às condições de distribuição de suas fontes. Antes de tornar o repositório público, revise esses materiais e substitua por links oficiais quando necessário.
