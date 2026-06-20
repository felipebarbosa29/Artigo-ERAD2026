## 1. Cenário A: Execução EC2 na mesma Região - Norte da Virgínia

A tabela seguinte apresenta a evolução da latência com base no tamanho da mensagem quando ambos os processos estão a correr dentro da mesma instância EC2:

| Tamanho (Bytes) | Latência (µs) |
| :--- | :--- |
| 1 | 1,20 |
| 1024 | 1,08 |
| 65536 | 10,93 |
| 4194304 | 1452,00 |

**Análise Técnica (Local):** Uma observação inicial mostra que a latência para uma mensagem de 1 byte (1,20 µs) é ligeiramente superior à de uma mensagem de 1024 bytes (1,08 µs). Este é um fenómeno conhecido em ambientes virtualizados atribuído à sobrecarga de "Cold Start" (arranque a frio). O pacote inicial absorve o custo de acordar a CPU dos estados C inativos, da comutação de contexto e do estabelecimento de buffers de memória. Assim que o caminho de dados estiver ativo (o estado "quente"), os pacotes subsequentes maiores, como os de 1024 bytes, fluem mais rapidamente através do barramento de memória do hipervisor. À medida que o payload cresce para 4 MB, as operações de cópia de memória tornam-se o principal estrangulamento, aumentando exponencialmente a latência.

---

## 2. Cenário B: Execução Inter-Regional (Nuvem)

A tabela seguinte detalha a latência quando o tráfego atravessa o backbone da AWS via VPC Peering da Costa Leste para a Costa Oeste dos EUA:

| Tamanho (Bytes) | Latência (µs) |
| :--- | :--- |
| 1 | 28659,51 |
| 1024 | 28301,71 |
| 65536 | 85005,58 |
| 4194304 | 147349,24 |