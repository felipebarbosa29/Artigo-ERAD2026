import matplotlib.pyplot as plt
import os

# 1. Dados Reais do experimento de Broadcast (osu_bcast) no VirtualBox
sizes = [1, 16, 256, 1024, 4096, 65536, 1048576]
labels_x = ['1 B', '16 B', '256 B', '1 KB', '4 KB', '64 KB', '1 MB']

# Latências em µs extraídas de dados_vbox.md
np4 = [1268.70, 1157.63, 1198.95, 1331.32, 1508.51, 3876.52, 20021.94]
np8 = [17225.31, 19616.45, 16357.41, 15481.06, 19259.83, 25341.15, 43703.31]
np16 = [3189.71, 3228.87, 3211.98, 3111.73, 3239.29, 9270.27, 48089.79]

# 2. Configuração da Figura (Estética Limpa e Acadêmica)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Cores da paleta Seaborn/Deep
cor_azul = '#4C72B0'
cor_laranja = '#DD8452'
cor_verde = '#55A868'

# 3. Plotando as linhas com marcadores
ax.plot(sizes, np4, marker='o', markersize=8, linewidth=2.5, color=cor_azul, label='4 Processos (NP=4)')
ax.plot(sizes, np8, marker='s', markersize=8, linewidth=2.5, color=cor_laranja, label='8 Processos (NP=8)')
ax.plot(sizes, np16, marker='^', markersize=8, linewidth=2.5, color=cor_verde, label='16 Processos (NP=16)')

# 4. Escalas Logarítmicas
ax.set_xscale('log', base=2)
ax.set_yscale('log', base=10)

# 5. Configuração do Eixo X
ax.set_xticks(sizes)
ax.set_xticklabels(labels_x, rotation=45, ha='right', fontsize=12)

# Configuração do Eixo Y
ax.tick_params(axis='y', labelsize=12)

# 6. Títulos e Textos Traduzidos
ax.set_title('OSU Micro-Benchmarks: BROADCAST (Cluster VirtualBox)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Tamanho da Mensagem', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Tempo Médio (µs)', fontsize=14, fontweight='bold', labelpad=10)

# 7. Grid (Grade) tracejada em cinza claro
ax.grid(True, which='major', linestyle='--', color='#d3d3d3', linewidth=1.2)

# 8. Legenda
legend = ax.legend(fontsize=12, loc='upper left', frameon=True)
legend.get_frame().set_edgecolor('#cccccc')
legend.get_frame().set_linewidth(1.5)

# Borda do gráfico cinza claro
for spine in ax.spines.values():
    spine.set_edgecolor('#cccccc')
    spine.set_linewidth(1.5)

plt.tight_layout()

# Garantir que a pasta graficos existe
os.makedirs('../graficos', exist_ok=True)

# 9. Salvando nos formatos solicitados na pasta correta
plt.savefig('../graficos/chart_osu_bcast.png', format='png', dpi=300, bbox_inches='tight')
plt.savefig('../graficos/chart_osu_bcast.pdf', format='pdf', bbox_inches='tight')

print("Gráficos de BROADCAST gerados com sucesso na pasta '../graficos/': 'chart_osu_bcast.png' e 'chart_osu_bcast.pdf'")