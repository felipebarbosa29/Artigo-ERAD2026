# Desempenho OpenMPI: VirtualBox vs. Nuvem AWS

Artefatos, dados brutos, códigos modificados e scripts de plotagem utilizados para avaliar o desempenho do OpenMPI (OSU Micro-Benchmarks v7.3) em dois cenários de computação distribuída: um cluster local virtualizado (VirtualBox) e uma infraestrutura de nuvem pública (AWS).

## 📌 Objetivo

Viabilizar e documentar a criação de ambientes para o ensino e prática de computação distribuída, mitigando o alto custo de manutenção de clusters físicos. O foco da análise inclui:
1. Configuração e requisitos mínimos de infraestrutura via código (IaC).
2. Scripts para execução reprodutível de benchmarks.
3. Avaliação de viabilidade técnica (Local vs. Nuvem inter-regional).

---

## 📁 Estrutura do Repositório

* `/virtualbox/`: Dados brutos (`.txt`), scripts Python e gráficos do cluster local.
* `/aws_nuvem/`: Dados, scripts e gráficos do teste inter-regional (EUA Leste -> Oeste, ~4.500 km de distância).
* `/codigos_modificados/`: Código-fonte em C (`osu_latency.c` e `osu_bcast.c`) com injeção da chamada `gethostname()` para mapeamento exato dos Ranks MPI em cada nó.
* **Tratamento de Dados:** Logs brutos processados e consolidados em tabelas estruturadas (`dados_vbox.md` e `latencia_aws.md`) para anexação direta no artigo final.

---

## 🛠️ Infraestrutura e Pré-requisitos

### 1. Ambiente Local (VirtualBox / Vagrant)
* **Cluster:** 4 VMs gerenciadas via Vagrant/VirtualBox (Ubuntu 22.04 LTS).
* **Recursos por nó:** 1 vCPU, 1 GB RAM.
* **Rede:** Host-Only (`192.168.56.0/24`) com IPs estáticos via Netplan.

### 2. Ambiente Nuvem (AWS)
* **Instâncias:** 2 instâncias EC2 (`t2.micro` com Ubuntu 24.04 LTS).
* **Rede:** Túnel AWS VPC Peering interligando N. Virginia (`us-east-1` / `172.31.0.0/16`) a Oregon (`us-west-2` / `10.0.0.0/16`).

### 3. Software Base (Instalação em todos os nós)
```bash
sudo apt update && sudo apt install build-essential openmpi-bin openmpi-common libopenmpi-dev git -y
```

### ⚙️ Configuração Automática do Cluster Local (Vagrant)
Para evitar erros de provisionamento manual, a infraestrutura local pode ser instanciada como código. Um único comando cria os nós com IPs sequenciais, chaves SSH pré-configuradas e compila a suíte OSU nativamente.

Execução via Vagrantfile
Na raiz do projeto contendo o arquivo Vagrantfile, execute no terminal do hospedeiro:

```Bash
vagrant up
```
Nota: O script utiliza Clones Vinculados (linked_clone = true). O VirtualBox baixa a imagem base apenas uma vez e gera discos diferenciais para os nós, reduzindo o consumo de armazenamento em 75% e acelerando o tempo de boot.

* **Correção Crítica de Rede (Apenas para Clonagem Manual)**
Caso opte por clonar as VMs manualmente via interface ou CLI do VirtualBox (VBoxManage) em vez do Vagrant, o Ubuntu clonará o mesmo identificador de máquina, gerando conflitos de IP no DHCP. Contorne o problema rodando no nó clonado:

```Bash
sudo rm /etc/machine-id /var/lib/dbus/machine-id
sudo systemd-machine-id-setup
sudo reboot
```
#### Fixando IPs via Netplan
Para garantir que chaves SSH e o hostfile do MPI não quebrem após reboots, configure o arquivo /etc/netplan/50-cloud-init.yaml de cada nó para operar com IP estático na interface secundária:

YAML
network:
  version: 2
  ethernets:
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.56.101/24  # Altere o final para .102, .103, etc., em cada nó
Aplique as regras com: sudo netplan apply

## 🔑 Autenticação SSH Sem Senha
O orquestrador do OpenMPI (mpirun) exige acesso SSH irrestrito entre os nós. No nó mestre, gere o par de chaves e distribua-o para os nós trabalhadores (incluindo o próprio mestre):

```Bash
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
ssh-copy-id usuario@192.168.56.101
ssh-copy-id usuario@192.168.56.102
```
Atenção para AWS: Ambientes EC2 desativam autenticação por senha por padrão. Nesses cenários, copie manualmente o conteúdo de ~/.ssh/id_rsa.pub do mestre e anexe-o ao arquivo ~/.ssh/authorized_keys de cada worker.

## 🚀 Execução dos Testes
### 1. Cluster Local: Teste de Broadcast
 Execute:

```Bash
mpirun --hostfile hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node --oversubscribe -np 8 ./osu_bcast -i 100 -x 10
```
Tuning: As flags -i 100 e -x 10 forçam 10 iterações de warmup e 100 de medição real.

#### 1. Nuvem AWS: Latência Inter-Regional
Medição de latência ponto a ponto isolada através do túnel transcontinental do VPC Peering:

```Bash
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_if_include 172.31.0.0/16,10.0.0.0/16 \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency -i 100 -x 10
```  

## 📈 Processamento Visual (Gráficos)
Para converter os logs nos gráficos gerados para o artigo, execute os scripts a partir da raiz do repositório:

```Bash
# Gráficos do cluster local (VirtualBox)
python3 virtualbox/scripts/plotar_graficos_wsl.py

# Gráficos do ambiente em nuvem (AWS)
python3 aws_nuvem/scripts/plotar_graph_aws.py
```