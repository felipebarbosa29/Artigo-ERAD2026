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

A infraestrutura é definida via *Infrastructure as Code* (IaC) através do arquivo `Vagrantfile`, que automatiza a criação de 4 instâncias virtuais (Ubuntu 22.04 Server). O script realiza a configuração da rede interna (Host-Only) e o *provisioning* automático das dependências do OpenMPI em todos os nós.

### Procedimento de Instalação e Setup

1. Abra o **PowerShell como Administrador** e navegue até a raiz deste diretório.
2. Caso ainda não possua o Vagrant instalado, execute o comando via Gerenciador de Pacotes do Windows (`winget`):
   ```powershell
   winget install --id Hashicorp.Vagrant
   ```
   *Nota: Pode ser necessário reiniciar o terminal após a instalação para atualizar as variáveis de ambiente.*

3. Inicie o provisionamento do cluster:
   ```bash
   vagrant up
   ```
4. O processo realizará automaticamente o download da *box* oficial do Ubuntu, a configuração dos adaptadores de rede e o deploy dos scripts de instalação. Aguarde a conclusão da subida dos 4 nós (`node1`, `node2`, `node3`, `node4`).

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

![Tempo de envio (broadcast) no cluster VirtualBox](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/Afs6BUGPmEE5XAitlhI0SN-images_1783091604522_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNl93b3JraW5nL3ZpcnR1YWxib3gvZ3JhZmljb3MvY2hhcnRfb3N1X2JjYXN0.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94L0FmczZCVUdQbUVFNVhBaXRsaEkwU04taW1hZ2VzXzE3ODMwOTE2MDQ1MjJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmw5M2IzSnJhVzVuTDNacGNuUjFZV3hpYjNndlozSmhabWxqYjNNdlkyaGhjblJmYjNOMVgySmpZWE4wLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTgzMDI5NzYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=HynAetmBBGG9G~Pm9WgsUJ-jIwX3~DAi4EiPv0gwBq3zCO850PRpCKnAxVSlsTQQ77PZJ1fEJVsVfuzlgD49ue2-kda9wm7EtPq555jhFIQJG-1thDzXw00Z4-Zs7uFYJO0dJkR40VEyneKFXVOxF1NYhjEaX2~GeAk6MnMVZXiOLhJxjHLWc2yXtRxtNuqzQGwsrEmBd51aQHajl9V1YdcAT~1Q63CX4wQAE7YxZ6e4zzjGDiJo-7dsiZQENpjrR1QMk5nScn1PVmresF6AHhlBDd97b0pBVtDuP8Wg1YPN1ojUZ8nzyutFMWOEJ8ydAjfXG9G0KwlZN3N5cbTpIg__)

Para detalhes dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
```
