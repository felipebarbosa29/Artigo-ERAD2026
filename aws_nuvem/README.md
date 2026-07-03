# Ambiente na Nuvem (AWS)

Este diretório detalha a metodologia experimental, os fundamentos de infraestrutura de rede e os procedimentos técnicos para a replicação do laboratório em nuvem utilizando a **Amazon Web Services (AWS)**.

## 3. Ambiente na Nuvem (AWS)

A utilização da nuvem pública visa proporcionar um cenário de experimentação distribuída em larga escala, permitindo observar o comportamento de sistemas em redes de longa distância (WAN). A arquitetura foi desenhada para explorar a latência física e a estabilidade de rede entre regiões geograficamente distantes.

### 3.1. Fundamentos de Networking e Infraestrutura

A base da experimentação na AWS reside na definição de uma topologia de rede isolada. Abaixo, detalhamos os componentes utilizados:

#### Virtual Private Cloud (VPC)
A [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) permite lançar recursos da AWS em uma rede virtual logicamente isolada. Este isolamento serve para:
- **Segregação de Tráfego:** Garantir que a comunicação do cluster MPI não sofra interferência de outros recursos da nuvem.
- **Endereçamento Consistente:** Definir faixas de IP privado (CIDR) que facilitam a configuração do `hostfile` do MPI.
- **Conceito Multi-nuvem:** Este recurso é análogo à **VCN** (*Virtual Cloud Network*) na Oracle OCI, à **VNet** no Microsoft Azure e à **VPC** no Google Cloud.

#### VPC Peering Inter-regional
Para conectar a instância da **Virgínia do Norte (`us-east-1`)** à instância do **Oregon (`us-west-2`)**, distantes ~4.000 km, utiliza-se o [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html).
- **A conexão** O Peering estabelece uma conexão de roteamento direta. Ao trafegar via rede privada, os pacotes utilizam o *backbone* de fibra óptica global da AWS, evitando a internet pública.
- **Vantagem Experimental:** Reduz o **Jitter** (variação da latência), garantindo que os resultados reflitam a latência física.
- **Equivalências:** *Remote VCN Peering* (OCI), *Global VNet Peering* (Azure) e *VPC Network Peering* (GCP).

#### Segurança e Controle de Acesso
- **Security Groups:** Atuam como firewalls no nível da instância. É necessário configurar regras que permitam o tráfego TCP nas portas efêmeras para o MPI e a porta 22 para SSH. [Saiba mais sobre Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html).
- **Autenticação SSH:** Utilização de chaves assimétricas para permitir que o nó mestre (Virgínia) lance processos remotos no nó escravo (Oregon) sem intervenção manual.

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

O experimento utiliza o benchmark **`osu_latency`** sob o modelo **"ping-pong"**: o processo raiz envia uma mensagem (`MPI_Send`) e o destino a devolve(`MPI_Recv`). A latência reportada é a média de **100 iterações** para cada tamanho de mensagem.

#### Procedimento de Execução
A execução deve ser iniciada a partir da instância na **Virgínia do Norte**. Parâmetros de MCA (*Modular Component Architecture*) são para a correta identificação das placas de rede virtuais (ENA):

```bash
# Execução iniciada na instância da Virgínia do Norte
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

**Análise dos Parâmetros:**
- `--mca pml ob1`: Seleciona a camada de gerenciamento de mensagens ponto-a-ponto.
- `--mca btl tcp,self`: Força o uso da pilha TCP para rede e *self* para comunicação interna.
- `--mca btl_tcp_disable_family IPv6`: Desabilita o IPv6, prevenindo falhas de resolução em VPCs que operam exclusivamente em IPv4.

### 3.3. Cenário de Execução e Resultados

Executamos o `osu_latency` em dois cenários diferentes: 
1. **Local:** Utilizando os dois processos em uma mesma máquina, localizada na Virgínia do Norte.
2. **Distribuído:** Utilizando os dois processos em máquinas distintas, uma localizada na Virgínia do Norte e outra localizada no Oregon. 

Os resultados dessas execuções são ilustrados pela **Figura 2**. No teste com ambos os processos em uma mesma máquina, a latência variou de **0,92µs até 202,66µs**. Com processos em máquinas distintas (inter-regional), a latência variou de **28,27ms até 87,17ms**.

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](graficos/grafico_latencia_aws.png)

Para auditoria dos dados e o script de plotagem, consulte as pastas `dados/` e `scripts/`.
