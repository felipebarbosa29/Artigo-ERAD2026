import matplotlib.pyplot as plt

# 1. Dados dos seus testes na AWS
sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304]

lat_local = [1.20, 1.53, 0.94, 0.94, 0.96, 0.92, 0.95, 0.93, 0.97, 1.02, 1.08, 1.27, 3.47, 4.17, 5.09, 7.50, 10.93, 18.94, 37.94, 92.33, 202.66, 447.12, 1452.00]

lat_dist = [28659.51, 28282.05, 28280.68, 28279.96, 28286.30, 28288.07, 28287.14, 28284.58, 28287.12, 28393.71, 28301.71, 28300.72, 28315.99, 28340.05, 28431.22, 28410.60, 85005.58, 85400.20, 85427.91, 85599.15, 87179.18, 87412.13, 147349.24]

# 2. Configuração da Figura (Estética Limpa)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Cores idênticas ao modelo enviado
cor_azul = '#4C72B0'
cor_laranja = '#DD8452'

# 3. Plotando as linhas com marcadores específicos
ax.plot(sizes, lat_local, marker='o', markersize=8, linewidth=2.5, color=cor_azul, label='Linha de Base Local (NP=2)')
ax.plot(sizes, lat_dist, marker='s', markersize=8, linewidth=2.5, color=cor_laranja, label='Rede Distribuída (NP=2)')

# 4. Escalas Logarítmicas
ax.set_xscale('log', base=2)
ax.set_yscale('log', base=10)

# 5. Configuração do Eixo X para mostrar os labels exatos do seu print
ticks_x = [1, 16, 256, 4096, 65536, 1048576]
labels_x = ['1 B', '16 B', '256 B', '4 KB', '64 KB', '1 MB']
ax.set_xticks(ticks_x)
ax.set_xticklabels(labels_x, rotation=45, ha='right', fontsize=12)

# Configuração do Eixo Y
ax.tick_params(axis='y', labelsize=12)

# 6. Títulos e Textos Traduzidos
ax.set_title('OSU Micro-Benchmarks: LATÊNCIA (Ponto-a-Ponto)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Tamanho da Mensagem', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Latência (µs)', fontsize=14, fontweight='bold', labelpad=10)

# 7. Grid (Grade) tracejada em cinza claro
ax.grid(True, which='major', linestyle='--', color='#d3d3d3', linewidth=1.2)

# 8. Legenda no canto superior esquerdo
legend = ax.legend(fontsize=13, loc='upper left', frameon=True)
legend.get_frame().set_edgecolor('#cccccc')
legend.get_frame().set_linewidth(1.5)

# Borda do gráfico cinza claro
for spine in ax.spines.values():
    spine.set_edgecolor('#cccccc')
    spine.set_linewidth(1.5)

plt.tight_layout()

import os

# Garantir que a pasta graficos existe
os.makedirs('../graficos', exist_ok=True)

# 9. Salvando nos formatos solicitados na pasta correta
plt.savefig('../graficos/chart_osu_bcast.png', format='png', dpi=300, bbox_inches='tight')
plt.savefig('../graficos/chart_osu_bcast.pdf', format='pdf', bbox_inches='tight')

print("Gráficos gerados com sucesso na pasta '../graficos/': 'chart_osu_bcast.png' e 'chart_osu_bcast.pdf'")
