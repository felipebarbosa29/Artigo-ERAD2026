# Ambiente na Nuvem (AWS)

Este diretório contém as instruções e dados do laboratório em nuvem. Usamos a
AWS para medir a latência de comunicação entre dois processos MPI em cenários
diferentes: dentro de uma mesma máquina e entre duas máquinas em regiões
distantes.

## O que foi feito

Criamos duas instâncias `t2.micro` (1 vCPU, 1 GB de RAM) em regiões diferentes
dos EUA:

- **Virgínia do Norte** (`us-east-1`)
- **Oregon** (`us-west-2`)

A distância entre elas é de aproximadamente 4.000 km. Executamos o benchmark
`osu_latency`, que funciona no modelo ping-pong: um processo envia uma mensagem
(`MPI_Send`) e o outro devolve (`MPI_Recv`). O tempo reportado é a média de 100
iterações para cada tamanho de mensagem.

## Configuração de Rede

Para que as duas instâncias se comuniquem, configuramos:

- **VPC (Virtual Private Cloud):** Uma rede isolada por região, com faixas de IP
  privado (ex: 10.0.0.0/16). Isso garante que a comunicação do MPI não sofra
  interferência de outros serviços.
- **VPC Peering:** Conexão direta entre as duas VPCs. A comunicação entre as
  regiões passa pela rede interna da AWS (não pela internet pública).
- **Security Groups:** Regras de firewall que liberam o tráfego TCP nas portas
  usadas pelo MPI (portas acima de 1024) e a porta 22 para SSH.
- **Chaves SSH:** Para permitir que o nó na Virgínia lance processos no nó do
  Oregon sem precisar de senha.

## Como rodar o teste

A execução é feita a partir da instância na Virgínia do Norte:

```
mpirun --hostfile hostfile_aws \
  --mca pml ob1 \
  --mca btl tcp,self \
  --mca btl_tcp_disable_family IPv6 \
  --map-by node -np 2 ./osu_latency
```

### Parâmetros:

- `--mca pml ob1`: Seleciona a camada de mensagens ponto a ponto.
- `--mca btl tcp,self`: Usa TCP para rede e comunicação interna.
- `--mca btl_tcp_disable_family IPv6`: Desabilita IPv6 (as VPCs usam só IPv4).

## Resultados

Executamos o `osu_latency` em dois cenários:

1. **Local:** Os dois processos na mesma máquina (Virgínia do Norte).
2. **Inter-regional:** Um processo na Virgínia e outro no Oregon.

No teste local, a latência variou de 0,92 µs até 202,66 µs. No inter-regional,
de 28,27 ms até 87,17 ms.

![Latência AWS](graficos/grafico_latencia_aws.png)

## Dados e Scripts

Os dados brutos estão em `dados/` e o script que gera o gráfico está em
`scripts/`.