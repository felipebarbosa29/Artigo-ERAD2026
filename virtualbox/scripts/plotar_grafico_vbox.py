import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os

# Funcao para formatar os ticks do Eixo X (B, KB, MB)
def formatador_bytes(x, pos):
    if x < 1024:
        return f"{int(x)} B"
    elif x < 1048576:
        return f"{int(x/1024)} KB"
    else:
        return f"{int(x/1048576)} MB"

def gerar_graficos():
    # Caminho do CSV consolidado
    csv_path = '../dados/dados_vbox.csv'
    
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo {csv_path} nao foi encontrado.")
        return

    # Lendo os dados via Pandas
    df = pd.read_csv(csv_path)
    tamanhos = df['Tamanho_Bytes']
    tempo_4 = df['NP_4_us']
    tempo_8 = df['NP_8_us']
    tempo_16 = df['NP_16_us']

    plt.figure(figsize=(10, 6))
    
    # Plotagem com estilos idênticos ao artigo
    plt.plot(tamanhos, tempo_4, marker='o', linestyle='-', linewidth=1.5, color='#1f77b4', label='4 Processos')
    plt.plot(tamanhos, tempo_8, marker='s', linestyle='--', linewidth=1.5, color='#ff7f0e', label='8 Processos')
    plt.plot(tamanhos, tempo_16, marker='^', linestyle='-.', linewidth=1.5, color='#2ca02c', label='16 Processos')

    plt.xscale('log', base=2)
    plt.yscale('log', base=10)

    # Formatação dos eixos
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatador_bytes))
    plt.xticks(rotation=45)

    plt.xlabel('Tamanho da Mensagem', fontsize=12)
    plt.ylabel('Tempo de Execucao (Microssegundos)', fontsize=12)
    plt.title('Desempenho de Broadcast no VirtualBox (4 VMs)', fontsize=14)
    
    plt.legend(loc='upper left')
    plt.grid(True, which="both", ls="--", alpha=0.5)

    plt.tight_layout()

    # Garantir que a pasta graficos existe
    os.makedirs('../graficos', exist_ok=True)

    # Salvando na pasta correta
    plt.savefig('../graficos/chart_osu_bcast.png', dpi=300)
    plt.savefig('../graficos/chart_osu_bcast.pdf', format='pdf')

    print(f"Sucesso! Grafico gerado a partir de {csv_path} e salvo em '../graficos/'.")

if __name__ == '__main__':
    gerar_graficos()
