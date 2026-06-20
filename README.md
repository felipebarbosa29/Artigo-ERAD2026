# Avaliação de Desempenho OpenMPI: VirtualBox vs. Nuvem AWS

Este repositório contém os artefatos, dados brutos, códigos-fonte modificados e scripts de geração de gráficos utilizados no artigo de análise de desempenho do middleware de comunicação OpenMPI, empregando a suíte OSU Micro-Benchmarks (OMB) v7.3.

## 📌 Objetivo do Estudo

O objetivo central é avaliar e comparar o impacto da infraestrutura subjacente na comunicação de processos MPI. Foram analisados dois cenários distintos:
1. **Ambiente Local (VirtualBox):** Foco na identificação de gargalos de CPU e Hypervisor durante operações coletivas (`osu_bcast`) em cenários de superlotação de processos (*oversubscription*).
2. **Ambiente em Nuvem (AWS):** Foco no impacto da distância geográfica física e do isolamento da pilha TCP/IP na latência ponto a ponto (`osu_latency`) utilizando túneis inter-regionais (VPC Peering).

---

## 📁 Estrutura de Diretórios

* `/virtualbox/`: Contém os dados brutos (`.txt`), scripts de plotagem em Python e gráficos (PNG/PDF) extraídos do cluster localizado na máquina hospedeira.
* `/aws_nuvem/`: Contém os dados consolidados, scripts e gráficos vetoriais comprovando o piso de latência física estabelecido pela distância entre os datacenters (aprox. 4.500 km).
* `/codigos_modificados/`: Código-fonte em C (`osu_latency.c` e `osu_bcast.c`) alterado com injeção de rotinas `gethostname()`. Essa modificação foi crucial para garantir a rastreabilidade topológica dos Ranks MPI durante a execução nos diferentes nós.

---

## 🛠️ Pré-requisitos de Infraestrutura

Para reproduzir os testes, os seguintes componentes base foram utilizados:
* **Ambiente Local:** HashiCorp Vagrant e Oracle VirtualBox.
* **Ambiente Nuvem:** Instâncias AWS EC2 (t2.micro) distribuídas geograficamente.
* **Dependências de Software (Ubuntu Linux):**
  * OpenMPI (`openmpi-bin`, `openmpi-common`, `libopenmpi-dev`)
  * Ferramentas de compilação C (`build-essential`)
  * Python 3 e Matplotlib (para a renderização dos gráficos de análise)

---

## 🚀 Execução: Ambiente Local (VirtualBox)

O cluster local é composto por 4 máquinas virtuais (1 vCPU, 512MB RAM) interligadas por uma rede privada isolada (Host-Only na sub-rede `192.168.56.0/24`).

### Comando de Execução (Broadcast)
Para forçar o cenário de *oversubscription* e analisar a degradação de desempenho do hypervisor, escalamos a operação de Broadcast em múltiplos processos. O comando abaixo exemplifica a execução distribuída forçando 8 Ranks concorrentes:

```bash
mpirun --hostfile hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node --oversubscribe -np 8 ./osu_bcast -i 100 -x 10
