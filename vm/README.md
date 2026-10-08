# Máquina virtual do laboratório

A máquina virtual utilizada no trabalho foi criada no **VirtualBox** e é distribuída por uma **GitHub Release**, não por um commit comum. Como o arquivo ultrapassa o limite individual de um ativo, ele foi compactado e dividido em três partes com o 7-Zip.

## Estado atual

As partes `mn.7z.001`, `mn.7z.002` e `mn.7z.003` foram carregadas em uma Release ainda em rascunho. Enquanto a Release não tiver tag, notas completas e verificação final, ela não deve ser tratada como versão estável.

Página das versões:

<https://github.com/0sardinha0/Redund-ncia-L2-em-redes-SDN/releases>

## Download e extração no Windows

1. Instale o 7-Zip.
2. Baixe **todas** as partes da mesma Release.
3. Coloque `.001`, `.002` e `.003` na mesma pasta.
4. Clique com o botão direito somente em `mn.7z.001`.
5. Selecione **7-Zip → Extrair aqui**.
6. Não tente abrir ou extrair as partes `.002` e `.003` separadamente.
7. Aguarde a reconstrução do conteúdo original.

As três partes somadas continuam ocupando aproximadamente o mesmo espaço do arquivo original. A divisão reduz o tamanho de cada ativo; ela não reduz necessariamente o tamanho total.

## Verificação SHA-256 no Windows

No PowerShell:

```powershell
Get-FileHash ".\mn.7z.001" -Algorithm SHA256
Get-FileHash ".\mn.7z.002" -Algorithm SHA256
Get-FileHash ".\mn.7z.003" -Algorithm SHA256
```

Compare os valores com os hashes publicados nas notas da Release. Depois da extração, também verifique o hash da OVA:

```powershell
Get-FileHash ".\mn.ova" -Algorithm SHA256
```

O SHA-256 funciona como uma impressão digital: valores idênticos indicam que o conteúdo baixado corresponde ao arquivo publicado.

## Importação no VirtualBox

1. Abra o VirtualBox.
2. Acesse **Arquivo/Ferramentas → Importar Appliance**.
3. Selecione o arquivo `.ova` extraído.
4. Revise memória, CPUs, armazenamento e adaptadores de rede.
5. Escolha um novo endereço MAC para os adaptadores caso o VirtualBox ofereça essa opção.
6. Conclua a importação e inicie a VM.
7. Abra o terminal dentro da VM e localize o repositório.
8. Execute o roteiro mínimo abaixo.

## Validação mínima dentro da VM

```bash
cd Redund-ncia-L2-em-redes-SDN
git status
git rev-parse HEAD
./scripts/preflight.sh
sudo mn -c
```

Terminal 1:

```bash
./scripts/run-controller.sh controller/arp_proxy_v3_7.py
```

Terminal 2:

```bash
./scripts/run-topology.sh topologies/topologia_arp_proxy_anel_3s_6h.py
```

No Mininet:

```text
mininet> pingall
mininet> h1 ping -c 20 10.0.0.3
mininet> link s1 s2 down
mininet> h1 ping -c 20 10.0.0.3
mininet> link s1 s2 up
mininet> exit
```

Depois:

```bash
./scripts/cleanup-mininet.sh
```

Para reproduzir todos os cenários, consulte [`../docs/TEST_PLAN.md`](../docs/TEST_PLAN.md).

## Preparação de uma nova versão no Windows

O script abaixo calcula o SHA-256 e cria volumes de 1900 MiB usando o 7-Zip:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\preparar-ova-windows.ps1 -OvaPath "C:\CAMINHO\mn.ova"
```

Também é possível configurar manualmente o 7-Zip:

| Campo | Valor |
|---|---|
| Formato | `7z` |
| Método | `LZMA2` ou `Armazenar` |
| Nível | Máximo para tentar reduzir; Armazenar para maior velocidade |
| Dividir em volumes | `1900M` |

Como a OVA já contém um disco virtual otimizado, a compressão pode reduzir pouco. O campo `1900M` é o responsável por criar partes menores.

## Segurança antes de publicar

- utilizar uma cópia da VM;
- remover tokens, chaves, credenciais Git, arquivos pessoais e históricos;
- não reutilizar senha pessoal em usuário de demonstração;
- desligar a VM completamente antes da exportação;
- importar e testar a OVA em outro computador;
- publicar somente as partes, checksums e notas necessárias.

O checklist completo está em [`../docs/OVA_RELEASE_CHECKLIST.md`](../docs/OVA_RELEASE_CHECKLIST.md).
