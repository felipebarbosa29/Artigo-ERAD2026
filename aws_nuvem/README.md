# Ambiente em Nuvem (AWS)

Este diretório detalha a metodologia experimental, configurações de infraestrutura e procedimentos de execução para a replicação do laboratório em nuvem utilizando a **Amazon Web Services (AWS)**, conforme descrito no artigo.

## 3. Ambiente na Nuvem (AWS)

A utilização da nuvem pública visa proporcionar um cenário de experimentação distribuída em larga escala, permitindo observar o comportamento de sistemas em redes de longa distância (WAN).

### 3.1. Configuração do Ambiente na Nuvem

Para a montagem deste laboratório, foram provisionadas duas instâncias computacionais do tipo **`t2.micro`** (1 vCPU e 1 GB de RAM), utilizando o sistema operacional **Ubuntu 22.04 Server**. A distribuição geográfica foi planejada para maximizar a latência de rede, posicionando uma instância na região da **Virgínia do Norte (`us-east-1`)** e outra no **Oregon (`us-west-2`)**, totalizando uma distância física de aproximadamente 4.000 km.

#### Isolamento Lógico e Topologia de Rede
Um requisito fundamental para a execução de sistemas distribuídos em nuvem é a configuração de uma rede interna isolada. Na AWS, este recurso é denominado **VPC (*Virtual Private Cloud*)**. Este isolamento lógico é necessário tanto para a execução de processos em uma única máquina quanto para a comunicação entre instâncias distintas.

Embora o termo VPC seja proprietário da AWS, o conceito de rede lógica isolada é comum a outros provedores, sendo referenciado como:
- **Oracle Cloud (OCI):** VCN (*Virtual Cloud Network*).
- **Microsoft Azure:** VNet (*Virtual Network*).
- **Google Cloud:** VPC.

Para viabilizar a comunicação inter-regional via rede privada, utiliza-se o **VPC Peering**. Tecnicamente, este recurso estabelece uma conexão de roteamento entre duas VPCs distintas, permitindo que as instâncias troquem dados utilizando endereços IP privados. Ao evitar o tráfego pela internet pública, a comunicação utiliza o *backbone* de fibra óptica do provedor, o que é crítico para minimizar o *jitter* e garantir a estabilidade das medições de latência em sistemas distribuídos.

Em outros provedores, essa interconexão é implementada de forma análoga:
- **Oracle Cloud (OCI):** *Remote VCN Peering* via *Dynamic Routing Gateways* (DRG).
- **Microsoft Azure:** *Global VNet Peering*.
- **Google Cloud:** *VPC Network Peering*.

Além da interconexão lógica, é necessário ajustar as regras de **Firewall (*Security Groups*)** para permitir o tráfego TCP nas portas efêmeras utilizadas pelo MPI, além de configurar a autenticação via chaves SSH assimétricas para permitir a execução remota sem intervenção manual.

### 3.2. Cenário de Execução: Comunicação Ponto-a-Ponto (Latência)

O experimento na nuvem foca na análise de latência utilizando o benchmark **`osu_latency`**. A operação segue o modelo *ping-pong*: o processo de origem envia uma mensagem (`MPI_Send`) e o processo de destino a recebe e devolve imediatamente (`MPI_Recv`). O teste é executado para diferentes tamanhos de mensagem (de 1 byte a 1 megabyte), reportando a média do tempo de transmissão após 100 iterações.

#### Procedimento de Execução
Após a compilação dos benchmarks, a execução deve ser disparada a partir da instância principal (Virgínia), utilizando um `hostfile` que contenha os endereços das instâncias envolvidas.

Devido à natureza das interfaces de rede virtualizadas em nuvem, é necessário utilizar parâmetros adicionais no `mpirun` para a correta identificação das placas de rede e otimização do tráfego TCP:

```bash
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

### 3.3. Processamento de Dados e Visualização

Os resultados brutos coletados estão disponíveis na pasta `dados/`. Para gerar a visualização oficial apresentada no artigo, utilize o script Python localizado em `scripts/`. O script está pré-configurado com os dados validados da pesquisa para garantir a integridade da Figura 2.

1. Navegue até o diretório de scripts em seu host físico:
   ```bash
   cd aws_nuvem/scripts/
   ```
2. Execute a geração do gráfico:
   ```bash
   python3 plotar_grafico_aws.py
   ```

Abaixo, a **Figura 2** do artigo, que compara a latência local (intra-instância) com a latência inter-regional (Virgínia-Oregon):

![Figura 2: Latência AWS: Local (Virgínia) vs. Inter-regional (Virgínia-Oregon)](graficos/chart_osu_latency_aws.png)

Para detalhes sobre os dados experimentais e scripts de plotagem, consulte as respectivas pastas neste diretório.
