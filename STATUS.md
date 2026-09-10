# Estado dos artefatos

Este arquivo separa o que já foi recebido do que ainda é necessário para uma reprodução completa.

| Artefato | Estado | Observação |
|---|---|---|
| Controlador `arp_proxy_v3.py` | Incluído | Snapshot recebido; possui `idle_timeout=60` |
| Topologia `topologia_arp_proxy_v3.py` | Incluída | Um switch e quatro hosts |
| Documentos ARP Proxy v1/v2 | Incluídos | Histórico do desenvolvimento |
| Documento `topologiav2.docx` | Incluído | Histórico do desenvolvimento |
| Controlador final `v3.6` | Pendente | Necessário para representar os últimos testes documentados |
| Topologia convencional final | Pendente | Necessária para reproduzir a comparação |
| Topologia redundante/múltiplos switches | Pendente | Necessária para validar contenção de ARP nos enlaces internos e redundância |
| Resultados brutos e capturas | Pendente | Logs, `tcpdump`, dumps de fluxos e tabelas |
| Inventário exato da VM | Pendente | Gerar dentro da VM com `scripts/collect-environment-info.sh` |
| OVA sanitizada | Pendente | Publicar como ativo de Release, nunca em um commit comum |
| Licença do código | Pendente | Definir antes de tornar o repositório público |
| Direitos de redistribuição das referências | Revisão necessária | Se não houver permissão, manter apenas links oficiais |

Não criar uma tag de reprodução final enquanto os itens essenciais estiverem pendentes. Uma primeira tag pode ser publicada como `v0.1.0-snapshot` para registrar somente o material recebido.
