# Resultados Experimentais: AWS Cloud (Inter-regional)

Medições de latência transcontinental utilizando instâncias EC2

## 1. Topologia de Rede
*   **Nó Master:** `us-east-1` (Virgínia do Norte) - IP 172.31.10.73
*   **Nó Worker:** `us-west-2` (Oregon) - IP 10.0.0.193
*   **Distância Estimada:** 4.500 km de fibra óptica.

## 2. Latência Ponto-a-Ponto (osu_latency)
Comparação entre execução local (mesma instância) e execução distribuída entre regiões -  Virgínia do Norte e Oregon - EUA.

| Tamanho (Bytes) | Latência Local (µs) | Latência Inter-regional (µs) |
| :--- | :--- | :--- |
| 1 | 1,20 | 28659,51 |
| 16 | 1,15 | 28540,12 |
| 256 | 1,12 | 28490,45 |
| 1024 | 1,08 | 28301,71 |
| 4096 | 12,45 | 29120,33 |
| 65536 | 10,93 | 85005,58 |
| 1048576 | 380,12 | 115420,10 |
| 4194304 | 1452,00 | 147349,24 |
