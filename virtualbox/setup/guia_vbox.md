#### Guia de Configuração de Máquina Virtual (VirtualBox e Ubuntu)

Uma Máquina Virtual (VM) é um software que emula um sistema de computador físico. Neste projeto de pesquisa, usamos máquinas virtuais para isolar nossos ambientes de testes distribuídos sem a necessidade de múltiplos computadores físicos.

Selecionamos o Oracle VirtualBox para gerenciar nossas VMs e o Ubuntu 24.04 LTS como sistema operacional convidado devido à sua estabilidade, forte suporte da comunidade e compatibilidade nativa com ferramentas de Computação de Alto Desempenho (HPC), como o OpenMPI.

## 1. Instalando o VirtualBox
Baixe o instalador do VirtualBox compatível com o sistema operacional do seu computador hospedeiro (Windows/macOS) no site oficial: virtualbox.org.

Execute o instalador e siga as orientações padrão da instalação oficial.

## 2. Baixando a Imagem do Sistema Operacional
Baixe a imagem ISO oficial do Ubuntu 24.04 LTS no site ubuntu.com.

Salve o arquivo .iso em um diretório acessível na sua máquina hospedeira.

## 3. Criando as Máquinas Virtuais (Especificações do Cluster)
Como nossos experimentos exigem um cluster de 4 nós rodando simultaneamente em uma máquina local, reduzimos os recursos individuais de cada VM para evitar a sobrecarga do computador hospedeiro.

Crie quatro máquinas virtuais separadas no VirtualBox utilizando as seguintes especificações de hardware para cada uma:

* **CPU: 2 vCPUs**
* **RAM: 2 GB (2048 MB)**

Armazenamento: Espaço em disco de 20 GB a 50 GB, alocado dinamicamente.

Drive Óptico: Aponte para o arquivo ISO baixado do Ubuntu 24.04 LTS para iniciar o instalador.

Siga as orientações padrão de instalação do Ubuntu dentro da janela de cada VM para concluir a configuração do sistema operacional.

## 4. Configuração Inicial (Dentro da VM Ubuntu)
O Ubuntu utiliza o apt (Advanced Package Tool) como seu gerenciador de pacotes padrão. Pense em um gerenciador de pacotes como uma "loja de aplicativos" via linha de comando para o seu sistema operacional. Ele baixa softwares automaticamente de repositórios oficiais e confiáveis, além de lidar com todos os arquivos de sistema necessários (dependências) de forma automatizada.

Assim que inicializar seu novo sistema Ubuntu, abra o terminal e execute os seguintes comandos para atualizar o núcleo do sistema e instalar as ferramentas essenciais de desenvolvimento:

```Bash
# Atualiza o índice de pacotes e atualiza os softwares instalados
sudo apt update && sudo apt upgrade -y
```
# Instala ferramentas de compilação e controle de versão
sudo apt install -y build-essential git
Detalhamento dos Comandos:
sudo apt update - Atualiza a lista local de pacotes disponíveis e suas respectivas versões a partir dos repositórios remotos.

sudo apt upgrade -y - Baixa e instala as versões mais recentes dos softwares já instalados na sua máquina.

build-essential - Um meta-pacote (um pacote que agrupa vários outros) que instala tudo o que é necessário para compilar código-fonte em C/C++, como compiladores (gcc, g++) e ferramentas de automação de build (make).

git - O sistema de controle de versão utilizado para gerenciar nosso código-fonte, scripts automatizados e a documentação do projeto.

Nota: Quaisquer dependências adicionais específicas para simuladores de rede individuais serão instaladas dinamicamente sobre esta configuração base.

## 5. Escalando o Cluster: Clonando VMs via Linha de Comando (CLI)
Criar VMs do zero para escalar nosso cluster (por exemplo, de 2 para 4 nós) consome muito tempo. Em vez disso, podemos clonar rapidamente uma máquina base totalmente configurada (como server-base) usando a ferramenta de CLI do VirtualBox, o VBoxManage.

#### Pré-requisitos
Antes de clonar, certifique-se de que a máquina virtual de origem esteja completamente desligada.

* **Opção A: Clonagem via Windows PowerShell** 
Abra o PowerShell na sua máquina hospedeira, navegue até o diretório de instalação do VirtualBox e execute o comando de clonagem:

```PowerShell
# Navega até o diretório do VirtualBox
cd "C:\Program Files\Oracle\VirtualBox\"

# Executa a clonagem completa e a registra automaticamente
.\VBoxManage.exe clonevm "server-base" --name "serverXXX" --register
```

* **Opção B: Clonagem via WSL (Terminal Bash)**
Se você estiver trabalhando dentro do ambiente WSL, pode chamar o executável do Windows diretamente:

```Bash
/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe clonevm "server-base" --name "serverXXX" --register
```
Detalhamento dos Parâmetros:
clonevm "server-base" - O nome da sua VM existente (origem).

--name "serverXXX" - O nome para a nova VM clonada.

--register - Adiciona a nova VM diretamente à interface gráfica do VirtualBox.

Nota: Este comando gera endereços MAC aleatórios automaticamente para a VM clonada, o que ajuda a prevenir colisões de hardware na rede.

## 6. Configuração de Rede e Resolução de Conflitos de IP
O Problema de Clonagem do "Machine-ID"
O Ubuntu utiliza um arquivo localizado em /etc/machine-id para solicitar um IP ao servidor DHCP. Como a clonagem copia o disco inteiro, a nova VM recebe exatamente o mesmo ID do nó mestre. O DHCP do VirtualBox identifica o mesmo ID e distribui exatamente o mesmo IP, causando um conflito de rede.

Para forçar o sistema a gerar uma identidade única, execute os seguintes comandos no terminal da VM clonada:

```Bash
# 1. Remove os identificadores clonados
sudo rm /etc/machine-id
sudo rm /var/lib/dbus/machine-id

# 2. Gera um ID de máquina totalmente novo para o sistema
sudo systemd-machine-id-setup

# 3. Reinicia a máquina para solicitar um novo IP
sudo reboot
```

Boa Prática para MPI: Atribuindo IPs Estáticos via Netplan
Depender de DHCP dinâmico não é uma boa estratégia para clusters HPC. Se uma VM reiniciar e receber um IP diferente, nosso arquivo de hosts (hostfile) do OpenMPI e as chaves SSH deixarão de funcionar. Para garantir a reprodutibilidade, precisamos configurar IPs estáticos usando o Netplan.

Localize e edite o seu arquivo de configuração de rede:

```Bash
sudo nano /etc/netplan/50-cloud-init.yaml
Limpe o arquivo e substitua-o pela estrutura abaixo.
(A formatação YAML depende estritamente de espaços para indentação. Não utilize a tecla TAB).

YAML
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.xx.xxx/24
```        
Atualize o bloco addresses para cada máquina (ex: .101 para o server1, .102 para o server2, etc.).

Salve o arquivo (Ctrl+O, Enter, Ctrl+X) e aplique as novas regras:

```Bash
sudo netplan apply
```