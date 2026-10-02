# Guia de reprodução

Este diretório concentra tudo o que uma terceira pessoa precisa para executar os cenários descritos no TCC. A reprodução preferencial utiliza a OVA, pois ela preserva versões compatíveis do sistema operacional, Ryu, Mininet e Open vSwitch.

## Opção A — usar a OVA

1. Acesse a página de [Releases do projeto](https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN/releases).
2. Baixe a OVA e o arquivo de checksum da mesma versão.
3. Confira a integridade com `sha256sum -c NOME_DA_OVA.ova.sha256`.
4. Importe a OVA no VirtualBox.
5. Inicie a VM e abra o repositório disponível nela.
6. Execute `./utilitarios/verificar-ambiente.sh`.
7. Siga [00 — Preparação do ambiente](../testes/00-preparacao-do-ambiente.md).

Se a OVA estiver dividida, consulte as instruções de remontagem em [maquina_virtual/README.md](maquina_virtual/README.md).

## Opção B — preparar o ambiente manualmente

1. Use uma distribuição Linux compatível com as versões registradas em `ambiente/versoes.txt`.
2. Instale Python, Ryu, Mininet, Open vSwitch, `tcpdump` e `iperf`.
3. Clone este repositório e acesse sua raiz.
4. Execute:

   ```bash
   ./utilitarios/verificar-ambiente.sh
   ./utilitarios/coletar-informacoes-do-ambiente.sh
   ./utilitarios/limpar-mininet.sh
   ```

5. Compare a saída com o inventário da OVA antes de atribuir diferenças de resultado ao controlador.

Não foi fixada aqui uma sequência genérica de instalação por `apt` ou `pip`, pois combinações recentes de Python, Ryu, Eventlet, Mininet e Open vSwitch podem não reproduzir o ambiente original. A OVA e o arquivo `ambiente/versoes.txt` serão a referência exata.

## Conteúdo

| Caminho | Uso |
|---|---|
| `codigo/controlador/` | Controladores Ryu utilizados nos ensaios |
| `codigo/topologias/` | Topologias Mininet convencionais e SDN |
| `ambiente/` | Inventário de versões e configuração do laboratório |
| `maquina_virtual/` | Instruções de exportação, publicação, importação e integridade da OVA |
| `resultados/brutos/` | Logs e capturas locais de cada execução |
| `resultados/consolidados/` | Tabelas, gráficos e sínteses pequenas que podem ser versionadas |

## Arquivos que ainda precisam ser colocados

Os espaços já estão preparados para receber:

- controlador `v3.6`, usado na contenção de ARP;
- controlador `v3.7`, usado nos testes de falha e reconvergência;
- topologia convencional de 1 switch e 4 hosts;
- topologias em anel para STP, RSTP e SDN;
- topologias da malha completa K4;
- `ambiente/versoes.txt` gerado dentro da VM final;
- resultados brutos e consolidados;
- OVA exportada e seu checksum.

Após adicionar os arquivos, atualize [ESTADO_DOS_ARTEFATOS.md](../ESTADO_DOS_ARTEFATOS.md) e substitua os nomes recomendados nos roteiros pelos nomes reais.

## Regra de comparação

Os cenários comparados devem usar os mesmos pares de hosts, quantidade e intervalo de pacotes, duração do `iperf`, capacidade/atraso dos enlaces e momento da falha. Alterar um desses parâmetros exige uma nova rodada para todos os cenários.

## Fontes técnicas oficiais

- [Mininet Walkthrough](https://mininet.org/walkthrough/)
- [Open vSwitch — documentação](https://docs.openvswitch.org/en/stable/)
- [Ryu — documentação](https://ryu.readthedocs.io/en/latest/)
- [Oracle VirtualBox — manual](https://www.virtualbox.org/manual/)
- [GitHub — arquivos grandes](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [GitHub — Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
