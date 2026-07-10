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
2. Se não tiver o Vagrant, instale-o via Gerenciador de Pacotes do Windows:
   ```powershell
   winget install --id Hashicorp.Vagrant
   ```
   *Nota: Pode ser necessário reiniciar o computador para atualizar as variáveis de ambiente.*

3. Inicie o laboratório:
   ```bash
   vagrant up
   ```
O Vagrant fará o download do Ubuntu e configurará as ferramentas automaticamente. Aguarde até que os 4 nós (`node1` a `node4`) estejam prontos.

### Gerenciando o Laboratório

Como o laboratório roda na sua máquina, é importante saber como liberar recursos (RAM e CPU) quando não estiver estudando. Execute estes comandos na pasta do `Vagrantfile`:

*   **Ligar o Cluster:** `vagrant up` (instala na primeira vez, apenas liga nas próximas).
*   **Desligar (Pausar):** `vagrant halt` (desliga as VMs com segurança).
*   **Excluir Tudo:** `vagrant destroy -f` (apaga as máquinas e discos virtuais permanentemente).

## 2. Execução dos Experimentos

O foco no ambiente local é a análise de latência em operações coletivas usando o benchmark de Broadcast (`osu_bcast`). O `Vagrantfile` já configura os caminhos do sistema para facilitar a execução.

### Como Rodar o Teste

1. Acesse o nó principal via SSH:
   ```bash
   vagrant ssh node1
   ```
2. Execute o benchmark variando o número de processos (`-np`) para 4, 8 e 16:
   ```bash
   mpirun -np 4 --hostfile ~/hostfile --oversubscribe --mca btl tcp,self --mca btl_tcp_if_include 192.168.56.0/24 --mca mpi_yield_when_idle 1 /usr/local/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_bcast
   ```

### Explicação dos Parâmetros

*   `-np [4, 8, 16]`: Define quantos processos MPI serão lançados.
*   `--hostfile ~/hostfile`: Lista de IPs das máquinas virtuais criada pelo Vagrant.
*   `--oversubscribe`: Permite rodar mais processos do que núcleos de CPU.
*   `--mca btl tcp,self`: Força o uso da rede TCP para comunicação.
*   `--mca btl_tcp_if_include 192.168.56.0/24`: Garante que o teste use apenas a rede isolada do VirtualBox, sem interferência do seu Wi-Fi ou Internet.
*   `--mca mpi_yield_when_idle 1`: Faz as VMs "cederem" processamento quando ociosas, evitando que o seu computador trave.

## 3. Dados e Visualização

Os resultados das execuções ficam na pasta `dados/`. Para gerar os gráficos do artigo:

1. No seu computador, entre na pasta de scripts:
   ```bash
   cd virtualbox/scripts/
   ```
2. Execute o script (requer Python instalado):
   ```bash
   python3 plot_latencia.py
   ```
Os gráficos serão salvos na pasta `graficos/`.
