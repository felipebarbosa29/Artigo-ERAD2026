# Ambiente Local (VirtualBox)

Este diretório contém os recursos necessários para provisionar e testar um cluster local utilizando o **VirtualBox** e o **Vagrant**, conforme descrito no artigo.

## Requisitos de Sistema

Para a replicação dos experimentos em ambiente local, é necessário um computador hospedeiro com as seguintes características:

- **Sistema Operacional:** Windows 11
- **Processador:** Intel Core i7
- **Memória RAM:** 32 GB
- **Armazenamento:** SSD de 500 GB
- **Software:** VirtualBox (versão 7.0) e Vagrant instalados.

A Tabela 2, extraída do artigo, detalha o consumo estimado de recursos para o ambiente de virtualização:

| Componente            | Consumo (GB) | Disco (GB)    |
| :-------------------- | :----------- | :------------ |
| Windows 11 (base)     | 4,0          | 64,0          |
| 4 VMs Ubuntu (1 GB cada) | 3,5 – 4,0    | 37,0          |
| Gerenciamento VBox/Rede | 0,5          | 0,2 – 0,3     |
| **Total Estimado**    | **8,0 – 8,5**| **101,2 – 101,3** |

## 1. Provisionamento do Cluster

O arquivo `Vagrantfile` incluído neste diretório automatiza a criação de 4 máquinas virtuais (Ubuntu 22.04 Server), configurando a rede interna e instalando as bibliotecas MPI necessárias.

**Passo a passo:**
1. Abra o terminal (ou Prompt de Comando/PowerShell) neste diretório.
2. Execute o comando para iniciar a criação das máquinas:
   ```bash
   vagrant up
   ```
3. Aguarde o download da imagem do sistema operacional e a configuração automática dos 4 nós (`node1`, `node2`, `node3`, `node4`).

## 2. Execução dos Experimentos (Benchmark de Broadcast)

No ambiente local, o foco dos testes foi a análise de latência em operações coletivas de **Broadcast**, utilizando o benchmark `osu_bcast`.

### Procedimento de Execução

1. Acesse o nó principal (`server1` ou `node1`) via SSH:
   ```bash
   vagrant ssh node1
   ```

2. Navegue até o diretório dos benchmarks coletivos:
   ```bash
   cd /home/vagrant/osu-micro-benchmarks-7.3/c/mpi/collective/blocking
   ```

3. Execute o benchmark variando a quantidade de processos (`-np`) para 4, 8 e 16. Exemplo de comando utilizado:
   ```bash
   mpirun -np 4 --hostfile ~/hostfile --oversubscribe --mca btl tcp,self --mca btl_tcp_if_include 192.168.56.0/24 --mca mpi_yield_when_idle 1 ./osu_bcast
   ```

### Detalhamento dos Parâmetros

Para garantir a precisão dos resultados e a correta comunicação entre os nós virtuais, os seguintes parâmetros foram empregados no `mpirun`:

- `-np [4, 8, 16]`: Define o número de processos MPI a serem lançados no cluster.
- `--hostfile ~/hostfile`: Especifica o arquivo contendo os endereços IP dos nós (`node1` a `node4`), permitindo que o MPI distribua os processos entre as VMs.
- `--oversubscribe`: Permite o lançamento de mais processos do que o número de slots (núcleos) disponíveis. Essencial para testar a contenção de recursos no hospedeiro.
- `--mca btl tcp,self`: Força o uso da camada de transporte TCP para comunicação entre nós e `self` para comunicação interna, garantindo que o tráfego passe pela pilha de rede virtualizada.
- `--mca btl_tcp_if_include 192.168.56.0/24`: Restringe a comunicação MPI à interface de rede interna do VirtualBox (Host-Only), evitando interferências de outras interfaces.
- `--mca mpi_yield_when_idle 1`: Instrui o processo MPI a liberar o processador quando estiver em espera, otimizando o escalonamento em ambientes virtualizados onde há disputa por CPU física.
- `./osu_bcast`: O executável do benchmark de broadcast que mede a latência média de envio de mensagens de diferentes tamanhos para todos os nós do grupo.

## 3. Geração dos Gráficos

Os scripts Python para plotagem dos gráficos estão localizados na pasta `scripts/`.

1.  Certifique-se de que os dados dos experimentos (`.csv`) estejam na pasta `dados/`.
2.  No seu host (fora da VM), navegue até o diretório `virtualbox/scripts/`.
3.  Execute o script de plotagem. Por exemplo, para gerar o gráfico de latência:
    ```bash
    python3 plot_latencia.py
    ```
    *Isso gerará os arquivos de imagem (`.png`) e PDF (`.pdf`) na pasta `graficos/`.*

## 4. Resultados

O gráfico abaixo, apresentado no artigo, ilustra o aumento do tempo de envio de dados conforme o número de processos simultâneos aumenta, demonstrando a disputa por recursos no processador do hospedeiro.

![Tempo de envio (broadcast) no cluster VirtualBox](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/yi82sx5kGmsp1X896pVPsU-images_1783090510451_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNl93b3JraW5nL3ZpcnR1YWxib3gvZ3JhZmljb3MvY2hhcnRfb3N1X2JjYXN0.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94L3lpODJzeDVrR21zcDFYODk2cFZQc1UtaW1hZ2VzXzE3ODMwOTA1MTA0NTFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmw5M2IzSnJhVzVuTDNacGNuUjFZV3hpYjNndlozSmhabWxqYjNNdlkyaGhjblJmYjNOMVgySmpZWE4wLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTgzMDI5NzYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=awoh4K~r-iDGzXZxagtJBWbl8S722mQpIwblDhnGjP1WCr5ET86XXelDHrLAUguLiXnp1H7qanErZVZXiIW-cQBnNLZTd0dZ27pSe4EWOfI-nqIvhiBKPkUaIu9Fz7NuF-V1ahje-8nV5p7UFyt6~yFTe-6w3XFEEIXXiVGPcu4PUeVhj1fMjjNBx7GaeMw9wJejVxoQ7B1FtN61b1OuytjZWxt6UNY6-l39b4bvUwPoe-o1X0RNMbW40ZrlDhcQKopSe6CWO6fisH2LvyzHpls8Gw6lIqL6DZTeEnb0mc4NW93UvPLPzpqgiSJebIgucMWMXX2Wgq~0rxTosNE35w__)

Para detalhes dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
```
