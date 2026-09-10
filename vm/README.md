# Máquina virtual reproduzível

A OVA do laboratório será publicada como ativo de uma GitHub Release. Isso mantém o histórico Git leve e permite associar a VM a uma versão exata do código.

## Conteúdo esperado

- Linux e versões do ambiente documentadas;
- Open vSwitch;
- Mininet ou Mininet-WiFi conforme o cenário;
- Python e Ryu;
- clone do repositório em um caminho documentado;
- atalhos ou scripts para iniciar controlador e topologias;
- nenhum dado pessoal, token, chave privada ou credencial reutilizada.

## Nomenclatura sugerida

```text
arp-proxy-sdn-lab-v1.0.0.ova
arp-proxy-sdn-lab-v1.0.0.ova.sha256
```

Se houver partes:

```text
arp-proxy-sdn-lab-v1.0.0.ova.000.part
arp-proxy-sdn-lab-v1.0.0.ova.001.part
arp-proxy-sdn-lab-v1.0.0.ova.parts.sha256
arp-proxy-sdn-lab-v1.0.0.ova.sha256
```

## Remontagem

No Linux, dentro da pasta dos arquivos:

```bash
sha256sum -c arp-proxy-sdn-lab-v1.0.0.ova.parts.sha256
cat arp-proxy-sdn-lab-v1.0.0.ova.*.part > arp-proxy-sdn-lab-v1.0.0.ova
sha256sum -c arp-proxy-sdn-lab-v1.0.0.ova.sha256
```

Depois, importe a OVA pelo VirtualBox e siga o README que estará disponível na área de trabalho da VM.
