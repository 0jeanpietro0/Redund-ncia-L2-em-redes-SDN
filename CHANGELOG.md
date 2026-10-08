# Histórico de alterações

Este arquivo registra as mudanças relevantes do projeto.

## Não publicado — alinhamento com a versão final do TCC

### Adicionado

- Controladores `arp_proxy_v3_5.py`, `arp_proxy_v3_6.py` e `arp_proxy_v3_7.py`.
- Topologias convencional e SDN de um e dois switches.
- Topologias em anel sem STP/RSTP, com STP, com RSTP e com ARP Proxy.
- Topologias em malha completa K4 com RSTP e com ARP Proxy v3.7.
- Roteiro operacional completo para todos os ensaios descritos no TCC.
- Documentação das versões do controlador e das finalidades de cada topologia.
- Instruções de publicação e extração da OVA dividida com 7-Zip no Windows.
- Preparação da máquina virtual em uma GitHub Release ainda em rascunho.

### Alterado

- README atualizado com o título final, objetivo, delimitação, arquivos, comandos e síntese dos resultados.
- Estado dos artefatos atualizado para remover pendências que já foram resolvidas.
- Scripts de execução preparados para receber o controlador e a topologia como parâmetros.
- Verificação do ambiente ampliada para todos os arquivos Python do projeto.
- Documentação da VM adaptada ao VirtualBox e ao processo utilizado no Windows.

### Removido

- Cópias duplicadas dos documentos históricos dentro de `controller/`.
- Arquivo `controller/arp_proxy_v3.docx`, que continha o mesmo conteúdo do código Python com extensão incorreta.

### Pendente

- Publicar a Release da VM com tag, notas completas e SHA-256.
- Testar a importação da OVA em outro computador.
- Definir a licença do código.
- Revisar a redistribuição das referências acadêmicas antes de abrir o repositório.

## v0.1.0-snapshot

- Estrutura inicial do repositório.
- Snapshot do controlador ARP Proxy v3.
- Topologia inicial de um switch e quatro hosts.
- Documentos históricos e referências recebidas.
- Scripts iniciais de verificação, execução, limpeza e preparação da OVA.
