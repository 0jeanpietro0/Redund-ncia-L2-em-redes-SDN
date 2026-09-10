# ARP Proxy com SDN

Repositório de apoio ao TCC sobre uma implementação de ARP Proxy centralizado em uma rede definida por software (SDN), utilizando Ryu, OpenFlow 1.3, Open vSwitch e Mininet.

O controlador aprende a associação entre IP, MAC, switch e porta dos hosts, responde a solicitações ARP quando o destino já é conhecido, limita a descoberta de destinos desconhecidos às portas de borda e instala caminhos IPv4 calculados pelo controlador.

> **Estado atual:** esta primeira organização usa exatamente os arquivos recebidos como `v3`. A versão `v3.6`, as topologias finais convencional e redundante e a máquina virtual OVA ainda precisam ser adicionadas antes de marcar uma versão final reproduzível.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `controller/` | Aplicações do controlador Ryu |
| `topologies/` | Scripts de topologia Mininet/Mininet-WiFi |
| `docs/development/` | Documentos históricos do desenvolvimento |
| `docs/references/` | Referências acadêmicas recebidas, sujeitas à revisão de redistribuição |
| `environment/` | Inventário e instruções do ambiente experimental |
| `results/` | Modelo para logs, capturas e resultados dos ensaios |
| `scripts/` | Inicialização, verificação, limpeza e preparação da OVA |
| `vm/` | Instruções da máquina virtual; a OVA será distribuída por uma Release |

## Cenário disponível

A topologia atualmente versionada contém um switch Open vSwitch e quatro hosts na rede `10.0.0.0/24`:

| Host | IPv4 |
|---|---|
| `h1` | `10.0.0.1/24` |
| `h2` | `10.0.0.2/24` |
| `h3` | `10.0.0.3/24` |
| `h4` | `10.0.0.4/24` |

Esse cenário é útil para validar aprendizado de hosts, resposta ARP e instalação de fluxos. Como possui apenas um switch, ele **não comprova sozinho** a contenção de flooding em enlaces redundantes; isso depende da inclusão e execução da topologia cíclica final.

## Execução rápida

Em uma máquina com Ryu, Mininet e Open vSwitch instalados:

1. Verifique o ambiente:

   ```bash
   ./scripts/preflight.sh
   ```

2. Em um terminal, inicie o controlador:

   ```bash
   ./scripts/run-controller.sh
   ```

3. Em outro terminal, inicie a topologia:

   ```bash
   ./scripts/run-topology.sh
   ```

4. No prompt do Mininet, execute testes básicos:

   ```text
   mininet> pingall
   mininet> h1 ping -c 20 10.0.0.3
   mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

5. Ao terminar, saia do Mininet e limpe o ambiente:

   ```bash
   ./scripts/cleanup-mininet.sh
   ```

O controlador e a topologia usam OpenFlow 1.3 e a conexão remota em `127.0.0.1:6633`.

## Reprodução por máquina virtual

A forma principal de reprodução será uma OVA já configurada. Ela não deve entrar no histórico normal do Git, pois arquivos comuns acima de 100 MiB são bloqueados pelo GitHub. A OVA será anexada a uma **GitHub Release**, acompanhada de checksum SHA-256 e do inventário de versões do ambiente.

Se a OVA superar o limite individual da Release, o script abaixo gera partes menores e os respectivos checksums:

```bash
./scripts/prepare-ova-release.sh /caminho/arp-proxy-sdn-lab.ova
```

Consulte [`vm/README.md`](vm/README.md) antes de exportar ou publicar a máquina.

## Método de teste

O roteiro completo está em [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md). Cada execução deve preservar:

- versão do controlador e da topologia;
- inventário de SO, Python, Ryu, Mininet e Open vSwitch;
- comandos executados;
- logs do controlador;
- fluxos OpenFlow;
- capturas `tcpdump`, quando aplicável;
- resultados brutos e síntese da análise.

## Integridade e proveniência

Os hashes dos arquivos recebidos e seus destinos estão em [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md). Arquivos históricos foram preservados sem alteração; a validação sintática dos dois scripts Python recebidos foi concluída com sucesso.

## Licença e referências

A licença do código ainda precisa ser escolhida pelo autor. Os documentos de terceiros permanecem sujeitos aos direitos e às condições de distribuição de suas fontes originais. Antes de tornar o repositório público, esses materiais devem ser revisados e, quando necessário, substituídos por links oficiais.
