# Códigos-Fonte Modificados

Este diretório contém as versões customizadas dos benchmarks **OSU Micro-Benchmarks (v7.3)** utilizados nos experimentos deste laboratório.

## Motivação das Modificações

Normalmente, esses testes mostram apenas a velocidade da rede. Modificamos o código para que ele também informe o nome da máquina onde cada tarefa está rodando. Isso ajuda a conferir se o MPI distribuiu os processos corretamente entre as máquinas virtuais ou os servidores na nuvem.

## Arquivos Modificados

### 1. `osu_bcast.c`
- **Alteração:** Inserção de um bloco de código após a inicialização do ambiente MPI (`MPI_Init`).
- **Funcionalidade:** 
  - Captura o nome da máquina (`gethostname`).
  - Implementa uma barreira de sincronização (`MPI_Barrier`) para garantir que todos os nós estejam prontos.
  - Imprime a tag `[Virtual Box TOPO]` seguida do Rank e do Hostname correspondente.
- **Objetivo:** Confirmar visualmente a distribuição dos processos nas 4 VMs do cluster local antes do início da coleta de dados.

### 2. `osu_latency.c`
- **Alteração:** Implementação de lógica similar de identificação de host.
- **Funcionalidade:** Exibe o mapeamento dos dois processos envolvidos no teste *ping-pong*.
- **Objetivo:** Validar o cenário de execução inter-regional na AWS, garantindo que o Rank 0 esteja na Virgínia e o Rank 1 no Oregon (ou vice-versa), conforme definido no `hostfile`.

## Como Compilar

Para utilizar estas versões modificadas, substitua os arquivos originais nos diretórios do Osu Benchmark e proceda com a compilação padrão:

```bash
./configure CC=mpicc --prefix=/usr/local
make
sudo make install
```

