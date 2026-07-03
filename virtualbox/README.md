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

## 2. Execução dos Experimentos

Após o provisionamento, os benchmarks do OSU Micro-Benchmarks já estarão compilados e prontos para uso. Você pode executar os testes diretamente de `node1`.

1. Acesse o nó principal (`node1`) via SSH:
   ```bash
   vagrant ssh node1
   ```
2. Os executáveis dos benchmarks estão em `/opt/osu-micro-benchmarks-7.3/mpi/pt2pt/blocking/` (para `osu_latency`), `/opt/osu-micro-benchmarks-7.3/mpi/collective/blocking/` (para `osu_bcast`, `osu_alltoall`), etc.
3. Execute os benchmarks variando o número de processos (`-np`). Exemplo para `osu_latency` com 2 processos:
   ```bash
   mpirun --hostfile /home/vagrant/hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node -np 2 /usr/local/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/blocking/osu_latency -i 100 -x 10
   ```
   *Para outros benchmarks, ajuste o caminho do executável e os parâmetros conforme necessário.*

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

![Tempo de envio (broadcast) no cluster VirtualBox](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/0avdAQ0Fpxlt6SxNLT67X6-images_1783089271115_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNl93b3JraW5nL3ZpcnR1YWxib3gvZ3JhZmljb3MvY2hhcnRfb3N1X2JjYXN0.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94LzBhdmRBUTBGcHhsdDZTeE5MVDY3WDYtaW1hZ2VzXzE3ODMwODkyNzExMTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmw5M2IzSnJhVzVuTDNacGNuUjFZV3hpYjNndlozSmhabWxqYjNNdlkyaGhjblJmYjNOMVgySmpZWE4wLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTgzMDI5NzYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=lGNNL~ytAckqniCeYTFyO2A3A6GBcKxOwQsX~TF8IJ7V2j3y4lqwqzhugggFu6xr5g5AtVs20tM5~6xbOsBR-xN5aDKtg1Bw1yNDfiww~3IZzPjxTpRX5x5fmTdtC9xHkzm9jemBhDken901ZRNLIbPZrZS6Lgf753ExztVZNafKSTi6llsPPSLBPY8-I9kZLGV2jbVabSGzctUy~YGw50ynMBtNtQuCif5BaJCkjdRNcmtWNnFQZ4JSpanO3VRIfnKNRE7Ww4BhbthdZ92j~-lKl9AGte5YMbkqLo-Nz1b8iVxiBQ~WVQAilUXCpWTRnzXGuzjV1qeir-41l9lDAw__)

Para detalhes dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
```
