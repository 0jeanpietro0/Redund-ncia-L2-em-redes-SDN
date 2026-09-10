# Checklist da OVA

## Antes da exportação

- [ ] Trabalhar em uma cópia da VM, não na única VM do projeto.
- [ ] Confirmar que controlador, topologias, scripts e README estão dentro da VM.
- [ ] Executar os testes mínimos e salvar evidências sem dados pessoais.
- [ ] Criar um usuário exclusivo para demonstração, sem reutilizar senha pessoal.
- [ ] Remover tokens, chaves privadas, credenciais Git, redes Wi-Fi, VPNs e arquivos pessoais.
- [ ] Limpar históricos de shell, navegador, editores e arquivos recentes.
- [ ] Remover ou regenerar identificadores e chaves da máquina que não devam ser clonados.
- [ ] Limpar caches e arquivos temporários desnecessários.
- [ ] Desligar completamente a VM; não exportar em estado salvo.
- [ ] Registrar versões de SO, kernel, Python, Ryu, Mininet, OVS e VirtualBox.

## Exportação sugerida

Pela interface do VirtualBox, usar **Arquivo > Exportar Appliance** e escolher o formato OVA/OVF compatível. Pela linha de comando, adaptar:

```bash
VBoxManage export "NOME_DA_VM" --output arp-proxy-sdn-lab-v1.0.0.ova --ovf20
```

Após exportar:

```bash
./scripts/prepare-ova-release.sh /caminho/arp-proxy-sdn-lab-v1.0.0.ova
```

## Teste independente

- [ ] Importar a OVA em outro computador ou em uma instalação limpa do VirtualBox.
- [ ] Confirmar que a placa de rede inicia com uma configuração segura.
- [ ] Executar `preflight.sh`.
- [ ] Executar o controlador e todas as topologias publicadas.
- [ ] Confirmar `pingall`, ping direcionado, fluxos e capturas ARP.
- [ ] Desligar a VM e comparar o SHA-256 do arquivo distribuído.

## Publicação

- [ ] Criar uma tag específica, por exemplo `vm-v1.0.0`.
- [ ] Anexar a OVA ou todas as partes geradas à mesma GitHub Release.
- [ ] Anexar os arquivos de checksum.
- [ ] Informar VirtualBox mínimo testado, RAM, CPUs e espaço livre necessários.
- [ ] Documentar usuário de demonstração e a política de senha sem expor credenciais pessoais.
- [ ] Incluir instruções de importação, execução, remontagem de partes e verificação SHA-256.
- [ ] Não adicionar OVA, VDI, VMDK ou OVF ao histórico Git.
