# Ambiente experimental

A OVA será a referência principal do laboratório, mas as versões também devem ser registradas em texto para permitir auditoria e futura reconstrução.

Dentro da VM final, execute a partir da raiz do repositório:

```bash
./utilitarios/coletar-informacoes-do-ambiente.sh \
  | tee reproducao/ambiente/versoes.txt
```

Revise `versoes.txt` antes do commit para garantir que ele não contenha nome de usuário, hostname, endereço IP externo ou outra informação pessoal. O utilitário evita coletar esses campos deliberadamente.

Registre também, de forma manual:

- versão do VirtualBox usada para exportar e importar;
- quantidade de vCPU e RAM da VM;
- tamanho do disco virtual;
- tipo das placas de rede virtuais;
- commit do repositório presente na OVA;
- data em que todos os testes foram repetidos.
