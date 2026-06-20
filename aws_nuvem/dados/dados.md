## 1. Cenário A: Execução EC2 na mesma Região - Norte da Virgínia

A tabela seguinte apresenta a evolução da latência com base no tamanho da mensagem quando ambos os processos estão a correr dentro da mesma instância EC2:

| Tamanho (Bytes) | Latência (µs) |
| :--- | :--- |
| 1 | 1,20 |
| 1024 | 1,08 |
| 65536 | 10,93 |
| 4194304 | 1452,00 |

---

## 2. Cenário B: Execução Inter-Regional (Nuvem) Norte da Virgínia --> Oregon

A tabela seguinte detalha a latência quando o tráfego atravessa o backbone da AWS via VPC Peering da Costa Leste para a Costa Oeste dos EUA:

| Tamanho (Bytes) | Latência (µs) |
| :--- | :--- |
| 1 | 28659,51 |
| 1024 | 28301,71 |
| 65536 | 85005,58 |
| 4194304 | 147349,24 |