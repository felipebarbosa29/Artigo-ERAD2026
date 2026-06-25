# Ambiente em Nuvem (AWS)

Este diretório detalha as configurações e os comandos necessários para replicar o laboratório em nuvem utilizando a **Amazon Web Services (AWS)**. O foco deste ambiente é a análise da latência em comunicação ponto-a-ponto entre instâncias geograficamente distantes.

## 1. Configuração da Infraestrutura

Para replicar os resultados do artigo, é necessário criar instâncias no nível gratuito (*Free Tier*) da AWS.

**Especificações das Instâncias:**
- **Tipo:** `t2.micro` (1 vCPU, 1 GB de RAM).
- **Sistema Operacional:** Ubuntu 22.04 Server
- **Localização:** Uma instância na região da Virgínia do Norte (`us-east-1`) e outra no Oregon (`us-west-2`).

**Configurações de Rede e Segurança:**
1. **Isolamento Lógico:** Utilize as VPCs padrão ou crie VPCs interconectadas (VPC Peering) se desejar comunicação exclusiva via rede privada.
2. **Firewall (Security Groups):** Libere o tráfego TCP para as portas utilizadas pelo MPI entre os IPs das duas instâncias, além da porta 22 para acesso SSH.
3. **Chaves SSH:** Configure a autenticação por chaves assimétricas para permitir que o processo MPI em uma instância acesse a outra sem exigir senha.

## 2. Execução do Experimento (Latência)

O experimento utiliza o benchmark `osu_latency` para medir o tempo de ida e volta (ping-pong) de mensagens.

Após compilar o código na instância principal, crie um arquivo `hostfile_aws` com os endereços IP (públicos ou privados, dependendo da sua configuração de VPC) das duas instâncias.

**Comando de Execução:**
Para garantir que o sistema identifique as placas de rede corretamente em ambientes de nuvem, utilizamos parâmetros específicos no `mpirun`, conforme citado no artigo:

```bash
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

*Nota: Dependendo da configuração da sua rede privada na AWS, pode ser necessário incluir o parâmetro `--mca btl_tcp_if_include <sua_subrede>` para forçar o uso de uma interface de rede específica.*

## 3. Resultados

O gráfico abaixo, correspondente à Figura 2 do artigo, ilustra a diferença significativa de latência entre a comunicação local (dentro da mesma instância na Virgínia) e a comunicação inter-regional (entre Virgínia e Oregon).

![Latência AWS: Local vs. Inter-regional](graficos/chart_osu_latency_aws.png)

Para acessar os dados brutos obtidos durante os testes, consulte a pasta `dados/`.
