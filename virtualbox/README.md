# Ambiente Local (VirtualBox)

Este diretório contém os recursos necessários para provisionar e testar um cluster local utilizando o **VirtualBox** e o **Vagrant**, conforme descrito no artigo.

## Requisitos de Sistema

Para replicar este laboratório, o computador hospedeiro deve possuir:
- **Memória RAM:** Mínimo de 8 GB (O cluster consumirá aproximadamente 4,5 GB, incluindo o gerenciamento do VirtualBox).
- **Software:** VirtualBox (versão 7.0 ou superior) e Vagrant instalados.

## 1. Provisionamento do Cluster

O arquivo `Vagrantfile` incluído neste diretório automatiza a criação de 4 máquinas virtuais (Ubuntu 22.04 LTS), configurando a rede interna e instalando as bibliotecas MPI necessárias.

**Passo a passo:**
1. Abra o terminal (ou Prompt de Comando/PowerShell) neste diretório.
2. Execute o comando para iniciar a criação das máquinas:
```bash
   vagrant up
```
3. Aguarde o download da imagem do sistema operacional e a configuração automática dos 4 nós (`node1`, `node2`, `node3`, `node4`).

## 2. Execução do Experimento (Broadcast)

O experimento relatado no artigo utiliza o benchmark `osu_bcast` para analisar o tempo de envio de dados em operações de comunicação coletiva (*broadcast*).

1. Acesse o nó principal (node1) via SSH:
```bash
   vagrant ssh node1
```
2. Crie um arquivo chamado `hostfile` contendo os IPs da rede interna:
```text
   192.168.56.101
   192.168.56.102
   192.168.56.103
   192.168.56.104
```
3. Execute o benchmark variando o número de processos (`-np`). Exemplo para 8 processos:
```bash
   mpirun --hostfile hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node -np 8 ./osu_bcast -i 100 -x 10
```
## 3. Resultados

O gráfico abaixo, apresentado no artigo, ilustra o aumento do tempo de envio de dados conforme o número de processos simultâneos aumenta, demonstrando o impacto da disputa por recursos no processador do hospedeiro.

![Tempo de envio (broadcast) no cluster VirtualBox](graficos/grafico_latencia_aws.png)

Para detalhes dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.