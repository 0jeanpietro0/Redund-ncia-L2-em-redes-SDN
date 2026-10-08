# Checklist de publicação da máquina virtual

## 1. Antes da exportação

- [ ] Trabalhar em uma cópia da VM.
- [ ] Atualizar o repositório dentro da VM para o commit que será documentado.
- [ ] Executar `./scripts/preflight.sh`.
- [ ] Executar ao menos os testes mínimos de conectividade, contenção ARP e failover.
- [ ] Registrar as versões com `./scripts/collect-environment-info.sh`.
- [ ] Remover tokens, chaves privadas, credenciais Git, VPNs, redes Wi-Fi e arquivos pessoais.
- [ ] Limpar históricos de shell, navegador, editores e arquivos recentes.
- [ ] Criar um usuário de demonstração sem reutilizar senha pessoal.
- [ ] Remover caches e arquivos temporários desnecessários.
- [ ] Desligar completamente a VM; não exportar em estado salvo.

## 2. Exportar pelo VirtualBox no Windows

1. Abra o VirtualBox.
2. Selecione **Arquivo/Ferramentas → Exportar Appliance**.
3. Escolha a máquina do laboratório.
4. Utilize o formato OVA.
5. Salve com nome versionado, por exemplo `arp-proxy-sdn-lab-v1.0.0.ova`.

## 3. Gerar SHA-256

No PowerShell:

```powershell
$ova = "C:\CAMINHO\arp-proxy-sdn-lab-v1.0.0.ova"
$arquivo = Get-Item -LiteralPath $ova
$hash = (Get-FileHash -LiteralPath $ova -Algorithm SHA256).Hash.ToLower()
"$hash  $($arquivo.Name)" |
    Set-Content -LiteralPath "$ova.sha256" -Encoding ascii
```

## 4. Dividir quando ultrapassar o limite individual

Pelo script do repositório:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\preparar-ova-windows.ps1 `
    -OvaPath "C:\CAMINHO\arp-proxy-sdn-lab-v1.0.0.ova"
```

Ou manualmente no 7-Zip:

- formato: `7z`;
- método: `LZMA2` ou `Armazenar`;
- divisão em volumes: `1900M`;
- todas as partes devem permanecer juntas.

O tamanho total pode continuar próximo do original. O objetivo da divisão é manter cada ativo abaixo do limite individual da Release.

## 5. Teste independente

- [ ] Copiar ou baixar novamente todas as partes.
- [ ] Colocar `.001`, `.002` e `.003` na mesma pasta.
- [ ] Extrair somente `.001` pelo 7-Zip.
- [ ] Comparar os hashes das partes.
- [ ] Comparar o SHA-256 da OVA remontada.
- [ ] Importar a OVA em outro computador ou instalação limpa do VirtualBox.
- [ ] Confirmar CPUs, RAM, armazenamento e adaptadores de rede.
- [ ] Executar `preflight.sh`.
- [ ] Executar o anel SDN com a v3.7.
- [ ] Confirmar `pingall`, fluxos e failover.
- [ ] Executar `sudo mn -c` ao terminar.

## 6. Publicação da Release

- [ ] Remover ou ignorar rascunhos duplicados antes da publicação final.
- [ ] Criar uma tag, por exemplo `vm-v1.0.0`.
- [ ] Usar um título descritivo, como `Máquina virtual do laboratório — v1.0.0`.
- [ ] Anexar todas as partes à mesma Release.
- [ ] Anexar `parts.sha256` e o SHA-256 da OVA.
- [ ] Preencher `vm/RELEASE_NOTES_TEMPLATE.md`.
- [ ] Informar versão do VirtualBox, RAM, CPUs e espaço livre.
- [ ] Documentar a importação e a extração pelo `.001`.
- [ ] Vincular o commit exato do código.
- [ ] Publicar somente após o teste independente.

## 7. O que não deve entrar no Git

- OVA, OVF, VDI, VMDK ou VHD;
- volumes `.7z.001`, `.7z.002` e seguintes;
- senhas, tokens ou chaves;
- capturas e logs grandes sem necessidade acadêmica;
- arquivos pessoais presentes na VM.
