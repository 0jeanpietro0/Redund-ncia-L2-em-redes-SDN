# Manifesto dos arquivos recebidos

Os hashes abaixo foram calculados com SHA-256 antes da organização inicial. Eles permitem conferir se os arquivos de origem foram preservados durante a reorganização.

| Arquivo recebido | Destino em português | SHA-256 de origem |
|---|---|---|
| `topologia_arp_proxy_v3.py` | `reproducao/codigo/topologias/topologia_arp_proxy_v3.py` | `4148bdd4cbc58623a1f7f5dfc98bf847fe1865579a56ddf4b66d16acc0fcef18` |
| `topologiav2.docx` | `documentacao/desenvolvimento/topologiav2.docx` | `68f6b45c44dadfec818f0899587fcd5cbeb50fb1054d3269c94acce45dd32233` |
| `arp_proxy_v3.py` | `reproducao/codigo/controlador/arp_proxy_v3.py` | `f0ec7978a57418c79fdf33b202d7937b4fc52e58f92deacfbaeb098b7ac3f104` |
| `ARP PROXY v2.docx` | `documentacao/desenvolvimento/ARP_PROXY_v2.docx` | `c5e76283c8dab08d10681dbad4d86b28987a2e555850f19ffb9be31bbe51fd8f` |
| `ARP PROXY v1.docx` | `documentacao/desenvolvimento/ARP_PROXY_v1.docx` | `c93dc12e6da5c0c4f29362b070cbf442f3d8b56950ab8722b60f7640a5e41c14` |
| `Manuscrito Balanceamento de Carga...pdf` | `documentacao/referencias/Manuscrito_Balanceamento_de_Carga_SDN.pdf` | `7d8d82bc2612232426e3ef02b7d9cd7b0cf927a24bba5fefb3df783af46ff350` |
| `Manual_TCC...pdf` | `documentacao/referencias/Manual_TCC_IFSULDEMINAS.pdf` | `a568794d6ec819ae865f77b4270ac60bbf4ebf547ba6b52e679ec2af410fecff` |
| `Manual_TCC...docx` | `documentacao/referencias/Manual_TCC_IFSULDEMINAS.docx` | `4091f5f110e5e2445bfea74006ed9c7a36a29a972daa6339f1dab1fbbaf44452` |

## Como registrar um novo artefato

1. Preserve o arquivo original sem sobrescrever uma versão anterior.
2. Calcule o hash:

   ```bash
   sha256sum CAMINHO_DO_ARQUIVO
   ```

3. Adicione uma linha a este manifesto.
4. Informe a versão do controlador ou da topologia no nome ou em um README próximo.
5. Registre a inclusão no histórico de alterações.

Arquivos históricos e referências não são dependências para executar os experimentos. Se uma referência não puder ser redistribuída, remova o binário e mantenha o link oficial e a referência bibliográfica.
