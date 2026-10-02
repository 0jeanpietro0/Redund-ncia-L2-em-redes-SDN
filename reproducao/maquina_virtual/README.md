# Máquina virtual reproduzível

A OVA deve conter o ambiente usado no TCC e uma cópia do repositório no commit correspondente. Ela será publicada como ativo de uma GitHub Release, não como arquivo comum no histórico Git.

O GitHub bloqueia arquivos comuns acima de 100 MiB. Em Releases, cada ativo precisa ter menos de 2 GiB; por isso, o utilitário divide automaticamente uma OVA maior em partes de 1.900 MiB.

## Onde colocar a OVA

Durante a preparação local, coloque o arquivo em:

```text
reproducao/maquina_virtual/arquivos/
```

Essa pasta está preparada no repositório, mas os formatos `.ova`, `.ovf`, `.vdi`, `.vmdk`, `.vhd` e `.vbox` são ignorados pelo Git. Depois da validação, envie a OVA e os checksums para a [página de Releases](https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN/releases).

## Conteúdo esperado na VM

- Linux e versões registradas em `reproducao/ambiente/versoes.txt`;
- Open vSwitch;
- Mininet ou Mininet-WiFi, conforme os scripts finais;
- Python e Ryu compatíveis;
- `tcpdump` e `iperf` usados nos ensaios;
- clone do repositório em um caminho documentado;
- atalhos ou utilitários para controlador e topologias;
- nenhum token, chave privada, credencial reutilizada ou arquivo pessoal.

## Preparação antes da exportação

- [ ] Trabalhar em uma cópia da VM, preservando a original.
- [ ] Atualizar o clone para o commit exato que será marcado na Release.
- [ ] Executar `./utilitarios/verificar-ambiente.sh`.
- [ ] Gerar e revisar `reproducao/ambiente/versoes.txt`.
- [ ] Repetir todos os testes aplicáveis e salvar as evidências.
- [ ] Criar um usuário exclusivo de demonstração, sem senha pessoal reutilizada.
- [ ] Remover tokens, chaves SSH, credenciais Git, redes Wi-Fi, VPNs e arquivos pessoais.
- [ ] Limpar históricos de shell, navegador, editores e arquivos recentes.
- [ ] Limpar caches e temporários desnecessários.
- [ ] Encerrar o Mininet com `sudo mn -c`.
- [ ] Desligar completamente a VM; não exportar um estado salvo.

## Exportação

Pela interface do VirtualBox, use a função **Exportar Appliance** e selecione o formato OVA. Pela linha de comando, adapte:

```bash
VBoxManage export "NOME_DA_VM" \
  --output reproducao/maquina_virtual/arquivos/arp-proxy-sdn-v1.0.0.ova \
  --ovf20
```

Em seguida, gere os checksums e, se necessário, as partes:

```bash
./utilitarios/preparar-ova-para-release.sh \
  reproducao/maquina_virtual/arquivos/arp-proxy-sdn-v1.0.0.ova
```

## Teste independente

1. Importe a OVA em outro computador ou em uma instalação limpa do VirtualBox.
2. Confira vCPU, RAM, disco e modo de rede antes de iniciar.
3. Inicie a VM sem credenciais pessoais.
4. Execute `./utilitarios/verificar-ambiente.sh`.
5. Execute pelo menos `pingall`, ping direcionado e dump dos fluxos.
6. Execute os cenários redundantes, as falhas e os testes K4 que estiverem incluídos.
7. Desligue a VM.
8. Confira novamente o SHA-256 do arquivo que será publicado.

## Remontagem de uma OVA dividida

No Linux, dentro da pasta que contém todas as partes:

```bash
sha256sum -c arp-proxy-sdn-v1.0.0.ova.partes.sha256
cat arp-proxy-sdn-v1.0.0.ova.*.parte > arp-proxy-sdn-v1.0.0.ova
sha256sum -c arp-proxy-sdn-v1.0.0.ova.sha256
```

No Windows PowerShell, a união pode ser feita em modo binário:

```powershell
$partes = Get-ChildItem 'arp-proxy-sdn-v1.0.0.ova.*.parte' | Sort-Object Name
$saida = [System.IO.File]::Create('arp-proxy-sdn-v1.0.0.ova')
try {
  foreach ($parte in $partes) {
    $bytes = [System.IO.File]::ReadAllBytes($parte.FullName)
    $saida.Write($bytes, 0, $bytes.Length)
  }
} finally {
  $saida.Dispose()
}
Get-FileHash 'arp-proxy-sdn-v1.0.0.ova' -Algorithm SHA256
```

Compare o hash exibido com o conteúdo do arquivo `.ova.sha256`.

## Publicação

- [ ] Criar uma tag associada ao commit presente na VM.
- [ ] Usar [MODELO_NOTAS_DA_VERSAO.md](MODELO_NOTAS_DA_VERSAO.md) na descrição.
- [ ] Anexar a OVA ou todas as partes.
- [ ] Anexar os arquivos de checksum.
- [ ] Informar VirtualBox testado, RAM, vCPU e espaço livre necessário.
- [ ] Informar usuário de demonstração sem expor senha pessoal.
- [ ] Marcar como pré-lançamento enquanto houver artefatos pendentes.

Fontes: [GitHub — arquivos grandes](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [GitHub — limites de Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) e [manual do VirtualBox](https://www.virtualbox.org/manual/).
