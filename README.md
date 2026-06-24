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

A tabela abaixo resume as especificações utilizadas nos dois ambientes para garantir a reprodutibilidade dos experimentos descritos no artigo.

| Recurso | VirtualBox (Local) | AWS (Nuvem) |
| :--- | :--- | :--- |
| **Quantidade** | 4 máquinas virtuais | 2 máquinas virtuais |
| **Processador** | 1 vCPU por máquina | 1 vCPU por máquina |
| **Memória** | 1 GB por máquina | 1 GB por máquina |
| **Sistema Operacional** | Ubuntu 22.04 Server | Ubuntu 22.04 Server |

---

## Autores e Créditos

Este trabalho foi desenvolvido por **Felipe Barbosa da Silva** sob a orientação do **Prof. Dr. Mauricio G. Palma**, como parte das atividades de Iniciação Científica da Universidade Virtual do Estado de São Paulo (UNIVESP).

Para acessar os detalhes de configuração e replicação de cada experimento, navegue pelos diretórios listados acima.
