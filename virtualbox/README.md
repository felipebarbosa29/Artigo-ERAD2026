# Ambiente Local (VirtualBox)

Este diretório contém os recursos necessários para provisionar e testar um cluster local utilizando o **VirtualBox** e o **Vagrant**, conforme detalhado no artigo.

## Requisitos de Sistema

O laboratório foi criado em uma máquina com 32 GB de memória RAM, um SSD de 500 GB, um processador Intel Core i7-1165G7 e executando o sistema operacional Windows 11.

A tabela abaixo detalha o consumo estimado de recursos:

| Componente            | Consumo (GB) | Disco (GB)    |
| :-------------------- | :----------- | :------------ |
| Windows (Hospedeiro)  | 4,0          | 64,0          |
| 4 VMs Ubuntu (1 GB)   | 3,5 – 4,0    | 37,0          |
| Gerenciamento         | 0,5          | 0,2 – 0,3     |
| **Total Estimado**    | **8,0 – 8,5**| **101,2 – 101,3** |

## 1. Provisionamento do Cluster

A infraestrutura é definida como código (*Infrastructure as Code*) no arquivo `Vagrantfile`. Ele automatiza a criação das 4 máquinas virtuais, configura a rede interna isolada e instala todas as dependências do OpenMPI e do OSU Micro-Benchmarks.

### Instalação e Configuração

1. Abra o **PowerShell como Administrador** e navegue até esta pasta.
2. Inicie o laboratório:
   ```bash
   vagrant up
   ```
O Vagrant fará o download do Ubuntu e configurará as ferramentas automaticamente. O `Vagrantfile` já injeta os códigos modificados do autor durante a compilação.

### Gerenciando o Laboratório

Como o laboratório roda na sua máquina, é importante saber como liberar recursos (RAM e CPU) quando não estiver estudando:

*   **Ligar o Cluster:** `vagrant up`
*   **Desligar (Pausar):** `vagrant halt` (recupera a RAM do seu computador).
*   **Excluir Tudo:** `vagrant destroy -f` (apaga as máquinas e discos virtuais).

## 2. Execução dos Experimentos

O foco no ambiente local é a análise de latência em operações coletivas usando o benchmark de Broadcast (`osu_bcast`). 

### Como Rodar o Teste (Código Modificado)

Para validar a distribuição dos processos entre os nós (auditoria de Rank vs Hostname), o OSU já foi compilada com as modificações.

1. Acesse o nó principal via SSH:
   ```bash
   vagrant ssh node1
   ```

2. Execute o benchmark customizado:
   ```bash
   mpirun -np 4 --hostfile ~/hostfile --oversubscribe --mca btl tcp,self --mca btl_tcp_if_include enp0s8 --mca mpi_yield_when_idle 1 /usr/local/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_bcast
   ```

*Nota: Ao rodar este comando, você verá no cabeçalho as linhas **[Virtual Box TOPO]** identificando qual VM está processando cada Rank.

### Explicação dos Parâmetros

*   `-np 4`: Lança 4 processos MPI (1 por nó). Use 8 ou 16 para testar com outros processos.
*   `--hostfile ~/hostfile`: Lista de IPs das máquinas virtuais.
*   `--oversubscribe`: Permite rodar mais processos do que núcleos de CPU.
*   `--mca btl_tcp_if_include enp0s8`: Força o uso da interface de rede privada do VirtualBox (`enp0s8`).
*   `--mca mpi_yield_when_idle 1`: Diz para o MPI não "segurar" o processador enquanto espera uma mensagem. Ele libera a CPU para outras tarefas do seu computador.

## 3. Dados e Visualização

Os resultados estão no arquivo `dados/dados_vbox.csv`. Para gerar os gráficos da Figura 1 do artigo:

1. Instale as dependências: `pip install matplotlib pandas`
2. Entre na pasta: `cd virtualbox/scripts/`
3. Execute: `python3 plot_latencia.py`

Os gráficos serão gerados na pasta `virtualbox/graficos/`.

![Desempenho de Broadcast no VirtualBox](graficos/chart_osu_bcast.png)

