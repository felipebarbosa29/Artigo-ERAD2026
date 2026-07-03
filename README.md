# Laboratório Didático de Computação Distribuída em EAD

Este repositório contém os códigos, scripts de automação e dados experimentais referentes ao artigo **"Laboratório Didático de Computação Distribuída em EAD: Estudo de Caso com VirtualBox e AWS"**, submetido à Escola Regional de Alto Desempenho de São Paulo (ERAD-SP 2026).

Este artigo apresenta dois ambientes práticos para o ensino de computação distribuída: um cluster local com VirtualBox e um cenário em nuvem com AWS. Descrevemos sobre a criação destes ambientes, e também damos um exemplo de uso deles. Utilizamos um exemplo de operação coletiva para o cluster local, e um exemplo de operação ponto-a-ponto no cenário da nuvem. Também levantamos os requisitos mínimos para executar o cluster local. Este trabalho está dentro de um projeto maior que busca desenvolver ferramentas acessíveis para o aprendizado de computação distribuída.

-----------------------------------------------------

## Estrutura do Repositório

O projeto está dividido em dois ambientes de experimentação, conforme descrito no artigo:

1. **[Ambiente Local (VirtualBox)](virtualbox/README.md):** Contém os scripts de provisionamento (`Vagrantfile`) para criar um cluster local de 4 nós e as instruções para executar o teste de comunicação coletiva (*broadcast*).
2. **[Ambiente em Nuvem (AWS)](aws_nuvem/README.md):** Contém as diretrizes para configuração de instâncias EC2 em regiões distintas, regras de rede (VPC/Firewall) e execução do teste de comunicação ponto-a-ponto (*latência*).
3. **[Códigos Modificados](codigos_modificados/):** Contém os códigos-fonte C dos benchmarks OSU utilizados nos experimentos, com pequenas adaptações para identificação dos nós.

-----------------------------------------------------

## Resumo dos Ambientes

As tabelas abaixo resumem as especificações utilizadas nos dois ambientes e os requisitos de sistema estimados para o laboratório local, garantindo a reprodutibilidade dos experimentos descritos no artigo.

| Recurso | VirtualBox (Local) | AWS (Nuvem) |
| :--- | :--- | :--- |
| **Quantidade** | 4 máquinas virtuais | 2 máquinas virtuais |
| **Processador** | 1 vCPU por máquina | 1 vCPU por máquina |
| **Memória** | 1 GB por máquina | 1 GB por máquina |
| **Sistema Operacional** | Ubuntu 22.04 Server | Ubuntu 22.04 Server |

### Requisitos de Sistema para o Laboratório (VirtualBox)

A Tabela 2 mostra o consumo de memória RAM e disco do Laboratório. O laboratório foi montado usando o VirtualBox (versão 7.0, instalado no Windows 11). O consumo real pode variar conforme os processos em segundo plano e a carga de trabalho do sistema operacional hospedeiro.

| Componente | Consumo (GB) | Disco (GB) |
| :--- | :--- | :--- |
| **Windows 11 (base)** | 4,0 | 64,0 |
| **4 VMs Ubuntu (1 GB cada)** | 3,5 – 4,0 | 37,0 |
| **Gerenciamento VBox/Rede** | 0,5 | 0,2-0,3 |
| **Total Estimado** | **8,0 – 8,5** | **101,2 – 101,3** |

*O laboratório foi criado em uma máquina com 32 GB de memória RAM, um SSD de 500 GB, um processador Intel Core i7-1165G7 e executando o sistema operacional Windows 11.*

---

## Autores e Créditos

Este trabalho foi desenvolvido por **Felipe Barbosa da Silva** sob a orientação do **Prof. Dr. Mauricio G. Palma**, como parte das atividades de Iniciação Científica da Universidade Virtual do Estado de São Paulo (UNIVESP).

Para acessar os detalhes de configuração e replicação de cada experimento, navegue pelos diretórios listados acima.
