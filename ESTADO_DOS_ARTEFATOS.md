# Estado dos artefatos

Este quadro diferencia o material já versionado dos arquivos que ainda precisam ser adicionados para reproduzir integralmente os testes descritos no TCC.

| Artefato | Estado | Local ou ação necessária |
|---|---|---|
| Controlador `arp_proxy_v3.py` | Incluído | `reproducao/codigo/controlador/` |
| Topologia SDN de 1 switch e 4 hosts | Incluída | `reproducao/codigo/topologias/` |
| Documentos ARP Proxy v1/v2 | Incluídos | `documentacao/desenvolvimento/` |
| Documento `topologiav2.docx` | Incluído | `documentacao/desenvolvimento/` |
| Controlador `v3.6` | Pendente | Adicionar o arquivo usado no teste de contenção ARP |
| Controlador `v3.7` | Pendente | Adicionar o arquivo usado nos testes de falha e reconvergência |
| Topologia convencional de 1 switch | Pendente | Necessária para o teste 02 |
| Topologias em anel com 3 switches e 6 hosts | Pendente | Necessárias para os testes 03 a 07 |
| Topologias K4 com 4 switches e 8 hosts | Pendente | Necessárias para o teste 08 |
| Resultados brutos, tabelas e capturas | Pendente | Organizar em `reproducao/resultados/` |
| Inventário exato da VM | Pendente | Gerar com `utilitarios/coletar-informacoes-do-ambiente.sh` |
| OVA sanitizada | Pendente | Publicar em uma GitHub Release com SHA-256 |
| Versão final do TCC | Pendente | Adicionar em `documentacao/tcc/` se a publicação for autorizada |
| Licença do código | Pendente | Definir antes de tornar o repositório público |
| Direitos de redistribuição das referências | Revisão necessária | Manter somente o que puder ser redistribuído |

## Critério para versão reproduzível

Uma versão só deve ser marcada como reproduzível quando:

- os nomes dos controladores e das topologias coincidirem com os roteiros;
- a OVA tiver sido importada e testada em outro ambiente;
- todos os checksums tiverem sido conferidos;
- cada cenário possuir logs e parâmetros suficientes para repetição;
- os documentos não contiverem credenciais, dados pessoais ou arquivos sem autorização de redistribuição.

A tag `v0.1.0-snapshot` representa somente o material inicialmente recebido e não deve ser confundida com a versão final do experimento.
