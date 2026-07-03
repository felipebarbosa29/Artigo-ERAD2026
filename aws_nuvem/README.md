# Ambiente na Nuvem (AWS)

Este diretório detalha a montagem, os testes e os resultados do laboratório utilizando a infraestrutura da **Amazon Web Services (AWS)**, conforme descrito no artigo.

## 3. Ambiente na Nuvem (AWS)

A utilização da nuvem pública visa proporcionar um cenário de experimentação distribuída em larga escala, permitindo observar o comportamento de sistemas em redes de longa distância.

### 3.1. Configuração do Ambiente na Nuvem

Para a criação das máquinas virtuais na AWS, foi necessária a criação de uma rede interna (**VPC - Virtual Private Cloud**) para garantir o isolamento lógico do ambiente. Este isolamento é necessário tanto para a execução de uma única máquina quanto para a comunicação entre instâncias distintas. No caso de máquinas em regiões distintas, a comunicação entre elas precisou ser configurada.

Conforme detalhado no artigo, foram configuradas duas máquinas virtuais (**`t2.micro`**, 1 vCPU e 1 GB de RAM) em regiões distintas dos Estados Unidos:
- **Instância Mestre:** Localizada no estado da **Virgínia do Norte (`us-east-1`)**.
- **Instância Remota:** Localizada no estado do **Oregon (`us-west-2`)**.

A distância entre essas máquinas é de cerca de **4.000 quilômetros**. Para que elas conseguissem se comunicar, além do isolamento lógico dos ambientes, foram configuradas as regras de segurança (*firewall*) da AWS e o acesso via chaves SSH.

### Topologia de Rede e VPC Peering

A arquitetura de rede deste laboratório foi estruturada sobre duas **VPCs (Virtual Private Clouds)** independentes, alocadas nas regiões da Virgínia (`us-east-1`) e do Oregon (`us-west-2`). Para permitir que estas redes isoladas se comuniquem como se estivessem em uma única rede local, foi configurado um **VPC Peering inter-regional**.

#### Fundamentos Técnicos do Peering
Diferente de uma conexão via VPN ou Internet pública, o VPC Peering estabelece uma relação de roteamento direta entre as sub-redes das duas redes isoladas. Isso significa que:
- **Tráfego Privado:** Os dados do OpenMPI trafegam utilizando endereços IP privados, sem serem expostos à internet aberta.
- **Backbone AWS:** O plano de dados é encapsulado e transmitido através da infraestrutura de fibra óptica global da AWS.
- **Previsibilidade:** Ao evitar os múltiplos "saltos" (*hops*) e o congestionamento da internet pública, conseguimos mitigar o **Jitter** (variação da latência) e garantir que os resultados do benchmark reflitam a latência física do enlace de longa distância.

#### Implementação Didática (Conceito Multi-nuvem)
Embora a nomenclatura varie entre os provedores de nuvem, o padrão de design para interconexão de redes privadas geodistribuídas é universal:
- **AWS:** [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html )
- **Oracle Cloud (OCI):** [Remote VCN Peering](https://docs.aws.amazon.com/iaas/Content/Network/Tasks/remoteVCNpeering.htm ) via *Dynamic Routing Gateways*.
- **Microsoft Azure:** [Global VNet Peering](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview ).
- **Google Cloud (GCP):** [VPC Network Peering](https://cloud.google.com/vpc/docs/vpc-peering ).

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

Como exemplo de uso do laboratório na nuvem, utilizamos o benchmark **`osu_latency`**, que opera utilizando 2 processos no modelo **"ping-pong"**: um processo envia uma mensagem (`MPI_Send`) e o outro a recebe e devolve(`MPI_Recv`). O benchmark executa essa operação para diferentes tamanhos de mensagem e, para cada tamanho, reporta a média do tempo de transmissão de **100 iterações**.

#### Procedimento de Execução
A execução deve ser disparada a partir da instância na **Virgínia do Norte**. Tivemos de utilizar os seguintes parâmetros adicionais no `mpirun` para que o sistema identificasse as placas de rede corretamente em ambiente de nuvem:

```bash
# Execução iniciada na instância da Virgínia do Norte
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

**Explicação dos Parâmetros:**
- `--mca pml ob1`: Define a camada de gerenciamento de mensagens ponto-a-ponto.
- `--mca btl tcp,self`: Especifica o uso da pilha TCP para rede e *self* para comunicação interna.
- `--mca btl_tcp_disable_family IPv6`: Desabilita o suporte a IPv6, prevenindo falhas de resolução de endereço em VPCs que operam majoritariamente em IPv4.

### 3.3. Resultados Experimentais

Executamos o `osu_latency` em dois cenários diferentes:
1. **Local:** Utilizando os dois processos em uma mesma máquina, localizada na Virgínia do Norte.
2. **Distribuído:** Utilizando os dois processos em máquinas distintas, uma na Virgínia e outra no Oregon.

A **Figura 2** do artigo ilustra os resultados dessas execuções, comparando a latência local com a latência inter-regional:

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](graficos/chart_osu_latency_aws.png)

Para detalhes sobre os dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
