# Ambiente experimental

A OVA será a referência principal do ambiente, mas as versões exatas também devem ser registradas em texto para auditoria e reprodução futura.

Dentro da VM, execute:

```bash
./scripts/collect-environment-info.sh | tee environment/versions.txt
```

Revisar o arquivo antes do commit para garantir que não contenha hostname, nome de usuário, endereço IP externo ou outro dado pessoal. O script fornecido evita coletar esses campos deliberadamente.

Também é recomendável exportar somente as dependências Python relevantes usadas pelo projeto, sem tokens ou índices privados.
