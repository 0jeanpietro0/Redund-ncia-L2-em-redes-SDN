# Controladores Ryu

Coloque neste diretório cada versão do controlador realmente utilizada nos testes. Não substitua uma versão antiga: mantenha os arquivos separados para preservar a rastreabilidade.

## Conteúdo atual

| Arquivo | Estado | Uso |
|---|---|---|
| `arp_proxy_v3.py` | Incluído | Cenário SDN básico de 1 switch e 4 hosts |
| `arp_proxy_v3_6.py` | Pendente | Contenção de ARP na topologia redundante |
| `arp_proxy_v3_7.py` | Pendente | Detecção de falha e recálculo de caminho |

Os nomes `arp_proxy_v3_6.py` e `arp_proxy_v3_7.py` são recomendações. Se os arquivos originais tiverem outro nome, preserve o nome real e atualize os roteiros em `testes/`.

## Validação ao adicionar uma versão

```bash
python3 -m py_compile reproducao/codigo/controlador/NOME_DO_ARQUIVO.py
sha256sum reproducao/codigo/controlador/NOME_DO_ARQUIVO.py
```

Depois, registre o hash no manifesto, identifique em quais testes a versão foi usada e confirme o comando completo do `ryu-manager`.
