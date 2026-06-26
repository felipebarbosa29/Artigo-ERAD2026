```markdown
# Ambiente em Nuvem (AWS)

Este diretório detalha as configurações e os comandos necessários para replicar o laboratório em nuvem utilizando a **Amazon Web Services (AWS)**. O foco deste ambiente é a análise da latência em comunicação ponto-a-ponto entre instâncias geograficamente distantes.

## 1. Configuração da Infraestrutura

Para replicar os resultados do artigo, é necessário criar instâncias no nível gratuito (*Free Tier*) da AWS.

**Especificações das Instâncias:**
- **Tipo:** `t2.micro` (1 vCPU, 1 GB de RAM).
- **Sistema Operacional:** Ubuntu 22.04 LTS.
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

![Latência AWS: Local vs. Inter-regional](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/3180r09k4EjIXRkpGJwCtD-images_1782492208622_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNi9hd3NfbnV2ZW0vZ3JhZmljb3MvY2hhcnRfb3N1X2xhdGVuY3lfYXdz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94LzMxODByMDlrNEVqSVhSa3BHSndDdEQtaW1hZ2VzXzE3ODI0OTIyMDg2MjJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmk5aGQzTmZiblYyWlcwdlozSmhabWxqYjNNdlkyaGhjblJmYjNOMVgyeGhkR1Z1WTNsZllYZHoucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=sIoSvIYkRMEmmQ4itDOzPxu~C~4KRAFgHsZk2A9TBwYTkOQ33kg82WVbobrycPagN25LP15gj1D~5Ne2RClBfcW2T43VvOQoH8ea2fL~scZ-vdBt6~YYVPIwD0KZm9VULUgtJZ-8KZz~saNdkuZ4lFL71oRYjTvn3VpwvQjZ7Zzph-I1MddheKD070mRFBdUiv7yR30OX0hfoE02ynqTvWvO5HckjIYiUKrt3JyGhYshClmktuo3FZv-BV22yB5dIXmjR4Z9b~0bj88E2W3p6HY8zX7qzqCxQjb9RGz~uf9Gmip53gnaw1XdG94odhjE4yEk0FCB8CBT1WNshd5zmw__)

Para acessar os dados brutos obtidos durante os testes, consulte a pasta `dados/`.
```
