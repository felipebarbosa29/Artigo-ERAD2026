# Infraestrutura como Código: Automação do Cluster (Vagrant)

Este guia descreve a utilização do Vagrant para a criação automatizada e reprodutível do cluster de computação distribuída. A configuração manual de clusters MPI é suscetível a erros de rede e inconsistências de bibliotecas; o uso de Infraestrutura como Código (IaC) mitiga esses riscos ao garantir que todos os nós possuam o mesmo sistema operacional, limites de recursos e dependências do OpenMPI.

## 1. Pré-requisitos (Hospedeiro Windows)
O ambiente requer o Oracle VirtualBox e o HashiCorp Vagrant instalados.

Para instalar o Vagrant via PowerShell (Administrador):
```powershell
winget install --id Hashicorp.Vagrant
```
*Nota: Pode ser necessário reiniciar o sistema para atualizar o PATH.*

## 2. Script de Automação (Vagrantfile)
O arquivo `Vagrantfile` define a topologia do cluster de forma dinâmica. O script abaixo provisiona 4 nós, atribui IPs sequenciais e realiza a compilação nativa dos benchmarks antes do acesso inicial do usuário.

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

NUM_NODES = 4

# Geração dinâmica do hostfile MPI
HOSTFILE_CONTENT = (1..NUM_NODES).map { |n| "192.168.56.#{10+n} slots=1 max_slots=1" }.join("\n")

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  (1..NUM_NODES).each do |i|
    config.vm.define "node#{i}" do |node|
      
      node.vm.hostname = "node#{i}"
      node.vm.network "private_network", ip: "192.168.56.#{10+i}"

      # Ajustes do Hipervisor e Limites de Hardware
      node.vm.provider "virtualbox" do |vb|
        vb.name = "mpi_cluster_node_#{i}"
        vb.memory = "1024" # 1 GB por nó
        vb.cpus = 1        # 1 vCPU por nó
        vb.gui = false 
        vb.linked_clone = true # Otimização de armazenamento
      end

      # Provisionamento Automático (Zero Touch)
      node.vm.provision "shell", inline: <<-SHELL
        export DEBIAN_FRONTEND=noninteractive
        
        # 1. Configuração de chaves SSH para comunicação entre nós
        mkdir -p /home/vagrant/.ssh
        if [ ! -f /vagrant/mpi_key ]; then
          ssh-keygen -t rsa -b 2048 -f /vagrant/mpi_key -N "" -q
        fi
        cp /vagrant/mpi_key /home/vagrant/.ssh/id_rsa
        cp /vagrant/mpi_key.pub /home/vagrant/.ssh/id_rsa.pub
        cat /vagrant/mpi_key.pub >> /home/vagrant/.ssh/authorized_keys
        
        # 2. Instalação do OpenMPI e ferramentas de build
        apt-get update -y
        apt-get install -y openmpi-bin libopenmpi-dev build-essential wget
        
        # 3. Download e compilação dos benchmarks OSU
        cd /opt
        if [ ! -d "osu-micro-benchmarks-7.3" ]; then
          wget --no-check-certificate https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz
          tar -xzf osu-micro-benchmarks-7.3.tar.gz
        fi
        cd osu-micro-benchmarks-7.3
        ./configure CC=mpicc CXX=mpicxx --quiet
        make install > /dev/null 2>&1

        # 4. Geração do arquivo hostfile
        echo "#{HOSTFILE_CONTENT}" > /home/vagrant/hostfile
        chown vagrant:vagrant /home/vagrant/hostfile
      SHELL
    end
  end
end
```

## 3. Execução e Validação
Para instanciar o cluster, execute no terminal do hospedeiro:
```bash
vagrant up
```

Após o término, acesse o nó mestre para validar a malha de comunicação MPI:
```bash
vagrant ssh node1
mpirun --hostfile ~/hostfile -np 4 hostname
```

## 4. Análise Técnica de Recursos

### 4.1. Clones Vinculados (Linked Clones)
A configuração `vb.linked_clone = true` é essencial para operar nos limites de 8 GB de RAM e armazenamento SSD limitado. O VirtualBox utiliza uma imagem base de leitura e cria discos diferenciais para cada nó. Isso reduz o consumo de armazenamento em aproximadamente 75% e acelera significativamente o tempo de boot do cluster.

### 4.2. Isolamento de Rede e I/O
Embora o Vagrant utilize pastas compartilhadas (`/vagrant`), a execução dos benchmarks é realizada em diretórios isolados dentro da VM. Isso garante que as métricas de latência reflitam o tráfego real pela pilha TCP/IP virtualizada, evitando que o MPI utilize o sistema de arquivos compartilhado como atalho de comunicação, o que mascararia os resultados reais.
