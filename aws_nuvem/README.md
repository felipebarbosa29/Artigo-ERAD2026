# Ambiente em Nuvem (AWS)

Este diretório detalha a metodologia experimental, os fundamentos de networking e os procedimentos técnicos para a replicação do laboratório em nuvem utilizando a **Amazon Web Services (AWS)**.

## 3. Ambiente na Nuvem (AWS)

A utilização da nuvem pública neste projeto visa proporcionar um cenário de experimentação distribuída em larga escala, permitindo observar o comportamento de sistemas em redes de longa distância (WAN) sob condições reais de latência e jitter.

### 3.1. Arquitetura de Rede e Infraestrutura

A base da infraestrutura na AWS reside no isolamento lógico e na topologia de rede. Para garantir a fidelidade dos experimentos, é necessário compreender os componentes de networking utilizados:

#### Virtual Private Cloud (VPC)
A [VPC](https://aws.amazon.com/vpc/) é o alicerce que permite criar uma rede virtual isolada na nuvem. Este isolamento é fundamental para garantir que o tráfego do cluster MPI não sofra interferência externa e que as instâncias possuam endereçamento IP privado consistente.
- **Conceito Multi-nuvem:** O que a AWS chama de VPC é equivalente à **VCN** (*Virtual Cloud Network*) na Oracle Cloud, à **VNet** (*Virtual Network*) no Azure e à **VPC** no Google Cloud.

#### VPC Peering e Roteamento Inter-regional
Para viabilizar a comunicação entre a instância da **Virgínia do Norte (`us-east-1`)** e a do **Oregon (`us-west-2`)**, distantes aproximadamente 4.000 km, utiliza-se o [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html).
- **Por que usar Peering?** Diferente da comunicação via IP público (que transita pela internet aberta), o Peering estabelece uma conexão de roteamento direta através do *backbone* de fibra óptica global da AWS. Isso reduz drasticamente o *jitter* (variação da latência) e aumenta a previsibilidade das medições.
- **Equivalências:** *Remote VCN Peering* (OCI), *Global VNet Peering* (Azure) e *VPC Network Peering* (GCP).

#### Segurança e Firewall (Security Groups)
Os [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) atuam como firewalls estatais no nível da instância. Para o funcionamento do OpenMPI, é necessário:
1. Permitir tráfego TCP nas portas efêmeras entre os IPs privados das instâncias.
2. Liberar a porta 22 (SSH) para o nó mestre.
3. Configurar autenticação via chaves SSH assimétricas para permitir o lançamento de processos remotos sem senhas.

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

O experimento utiliza o benchmark **`osu_latency`** sob o modelo *ping-pong*: o processo de origem (rank 0) envia uma mensagem (`MPI_Send`) e o processo de destino (rank 1) a devolve imediatamente (`MPI_Recv`). A latência reportada é a média de **100 iterações** para cada tamanho de mensagem (1B a 1MB).

#### Execução Técnica
A execução deve ser iniciada a partir da instância na **Virgínia do Norte**. Devido à abstração das interfaces de rede virtualizadas (ENA - *Elastic Network Adapter*), o OpenMPI exige parâmetros de MCA (*Modular Component Architecture*) específicos:

```bash
# Execução a partir da instância us-east-1 (Virgínia)
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

**Análise dos Parâmetros:**
- `--mca pml ob1`: Seleciona a camada de gerenciamento de mensagens ponto-a-ponto padrão para garantir compatibilidade.
- `--mca btl tcp,self`: Força o uso da pilha TCP para tráfego de rede e *self* para memória compartilhada interna.
- `--mca btl_tcp_disable_family IPv6`: Desabilita o IPv6. Em redes AWS configuradas apenas com IPv4, isso evita que o MPI tente resolver endereços em uma pilha inexistente, o que causaria timeouts e falhas na inicialização do cluster.

### 3.3. Resultados e Visualização

O estudo compara dois cenários distintos para evidenciar o impacto da distância física no desempenho:
1. **Local (Intra-região):** Comunicação dentro da mesma instância na Virgínia.
2. **Distribuído (Inter-regional):** Comunicação entre Virgínia e Oregon.

A **Figura 2** (abaixo) demonstra que a latência salta de microsegundos (local) para dezenas de milissegundos (inter-regional), validando a influência do atraso de propagação em redes geodistribuídas.

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](graficos/chart_osu_latency_aws.png)

Para auditoria dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
