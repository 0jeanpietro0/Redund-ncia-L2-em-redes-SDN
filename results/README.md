# Resultados

Use uma pasta por data e cenário, por exemplo:

```text
results/raw/2026-09-10-sdn-1s4h/
├── commands.txt
├── controller.log
├── flows-s1.txt
├── ping-h1-h3.txt
└── arp-h1.pcap
```

Arquivos brutos são ignorados pelo Git por padrão para evitar crescimento desnecessário. Resultados consolidados pequenos, tabelas e gráficos aprovados podem ser adicionados em uma pasta futura `results/processed/`.

Cada conjunto deve registrar:

- versão/commit do código;
- topologia usada;
- parâmetros e comandos;
- data e ambiente;
- resultado observado;
- pequena conclusão, limitações e melhorias.
