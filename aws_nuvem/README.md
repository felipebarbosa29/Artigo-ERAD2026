# Ambiente na Nuvem (AWS)

Este diretório detalha a metodologia experimental, os fundamentos de infraestrutura de rede e os procedimentos técnicos para a replicação do laboratório em nuvem utilizando a **Amazon Web Services (AWS)**.

## 3. Ambiente na Nuvem (AWS)

A utilização da nuvem pública visa proporcionar um cenário de experimentação distribuída em larga escala, permitindo observar o comportamento de sistemas em redes de longa distância. O experimento visa utilizar o benchmark osu_latency para validar um cenário em nuvem. 

### 3.1. Cenário de Execução

Executamos o osu latency em dois cen´arios diferentes: (1) Utilizando os dois
processos em uma mesma m´aquina, localizada na Virg´ınia do Norte, e (2) utilizando
os dois processos em m´aquinas distintas, uma localizada na Virg´ınia do Norte e outra
localizada no Oregon. Os resultados dessas execuc¸ ˜oes s˜ao mostrados pela Figura 2. No
teste com ambos os processos em uma mesma m´aquina, a latˆencia variou de 0, 92μs
at´e 202, 66μs. Com processos em m´aquinas distintas, a latˆencia variou de 28, 27ms at´e
87, 17ms.

#### Virtual Private Cloud (VPC)
A [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) permite lançar recursos da AWS em uma rede virtual logicamente isolada. Este isolamento é fundamental para:
- **Segregação de Tráfego:** Garantir que a comunicação do cluster MPI não sofra interferência de outros recursos da nuvem.
- **Endereçamento Consistente:** Definir faixas de IP privado (CIDR) que facilitam a configuração do `hostfile` do MPI.
- **Conceito Multi-nuvem:** Este recurso é análogo à **VCN** (*Virtual Cloud Network*) na Oracle OCI, à **VNet** no Microsoft Azure e à **VPC** no Google Cloud.

#### VPC Peering Inter-regional
Para conectar a instância da **Virgínia do Norte (`us-east-1`)** à instância do **Oregon (`us-west-2`)**, distantes ~4.000 km, utiliza-se o [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html).
- **Mecânica Técnica:** O Peering estabelece uma conexão de roteamento direta. Ao trafegar via rede privada, os pacotes utilizam o *backbone* de fibra óptica global da AWS, evitando a internet pública.
- **Vantagem Experimental:** Reduz drasticamente o **Jitter** (variação da latência), garantindo que os resultados reflitam a latência física determinística do enlace WAN.
- **Equivalências:** *Remote VCN Peering* (OCI), *Global VNet Peering* (Azure) e *VPC Network Peering* (GCP).

#### Segurança e Controle de Acesso
- **Security Groups:** Atuam como firewalls estatais no nível da instância. É necessário configurar regras que permitam o tráfego TCP nas portas efêmeras para o MPI e a porta 22 para SSH. [Saiba mais sobre Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html).
- **Autenticação SSH:** Utilização de chaves assimétricas para permitir que o nó mestre (Virgínia) lance processos remotos no nó escravo (Oregon) sem intervenção manual.

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

O experimento utiliza o benchmark **`osu_latency`** sob o modelo **"ping-pong"**: o processo raiz envia uma mensagem (`MPI_Send`) e o destino a devolve imediatamente (`MPI_Recv`). A latência reportada é a média de **100 iterações** para cada tamanho de mensagem.

#### Procedimento de Execução
A execução deve ser iniciada a partir da instância na **Virgínia do Norte**. Parâmetros de MCA (*Modular Component Architecture*) são essenciais para a correta identificação das placas de rede virtuais (ENA):

```bash
# Execução iniciada na instância da Virgínia do Norte
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

**Análise dos Parâmetros:**
- `--mca pml ob1`: Seleciona a camada de gerenciamento de mensagens ponto-a-ponto padrão.
- `--mca btl tcp,self`: Força o uso da pilha TCP para rede e *self* para comunicação interna.
- `--mca btl_tcp_disable_family IPv6`: Desabilita o IPv6, prevenindo falhas de resolução em VPCs que operam exclusivamente em IPv4.

### 3.3. Resultados Experimentais

O experimento compara dois cenários:
1. **Local:** Processos na mesma instância (Virgínia do Norte).
2. **Distribuído:** Processos entre Virgínia e Oregon.

A **Figura 2** apresenta a discrepância de desempenho, validando o impacto da distância geográfica:

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/jBQPQ8CUiz0YnKKDP8XcGz-images_1783106749671_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNl93b3JraW5nL2F3c19udXZlbS9ncmFmaWNvcy9ncmFmaWNvX2xhdGVuY2lhX2F3cw.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94L2pCUVBROENVaXowWW5LS0RQOFhjR3otaW1hZ2VzXzE3ODMxMDY3NDk2NzFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmw5M2IzSnJhVzVuTDJGM2MxOXVkWFpsYlM5bmNtRm1hV052Y3k5bmNtRm1hV052WDJ4aGRHVnVZMmxoWDJGM2N3LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTgzMDI5NzYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=HQe-JLTfYxQNW-qlAkZL~1NFvOMPzTrpFgBsYiDWnQR9ognUl7tYASLth21V-zFXfJcp~CMSbDNPosv39OtR8ot6t4ST2gb3CGS9xX-v1bUegIjAtgpYQYpcspoTVkwB2PlSNrVsvXwAat~1vEfE55GjxSsD8saFcLwOAHS~00I3sgo2LNVmMX5tYNbWKZ-QsVEJIhJqpyJKHM1Irx8RxxRhBBW7QFcmJd~~yp8OSNHxNb6pwg~wzfinu1o19jJv5DOhLr8oC3gNZ7xT38CTn7d6Z2zwjoJr-xVodscjPWXq7Douy4rB1vkfLachm1HbyeGEejoQtLk4puyaBcmG6g__)

Para auditoria dos dados e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
