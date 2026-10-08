# Estado dos artefatos

Este arquivo registra o estado real do repositório após o alinhamento com a versão final do TCC.

| Artefato | Estado | Observação |
|---|---|---|
| Controladores v3, v3.5, v3.6 e v3.7 | Incluídos | A v3.6 consolida a contenção ARP; a v3.7 acrescenta tratamento de falhas |
| Topologias de 1 switch | Incluídas | Cenários SDN e convencional, 4 hosts |
| Topologias lineares de 2 switches | Incluídas | Cenários SDN e convencional, 4 hosts |
| Anel de 3 switches e 6 hosts | Incluído | SDN, sem STP/RSTP, STP e RSTP |
| Malha completa K4 | Incluída | RSTP e SDN com ARP Proxy v3.7, 4 switches e 8 hosts |
| Roteiro de todos os testes | Incluído | `docs/TEST_PLAN.md` |
| Scripts auxiliares | Incluídos | Verificação, execução, limpeza, inventário e preparação da OVA |
| Documentos históricos | Incluídos | Mantidos em `docs/development/` |
| Referências acadêmicas locais | Incluídas | Revisar permissão de redistribuição antes de tornar o repositório público |
| OVA dividida em três partes | Em rascunho | Arquivos enviados para uma GitHub Release ainda não publicada |
| SHA-256 da OVA remontada | Pendente | Calcular depois da remontagem final e publicar junto à Release |
| Teste independente da OVA | Pendente | Importar em outra instalação do VirtualBox e executar o roteiro mínimo |
| Resultados brutos e capturas | Não versionados | Permanecem fora do Git para evitar crescimento do repositório |
| Licença do código | Pendente | Definir antes de tornar o repositório público |

## Antes de marcar uma versão reproduzível

1. Concluir o preenchimento das notas da Release da VM.
2. Confirmar que as três partes podem ser extraídas corretamente pelo 7-Zip.
3. Calcular e publicar os hashes SHA-256 das partes e da OVA remontada.
4. Importar a OVA em uma instalação independente do VirtualBox.
5. Executar ao menos `preflight.sh`, `pingall`, um teste de contenção ARP e um teste de failover.
6. Criar uma tag estável, por exemplo `v1.0.0` ou `vm-v1.0.0`.
7. Definir a licença e revisar os documentos de terceiros antes de tornar o repositório público.

Até essas verificações terminarem, a Release deve permanecer como rascunho.
