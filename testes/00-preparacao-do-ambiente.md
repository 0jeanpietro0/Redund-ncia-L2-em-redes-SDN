# 00 — Preparação do ambiente

Execute esta etapa antes de **cada** rodada. Ela evita que processos, interfaces, entradas ARP ou fluxos de uma execução anterior contaminem o resultado.

## 1. Fixar a versão

A partir da raiz do repositório:

```bash
git status --short
git rev-parse HEAD
```

Para uma rodada oficial, o estado deve estar limpo. Se houver alterações intencionais, faça um commit antes do teste; se não forem intencionais, investigue sem descartá-las automaticamente.

## 2. Verificar os programas

```bash
./utilitarios/verificar-ambiente.sh
```

O utilitário verifica Python, Ryu, Mininet, Open vSwitch, `tcpdump`, `iperf`, Git e a sintaxe dos arquivos Python presentes em `reproducao/codigo/`.

## 3. Limpar a emulação anterior

Não execute a limpeza enquanto uma rodada válida estiver ativa.

```bash
./utilitarios/limpar-mininet.sh
```

## 4. Criar a pasta da rodada

Substitua `nome-do-cenario` por um identificador curto, sem espaços ou acentos:

```bash
export PASTA_RESULTADO="$(./utilitarios/criar-pasta-de-teste.sh nome-do-cenario)"
printf 'Resultados em: %s\n' "$PASTA_RESULTADO"
```

O utilitário cria `commit.txt`, `ambiente.txt` e um modelo `COMANDOS.md`.

## 5. Registrar os arquivos usados

Edite `COMANDOS.md` e informe:

- caminho do controlador;
- caminho da topologia;
- parâmetros de largura de banda e atraso;
- tecnologia do cenário: sem STP, STP, RSTP ou SDN;
- data, horário e ordem exata dos comandos.

Calcule também os hashes:

```bash
sha256sum CAMINHO_DO_CONTROLADOR CAMINHO_DA_TOPOLOGIA \
  | tee "$PASTA_RESULTADO/hashes-dos-artefatos.txt"
```

Em cenário convencional, retire o caminho do controlador.

## 6. Abrir os terminais

- Terminal 1: controlador Ryu;
- Terminal 2: topologia Mininet;
- Terminal 3: monitoramento e recuperação.

Mantenha `PASTA_RESULTADO` exportada nos terminais que gravarão arquivos. Se abrir novos terminais, repita:

```bash
export PASTA_RESULTADO="CAMINHO_ABSOLUTO_EXIBIDO_ANTERIORMENTE"
```

## 7. Conferir a topologia ao iniciar

Na CLI do Mininet:

```text
mininet> net
mininet> dump
mininet> links
mininet> sh ovs-vsctl show
```

Para mapear as portas de cada switch:

```text
mininet> sh ovs-ofctl -O OpenFlow13 show s1
mininet> sh ovs-ofctl -O OpenFlow13 show s2
mininet> sh ovs-ofctl -O OpenFlow13 show s3
```

Execute apenas os comandos dos switches existentes. Copie o mapeamento para `portas-e-enlaces.txt`, pois ele será necessário nas capturas.

## Pronto para avançar quando

- os programas obrigatórios estiverem disponíveis;
- não houver rede Mininet antiga ativa;
- o commit, os hashes e as versões estiverem registrados;
- a pasta da rodada estiver definida;
- portas e enlaces da topologia tiverem sido conferidos.
