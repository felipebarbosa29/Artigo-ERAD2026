# Ambiente em Nuvem (AWS)

Este diretório detalha as configurações e os comandos necessários para replicar o laboratório em nuvem utilizando a **Amazon Web Services (AWS)**.

## 1. Provisionamento da Infraestrutura

A replicação dos experimentos em nuvem exige a alocação de instâncias computacionais distribuídas geograficamente. Para manter a fidelidade aos dados do artigo, as instâncias devem ser provisionadas com as seguintes especificações técnicas:

### Especificações das Instâncias
- **Tipo Recomendado:** `t2.micro` (1 vCPU, 1 GB RAM). 
  *   *Nota: Este tipo de instância é elegível ao **Free Tier** da AWS, mas instâncias de maior performance (famílias C ou M) podem ser utilizadas caso o usuário opte por planos pagos para reduzir o jitter de rede.*
- **Sistema Operacional:** Ubuntu 22.04 LTS (HVM).
- **Distribuição Geográfica:** 
  - **Instância A (Local):** Região `us-east-1` (N. Virginia).
  - **Instância B (Remota):** Região `us-west-2` (Oregon).

A escolha por essas regiões específicas visa maximizar a distância física dentro da infraestrutura da AWS, permitindo a medição clara da latência inter-regional.

**Configurações de Rede e Segurança:**
1. **Isolamento Lógico (VPC):** A *Virtual Private Cloud* (VPC) é o serviço que permite criar uma rede virtual isolada e logicamente separada para seus recursos na nuvem. Embora o termo VPC seja específico da AWS, o conceito de rede virtual isolada é universal entre provedores:
    - **Oracle Cloud (OCI):** Chamado de **VCN** (*Virtual Cloud Network*).
    - **Microsoft Azure:** Chamado de **VNet** (*Virtual Network*).
    - **Google Cloud (GCP):** Também utiliza o termo **VPC**.
    
    Para este laboratório, utilize as redes padrão de cada região ou configure um **VPC Peering** para permitir que as instâncias em regiões distintas (Virgínia e Oregon) se comuniquem via IPs privados, simulando uma rede local distribuída.
2. **Firewall (Security Groups):** Libere o tráfego TCP para as portas utilizadas pelo MPI entre os IPs das duas instâncias, além da porta 22 para acesso SSH.
3. **Chaves SSH:** Configure a autenticação por chaves assimétricas para permitir que o processo MPI em uma instância acesse a outra sem exigir senha.

## 2. Execução do Experimento (Latência)

O experimento utiliza o benchmark `osu_latency` para medir o tempo de ida e volta (ping-pong) de mensagens.

Após compilar o código na instância principal Us-east1, crie um arquivo `hostfile_aws` com os endereços IP (públicos ou privados, dependendo da sua configuração de VPC) das duas instâncias.

**Comando de Execução:**
Para garantir que o sistema identifique as placas de rede corretamente em ambientes de nuvem, utilizamos parâmetros específicos no `mpirun`, conforme citado no artigo:

```bash
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 /usr/local/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/blocking/osu_latency
```

*Nota: Dependendo da configuração da sua rede privada na AWS, pode ser necessário incluir o parâmetro `--mca btl_tcp_if_include <sua_subrede>` para forçar o uso de uma interface de rede específica.*

## 3. Geração dos Gráficos

Os scripts Python para plotagem dos gráficos estão localizados na pasta `scripts/`.

1.  Certifique-se de que os dados dos experimentos (`.csv`) estejam na pasta `dados/`.
2.  No seu host (fora da instância AWS), navegue até o diretório `aws_nuvem/scripts/`.
3.  Execute o script de plotagem. Por exemplo, para gerar o gráfico de latência da AWS:
    ```bash
    python3 plotar_grafico_aws.py
    ```
    *Isso gerará os arquivos de imagem (`.png`) e PDF (`.pdf`) na pasta `graficos/`.*

## 4. Resultados

O gráfico abaixo, correspondente à Figura 2 do artigo, ilustra a diferença de latência entre a comunicação local (dentro da mesma instância na Virgínia) e a comunicação inter-regional (entre Virgínia e Oregon).

![Latência AWS: Local vs. Inter-regional](graficos/chart_osu_latency_aws.png)

Para acessar os dados brutos obtidos durante os testes, consulte a pasta `dados/`.
```
