# Ambiente Local (VirtualBox)

Este diretório contém os recursos necessários para provisionar e testar um cluster local utilizando o **VirtualBox** e o **Vagrant**, conforme descrito no artigo.

## Requisitos de Sistema

Para replicar este laboratório, o computador hospedeiro deve possuir:
- **Memória RAM:** Mínimo de 8 GB (O cluster consumirá aproximadamente 4,5 GB, incluindo o gerenciamento do VirtualBox).
- **Software:** VirtualBox (versão 7.0 ou superior) e Vagrant instalados.

## 1. Provisionamento do Cluster

O arquivo `Vagrantfile` incluído neste diretório automatiza a criação de 4 máquinas virtuais (Ubuntu 22.04 Server), configurando a rede interna e instalando as bibliotecas MPI necessárias.

**Passo a passo:**
1. Abra o terminal (ou Prompt de Comando/PowerShell) neste diretório.
2. Execute o comando para iniciar a criação das máquinas:
   ```bash
   vagrant up
   ```
3. Aguarde o download da imagem do sistema operacional e a configuração automática dos 4 nós (`node1`, `node2`, `node3`, `node4`).

## 2. Execução dos Experimentos

Após o provisionamento, os benchmarks do OSU Micro-Benchmarks já estarão compilados e prontos para uso. Você pode executar os testes diretamente de `node1`.

1. Acesse o nó principal (`node1`) via SSH:
   ```bash
   vagrant ssh node1
   ```
2. Os executáveis dos benchmarks estão em `/opt/osu-micro-benchmarks-7.3/mpi/pt2pt/blocking/` (para `osu_latency`), `/opt/osu-micro-benchmarks-7.3/mpi/collective/blocking/` (para `osu_bcast`, `osu_alltoall`), etc.
3. Execute os benchmarks variando o número de processos (`-np`). Exemplo para `osu_latency` com 2 processos:
   ```bash
   mpirun --hostfile /home/vagrant/hostfile --mca btl_tcp_if_include 192.168.56.0/24 --map-by node -np 2 /usr/local/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/blocking/osu_latency -i 100 -x 10
   ```
   *Para outros benchmarks, ajuste o caminho do executável e os parâmetros conforme necessário.*

## 3. Geração dos Gráficos

Os scripts Python para plotagem dos gráficos estão localizados na pasta `scripts/`.

1.  Certifique-se de que os dados dos experimentos (`.csv`) estejam na pasta `dados/`.
2.  No seu host (fora da VM), navegue até o diretório `virtualbox/scripts/`.
3.  Execute o script de plotagem. Por exemplo, para gerar o gráfico de latência:
    ```bash
    python3 plot_latencia.py
    ```
    *Isso gerará os arquivos de imagem (`.png`) e PDF (`.pdf`) na pasta `graficos/`.*

## 4. Resultados

O gráfico abaixo, apresentado no artigo, ilustra o aumento do tempo de envio de dados conforme o número de processos simultâneos aumenta, demonstrando a disputa por recursos no processador do hospedeiro.

![Tempo de envio (broadcast) no cluster VirtualBox](https://private-us-east-1.manuscdn.com/sessionFile/tLw70lW5nGNp0ZMx8TCeU6/sandbox/3180r09k4EjIXRkpGJwCtD-images_1782492208703_na1fn_L2hvbWUvdWJ1bnR1L0FydGlnby1FUkFEMjAyNi92aXJ0dWFsYm94L2dyYWZpY29zL2dyYWZpY29fbGF0ZW5jaWFfYXdz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEx3NzBsVzVuR05wMFpNeDhUQ2VVNi9zYW5kYm94LzMxODByMDlrNEVqSVhSa3BHSndDdEQtaW1hZ2VzXzE3ODI0OTIyMDg3MDNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwRnlkR2xuYnkxRlVrRkVNakF5Tmk5MmFYSjBkV0ZzWW05NEwyZHlZV1pwWTI5ekwyZHlZV1pwWTI5ZmJHRjBaVzVqYVdGZllYZHoucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=gGoX1VgbpfJgIvp17kgFUAAZobo4GsURT8dDi8r7JVHGToSpL47nhYgfOY-RvZom11NQfRf2W7diUABJfaVm7Ro75YZiYbHvOxcP2TuVWK3kbMGE1HGyphikZXZvTqfNczoMR9UhGQEtlEkP2mFB-j8Yvqfa6hoHFBYDrgrPhZmxSsVVHuyU5WE9N~iJHn~2XoO7SHsv0Cx2qqRbd60TThkB7aM1v1M7zK8IcSHRPMgO2B7OGshs1yv6PnwduqiP77-Vw5jgCefwlfY98NEyleLf16QsoprF3~D5jFKBepJwEnsbl9gdlfm3gJ1MZaPuEYWWI3gwb~GgkfKtzvLyVQ__)
*(Nota: O arquivo de imagem atual no repositório tem o nome trocado, mas representa os dados do VirtualBox).*

Para detalhes dos dados brutos e scripts de plotagem, consulte as pastas `dados/` e `scripts/`.
```
