import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from math import ceil
import numpy as np

# Função para calcular estatísticas gerais
def estatisticas_gerais(df_smart, df_chrome, salvar=False):
    # Smart TV
    print(f"Smart TV - Upload: média={df_smart['bytes_up'].mean():.2f}, variância={df_smart['bytes_up'].var():.2f}, desvio padrão={df_smart['bytes_up'].std():.2f}")
    print(f"Smart TV - Download: média={df_smart['bytes_down'].mean():.2f}, variância={df_smart['bytes_down'].var():.2f}, desvio padrão={df_smart['bytes_down'].std():.2f}")
    n_smart = len(df_smart)
    k_smart = ceil(1 + np.log2(n_smart)) # método de Sturges: k = 1 + log2(n)
    print('Número de bins Smart TV:', k_smart)
    
    # Chromecast
    print(f"Chromecast - Upload: média={df_chrome['bytes_up'].mean():.2f}, variância={df_chrome['bytes_up'].var():.2f}, desvio padrão={df_chrome['bytes_up'].std():.2f}")
    print(f"Chromecast - Download: média={df_chrome['bytes_down'].mean():.2f}, variância={df_chrome['bytes_down'].var():.2f}, desvio padrão={df_chrome['bytes_down'].std():.2f}")
    n_chrome = len(df_chrome)
    k_chrome = ceil(1 + np.log2(n_chrome)) # método de Sturges: k = 1 + log2(n)
    print('Número de bins Chromecast:', k_chrome)    
    
    # salvar as estatísticas em um arquivo de texto
    if salvar:
        with open('estatísticas gerais/estatisticas_gerais.txt', 'w', encoding='utf-8') as f:
            f.write(f"Smart TV - Upload: média={df_smart['bytes_up'].mean():.2f}, variância={df_smart['bytes_up'].var():.2f}, desvio padrão={df_smart['bytes_up'].std():.2f}\n")
            f.write(f"Smart TV - Download: média={df_smart['bytes_down'].mean():.2f}, variância={df_smart['bytes_down'].var():.2f}, desvio padrão={df_smart['bytes_down'].std():.2f}\n")
            f.write(f"Número de bins Smart TV: {k_smart}\n")
            f.write(f"Chromecast - Upload: média={df_chrome['bytes_up'].mean():.2f}, variância={df_chrome['bytes_up'].var():.2f}, desvio padrão={df_chrome['bytes_up'].std():.2f}\n")
            f.write(f"Chromecast - Download: média={df_chrome['bytes_down'].mean():.2f}, variância={df_chrome['bytes_down'].var():.2f}, desvio padrão={df_chrome['bytes_down'].std():.2f}\n")
            f.write(f"Número de bins Chromecast: {k_chrome}\n")
            
# Função para plotar histogramas
def histogramas(df_smart, df_chrome, k_smart=24, k_chrome=22, salvar=False):
    # Configurações de exibição
    kde = False

    # Criação dos subplots
    plt.figure(figsize=(12, 6))

    # Smart TV - Upload
    plt.subplot(2, 2, 1)
    sns.histplot(df_smart['bytes_up'], bins=k_smart, color='blue', kde=kde)
    plt.title('Smart TV - Upload')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e5:.0f}'))
    plt.ylabel('Contagem ($\\times 10^5$)')
    plt.xlabel('bps (log10)')

    # Smart TV - Download
    plt.subplot(2, 2, 2)
    sns.histplot(df_smart['bytes_down'], bins=k_smart, color='blue', kde=kde)
    plt.title('Smart TV - Download')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e5:.0f}'))
    plt.ylabel('Contagem ($\\times 10^5$)')
    plt.xlabel('bps (log10)')

    # Chromecast - Upload
    plt.subplot(2, 2, 3)
    sns.histplot(df_chrome['bytes_up'], bins=k_chrome, color='red', kde=kde)
    plt.title('Chromecast - Upload')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e5:.0f}'))
    plt.ylabel('Contagem ($\\times 10^5$)')
    plt.xlabel('bps (log10)')

    # Chromecast - Download
    plt.subplot(2, 2, 4)
    sns.histplot(df_chrome['bytes_down'], bins=k_chrome, color='red', kde=kde)
    plt.title('Chromecast - Download')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e5:.0f}'))
    plt.ylabel('Contagem ($\\times 10^5$)')
    plt.xlabel('bps (log10)')

    # Ajustar layout e exibir o gráfico
    plt.tight_layout()
    if salvar:
        plt.savefig('estatísticas gerais/histogramas.png')
    plt.show()


# Função para o boxplot
def boxplot(df_smart, df_chrome, salvar=False):
    # Adicionar uma coluna para identificar o dispositivo
    df_smart['Dispositivo'] = 'Smart TV'
    df_chrome['Dispositivo'] = 'Chromecast'

    # Combinar os DataFrames
    df_combined = pd.concat([df_smart, df_chrome], ignore_index=True)

    # Transformar os dados para formato longo
    df_melted = pd.melt(df_combined,
                        id_vars=['Dispositivo'],
                        value_vars=['bytes_up', 'bytes_down'],
                        var_name='Tipo de Tráfego',
                        value_name='Bytes')

    # Criar o boxplot agrupado
    plt.figure(figsize=(12, 6))
    sns.boxplot(
        x='Tipo de Tráfego', 
        y='Bytes', 
        hue='Dispositivo', 
        data=df_melted,
        palette={'Smart TV': 'blue', 'Chromecast': 'red'}
    )
    plt.title('Boxplot por Tipo de Tráfego e Dispositivo')
    plt.xlabel('Tipo de Tráfego')
    plt.ylabel('bps (log10)')
    plt.legend(title='Dispositivo')
    if salvar:
        plt.savefig('estatísticas gerais/boxplot.png')
    plt.show()

# Função para calcular a ECDF
def ecdf(data):
    # Ordena os dados
    data_sorted = np.sort(data)
    # Calcula as proporções cumulativas
    y = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    return data_sorted, y

# Função para plotar a ECDF
def plot_ecdf(df_smart, df_chrome, salvar=False):
    # Calcula a ECDF
    x_smart_down, y_smart_down = ecdf(df_smart['bytes_down'])
    x_smart_up, y_smart_up = ecdf(df_smart['bytes_up'])
    x_chrome_down, y_chrome_down = ecdf(df_chrome['bytes_down'])
    x_chrome_up, y_chrome_up = ecdf(df_chrome['bytes_up'])

    # Cria o gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(x_smart_up, y_smart_up, linestyle='-', color='blue', label='Smart TV - Upload', linewidth=2)
    plt.plot(x_smart_down, y_smart_down, linestyle='-', color='blue', label='Smart TV - Download', linewidth=2, alpha=0.5)
    plt.plot(x_chrome_up, y_chrome_up, linestyle='-', color='red', label='Chromecast - Upload', linewidth=2)
    plt.plot(x_chrome_down, y_chrome_down, linestyle='-', color='red', label='Chromecast - Download', linewidth=2, alpha=0.5)
    plt.title('ECDF para Smart TV e Chromecast')
    plt.xlabel('bps (log10)')
    plt.ylabel('Probabilidade Acumulada')
    plt.grid(True)
    plt.legend()
    if salvar:
        plt.savefig('estatísticas gerais/ecdf.png')
    plt.show()

if __name__ == '__main__':
    # Salvar os resultados
    salvar = True

    # Carregar os datasets pré-processados
    df1 = pd.read_csv('dados/smart_preprocessado.csv')
    df2 = pd.read_csv('dados/chrome_preprocessado.csv')

    # Estatisticas gerais
    estatisticas_gerais(df1, df2, salvar=salvar)
    histogramas(df1, df2, k_smart=24, k_chrome=22, salvar=salvar)
    boxplot(df1, df2, salvar=salvar)
    plot_ecdf(df1, df2, salvar=salvar)