# Laboratório de Computação Distribuída: VirtualBox e AWS

Este repositório contém os artefatos técnicos, scripts de automação e dados experimentais utilizados no estudo de viabilidade de laboratórios de computação distribuída para a UNIVESP. O projeto foca na acessibilidade, permitindo que alunos repliquem clusters de alto desempenho em hardware modesto ou na nuvem.

## 📌 Visão Geral do Projeto

O trabalho está estruturado em dois pilares principais, conforme descrito no artigo:

1. **Ambiente Local (VirtualBox):** Focado na análise de comunicações coletivas (**Broadcast**) em um cluster de 4 nós.
2. **Ambiente em Nuvem (AWS):** Focado na medição de **Latência Ponto-a-Ponto** entre regiões geograficamente distantes (Virgínia do Norte e Oregon).

---

## 📁 Estrutura do Repositório

*   `/virtualbox/`: Scripts de automação (Vagrant), guias de instalação manual e dados brutos do teste de Broadcast.
*   `/aws_nuvem/`: Configurações de rede (VPC Peering) e dados de latência inter-regional.
*   `/codigos_modificados/`: Código-fonte C dos benchmarks OSU com a inclusão da rotina `gethostname()` para identificação precisa dos nós.
*   `/scripts/`: Scripts Python para geração dos gráficos apresentados no artigo.

---

## 🛠️ Infraestrutura e Configuração

### 1. Cluster Local (VirtualBox + Vagrant)
*   **Configuração:** 4 Máquinas Virtuais (Ubuntu 22.04).
*   **Recursos:** 1 vCPU e 1 GB de RAM por nó.
*   **Cálculo de Memória:** A alocação total de 4 GB de RAM para as VMs, somada ao consumo do sistema hospedeiro ($\approx$ 2-3 GB), torna o laboratório viável em máquinas com **8 GB de RAM**.
*   **Automação:** O uso do Vagrant garante que os limites de hardware sejam respeitados e que o ambiente seja idêntico em qualquer computador.

### 2. Nuvem AWS
*   **Instâncias:** 2 instâncias `t2.micro` (Free Tier).
*   **Rede:** Conectividade via **VPC Peering** entre `us-east-1` (Virgínia do Norte) e `us-west-2` (Oregon), cobrindo ~4.500 km.

---

## 🚀 Como Executar os Experimentos

### Teste de Broadcast (VirtualBox)
Para validar a comunicação coletiva no cluster local:
```bash
mpirun --hostfile hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node -np 8 ./osu_bcast -i 100 -x 10
```

### Teste de Latência (AWS)
Para medir a latência transcontinental isolando o tráfego no túnel VPC:
```bash
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_if_include 172.31.0.0/16,10.0.0.193/32 \
  --map-by node -np 2 ./osu_latency -i 100 -x 10
```

---

## 📈 Resultados e Visualização
Os dados brutos coletados estão disponíveis nas pastas de cada ambiente. Para gerar os gráficos do artigo, utilize os scripts Python:
```bash
python3 scripts/plotar_graficos_vbox.py
python3 scripts/plotar_graficos_aws.py
```

## 🔗 Referências e Documentação
*   [OSU Micro-Benchmarks](https://mvapich.cse.ohio-state.edu/benchmarks/)
*   [Documentação OpenMPI](https://www.open-mpi.org/doc/)
*   [VPC Peering AWS](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)

---
**Autor:** Felipe Barbosa da Silva  
**Orientador:** Mauricio G. Palma  
*Universidade Virtual do Estado de São Paulo (UNIVESP)*
