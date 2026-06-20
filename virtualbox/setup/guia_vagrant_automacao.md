## Infraestrutura como Código: Escalonamento Automatizado de Cluster (Vagrant)

O que é o Vagrant?
O HashiCorp Vagrant é uma ferramenta de código aberto para a criação e manutenção de ambientes virtuais de software portáteis. Ao atuar como uma camada de abstração sobre hipervisores como o Oracle VirtualBox, ele permite que os desenvolvedores automatizem o ciclo de vida das máquinas virtuais usando um arquivo de configuração (Vagrantfile), trazendo os princípios de Infraestrutura como Código (IaC) para o desenvolvimento e testes locais.

A configuração manual de um cluster MPI é propensa a erros e não escala. Para automatizar o provisionamento e garantir a consistência, a infraestrutura do cluster foi definida utilizando o HashiCorp Vagrant. Isso garante que cada nó seja inicializado com sistema operacional, limites de recursos, configuração de rede e dependências do OpenMPI idênticos.

### 1. Pré-requisitos do Hospedeiro (Windows)
O ambiente requer o Oracle VirtualBox e o HashiCorp Vagrant instalados.
Instale o Vagrant via winget utilizando uma sessão do PowerShell como Administrador:

```PowerShell
winget install --id Hashicorp.Vagrant
```
Verifique a instalação (pode ser necessário reiniciar o sistema para atualizar o PATH do sistema):

```Bash
vagrant --version
```
## 2. Script de Automação (Vagrantfile)
O script abaixo provisiona os nós dinamicamente por meio da variável NUM_NODES. Ele atribui IPs sequenciais, compila os benchmarks da OSU nativamente e mapeia a matriz de topologia MPI antes mesmo das VMs inicializarem.

Crie um arquivo chamado Vagrantfile na raiz do seu projeto:

```Ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

NUM_NODES = 4

# Gera dinamicamente a matriz de topologia MPI antes da inicialização
HOSTFILE_CONTENT = (1..NUM_NODES).map { |n| "192.168.56.#{10+n} slots=1 max_slots=1" }.join("\n")

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  (1..NUM_NODES).each do |i|
    config.vm.define "node#{i}" do |node|
      
      node.vm.hostname = "node#{i}"
      node.vm.network "private_network", ip: "192.168.56.#{10+i}"

      # AJUSTES DO HIPERVISOR E CLONAGEM 
      node.vm.provider "virtualbox" do |vb|
        vb.name = "mpi_cluster_node_#{i}"
        vb.memory = "1024"
        vb.cpus = 1
        vb.gui = false 
        vb.linked_clone = true
      end

      # MONTAGEM PARA ISOLAMENTO DE I/O
      node.vm.synced_folder "./workloads", "/vagrant/workloads"

      # === SCRIPT DE PROVISIONAMENTO ZERO-TOUCH ===
      node.vm.provision "shell", inline: <<-SHELL
        export DEBIAN_FRONTEND=noninteractive
        
        echo "=> 1. Configurando SSH sem senha..."
        mkdir -p /home/vagrant/.ssh
                
        if [ ! -f /vagrant/mpi_key ]; then
          ssh-keygen -t rsa -b 2048 -f /vagrant/mpi_key -N "" -q
        fi
                
        cp /vagrant/mpi_key /home/vagrant/.ssh/id_rsa
        cp /vagrant/mpi_key.pub /home/vagrant/.ssh/id_rsa.pub
        cat /vagrant/mpi_key.pub >> /home/vagrant/.ssh/authorized_keys
                
        echo "Host *" > /home/vagrant/.ssh/config
        echo "    StrictHostKeyChecking no" >> /home/vagrant/.ssh/config
                
        chmod 600 /home/vagrant/.ssh/id_rsa
        chmod 600 /home/vagrant/.ssh/config
        chown -R vagrant:vagrant /home/vagrant/.ssh

        echo "=> 2. Atualizando pacotes e instalando OpenMPI..."
        apt-get update -y
        apt-get install -y openmpi-bin libopenmpi-dev build-essential wget tar

        echo "=> 3. Compilando OSU Micro-Benchmarks..."
        cd /opt
        if [ ! -d "osu-micro-benchmarks-7.3" ]; then
          wget --no-check-certificate https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz
          tar -xzf osu-micro-benchmarks-7.3.tar.gz
        fi
        
        cd /opt/osu-micro-benchmarks-7.3
        ./configure CC=mpicc CXX=mpicxx --quiet
        make -j$(nproc) > /dev/null 2>&1
        make install > /dev/null 2>&1

        echo "=> 4. Gerando hostfile do MPI..."
        cat > /home/vagrant/hostfile <<-EOF
#{HOSTFILE_CONTENT}
EOF
        chown vagrant:vagrant /home/vagrant/hostfile
      SHELL
    end
  end
end
```
## 3. Execução e Teste
O avaliador pode reproduzir o ambiente com zero configurações manuais. Forneça o comando no PowerShell para provisionar o cluster:

```PowerShell
cd C:\Caminho\Para\Sua\Pasta\Do\Vagrant
vagrant up
```
Uma vez concluído, acesse o nó mestre via SSH e execute o teste para validar a comunicação:

```Bash
vagrant ssh node1
mpirun --hostfile ~/hostfile -np 4 hostname
```
## 4. Clones Vinculados (Linked Clones / Gold Image)
Provisionar quatro VMs completas do Ubuntu desperdiçaria mais de 40~GB de espaço em SSD. Definir vb.linked_clone = true força o VirtualBox a baixar a imagem base apenas uma vez e tratá-la como uma imagem mestre de leitura utilitária (Gold Image). Os nós gravam dados apenas em pequenos discos diferenciais, reduzindo o consumo de armazenamento em aproximadamente 75% e acelerando o tempo de boot.

## 5. Isolamento de Execução
O Vagrant monta o diretório do sistema hospedeiro em /vagrant. Embora isso seja útil para injetar chaves SSH, compilar ou rodar os benchmarks diretamente dentro deste diretório faz com que o tráfego ignore a rede, agindo como um sistema de arquivos compartilhado.

Para garantir um isolamento de execução, os códigos-fonte devem ser copiados para um diretório e isolado da VM antes da compilação:

```Bash
mkdir -p ~/my_workloads
cp /vagrant/workloads/*.c ~/my_workloads/
cd ~/my_workloads/
mpicc osu_bcast.c -o osu_bcast
```
