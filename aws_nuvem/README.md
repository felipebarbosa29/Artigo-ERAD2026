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

#### Roteamento e VPC Peering
Para viabilizar a comunicação inter-regional via rede privada, utiliza-se o **VPC Peering**. Este recurso estabelece uma conexão de roteamento direta através do *backbone* de fibra óptica da AWS, evitando o tráfego pela internet pública. Isso é fundamental para minimizar o *jitter* e garantir a estabilidade das medições de latência. Em outros provedores, este conceito é análogo ao *VCN Peering* (OCI), *Global VNet Peering* (Azure) ou *VPC Network Peering* (GCP).

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

Como exemplo de uso do laboratório na nuvem, utilizamos o benchmark **`osu_latency`**, que opera utilizando 2 processos no modelo **"ping-pong"**: um processo envia uma mensagem (`MPI_Send`) e o outro a recebe e devolve imediatamente (`MPI_Recv`). O benchmark executa essa operação para diferentes tamanhos de mensagem e, para cada tamanho, reporta a média do tempo de transmissão de **100 iterações**.

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

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/FFo198zXxTrSABZ89w8nUE-images_1783097917778_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNl93b3JraW5nL2F3c19udXZlbS9ncmFmaWNvcy9ncmFmaWNvX2xhdGVuY2lhX2F3cw.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94L0ZGbzE5OHpYeFRyU0FCWjg5dzhuVUUtaW1hZ2VzXzE3ODMwOTc5MTc3NzhfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmw5M2IzSnJhVzVuTDJGM2MxOXVkWFpsYlM5bmNtRm1hV052Y3k5bmNtRm1hV052WDJ4aGRHVnVZMmxoWDJGM2N3LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTgzMDI5NzYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=RZx2lzlMaTz6Wou25DU-HKuxL75T9qQ-9so4-V8iAFVnLo4780iBsojTkYJP5mWbrieCyaXdC4R6uP~qYLaYrU71932Iy4~iz-eJu7op9Au2feaY0ps5J26kkF06zpFp1Uu7S3scfVZhcCMHjlw7wEkjcHJszeN~qwH0vqnlVGf6AYVeDr~QmBn21klSHpXqhC1ZC1Pq5CgZCi~jE5565wn6TDNsDIZUKOxFX77XHJm9b8SOAL-r455tBmGLkDwZn8MZVdugUBxica1GGVeZKmMpI3U4Gk0uweYt4c3TVMcmOMprDw8p9fxbYbMyXyQqczEOanGhKo6Cly3pJ324lw__)

Para detalhes sobre os dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
