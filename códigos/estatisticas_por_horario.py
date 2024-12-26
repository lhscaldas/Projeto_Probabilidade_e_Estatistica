import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para calcular as estadísticas por hora
def estatisticas_por_hora(df_smart, df_chrome, salvar = False):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

    # Zerar o arquivo de texto
    if salvar:
        with open('estatísticas por hora/estatisticas_por_hora.txt', 'w', encoding='utf-8') as f:
            f.write('')

    # Loop para percorrer as horas
    medias_smart = []
    variancias_smart = []
    desvios_smart = []
    medias_chrome = []
    variancias_chrome = []
    desvios_chrome = []
    
    for hour in range(24):
        # Filtrar os dados para a hora específica
        df_smart_hour = df_smart[df_smart['hour'] == hour]
        df_chrome_hour = df_chrome[df_chrome['hour'] == hour]

        # Calcular as estatísticas
        media_smart_down = df_smart_hour['bytes_down'].mean()
        variancia_smart_down = df_smart_hour['bytes_down'].var()
        desvio_smart_down = df_smart_hour['bytes_down'].std()
        media_smart_up = df_smart_hour['bytes_up'].mean()
        variancia_smart_up = df_smart_hour['bytes_up'].var()
        desvio_smart_up = df_smart_hour['bytes_up'].std()

        media_chrome_down = df_chrome_hour['bytes_down'].mean()
        variancia_chrome_down = df_chrome_hour['bytes_down'].var()
        desvio_chrome_down = df_chrome_hour['bytes_down'].std()
        media_chrome_up = df_chrome_hour['bytes_up'].mean()
        variancia_chrome_up = df_chrome_hour['bytes_up'].var()
        desvio_chrome_up = df_chrome_hour['bytes_up'].std()

        # Adicionar os resultados às listas
        medias_smart.append((media_smart_up, media_smart_down))
        variancias_smart.append((variancia_smart_up, variancia_smart_down))
        desvios_smart.append((desvio_smart_up, desvio_smart_down))
        medias_chrome.append((media_chrome_up, media_chrome_down))
        variancias_chrome.append((variancia_chrome_up, variancia_chrome_down))
        desvios_chrome.append((desvio_chrome_up, desvio_chrome_down))

        # printar as estatísticas
        print(f'Hora {hour}: Smart TV - Upload: média={media_smart_up:.2f}, variância={variancia_smart_up:.2f}, desvio padrão={desvio_smart_up:.2f}')
        print(f'Hora {hour}: Smart TV - Download: média={media_smart_down:.2f}, variância={variancia_smart_down:.2f}, desvio padrão={desvio_smart_down:.2f}')
        print(f'Hora {hour}: Chromecast - Upload: média={media_chrome_up:.2f}, variância={variancia_chrome_up:.2f}, desvio padrão={desvio_chrome_up:.2f}')
        print(f'Hora {hour}: Chromecast - Download: média={media_chrome_down:.2f}, variância={variancia_chrome_down:.2f}, desvio padrão={desvio_chrome_down:.2f}')

        # salvar as estatísticas em um arquivo de texto
        if salvar:
            with open('estatísticas por hora/estatisticas_por_hora.txt', 'a', encoding='utf-8') as f:
                f.write(f'Hora {hour}: Smart TV - Upload: média={media_smart_up:.2f}, variância={variancia_smart_up:.2f}, desvio padrão={desvio_smart_up:.2f}\n')
                f.write(f'Hora {hour}: Smart TV - Download: média={media_smart_down:.2f}, variância={variancia_smart_down:.2f}, desvio padrão={desvio_smart_down:.2f}\n')
                f.write(f'Hora {hour}: Chromecast - Upload: média={media_chrome_up:.2f}, variância={variancia_chrome_up:.2f}, desvio padrão={desvio_chrome_up:.2f}\n')
                f.write(f'Hora {hour}: Chromecast - Download: média={media_chrome_down:.2f}, variância={variancia_chrome_down:.2f}, desvio padrão={desvio_chrome_down:.2f}\n\n')
                
    return medias_smart, variancias_smart, desvios_smart, medias_chrome, variancias_chrome, desvios_chrome

def plot_estatisticas_por_hora(medias_smart, desvios_smart, medias_chrome, desvios_chrome, salvar = False):
    horas = range(24)
    
    medias_smart_up, medias_smart_down = zip(*medias_smart)
    desvios_smart_up, desvios_smart_down = zip(*desvios_smart)
    medias_chrome_up, medias_chrome_down = zip(*medias_chrome)
    desvios_chrome_up, desvios_chrome_down = zip(*desvios_chrome)
    
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    
    # Smart TV - Upload
    axs[0, 0].plot(horas, medias_smart_up, '-o', color='blue', label='Média')
    axs[0, 0].fill_between(horas, 
                           [m - d for m, d in zip(medias_smart_up, desvios_smart_up)], 
                           [m + d for m, d in zip(medias_smart_up, desvios_smart_up)], 
                           color='blue', alpha=0.2, label='Desvio Padrão')
    axs[0, 0].set_title('Smart TV - Upload por Hora')
    axs[0, 0].set_xlabel('Hora')
    axs[0, 0].set_ylabel('bps')
    axs[0, 0].set_xticks(horas)
    axs[0, 0].legend()
    
    # Smart TV - Download
    axs[0, 1].plot(horas, medias_smart_down, '-o', color='blue', label='Média')
    axs[0, 1].fill_between(horas, 
                           [m - d for m, d in zip(medias_smart_down, desvios_smart_down)], 
                           [m + d for m, d in zip(medias_smart_down, desvios_smart_down)], 
                           color='blue', alpha=0.2, label='Desvio Padrão')
    axs[0, 1].set_title('Smart TV - Download por Hora')
    axs[0, 1].set_xlabel('Hora')
    axs[0, 1].set_ylabel('bps')
    axs[0, 1].set_xticks(horas)
    axs[0, 1].legend()
    
    # Chromecast - Upload
    axs[1, 0].plot(horas, medias_chrome_up, '-o', color='red', label='Média')
    axs[1, 0].fill_between(horas, 
                           [m - d for m, d in zip(medias_chrome_up, desvios_chrome_up)], 
                           [m + d for m, d in zip(medias_chrome_up, desvios_chrome_up)], 
                           color='red', alpha=0.2, label='Desvio Padrão')
    axs[1, 0].set_title('Chromecast - Upload por Hora')
    axs[1, 0].set_xlabel('Hora')
    axs[1, 0].set_ylabel('bps')
    axs[1, 0].set_xticks(horas)
    axs[1, 0].legend()
    
    # Chromecast - Download
    axs[1, 1].plot(horas, medias_chrome_down, '-o', color='red', label='Média')
    axs[1, 1].fill_between(horas, 
                           [m - d for m, d in zip(medias_chrome_down, desvios_chrome_down)], 
                           [m + d for m, d in zip(medias_chrome_down, desvios_chrome_down)], 
                           color='red', alpha=0.2, label='Desvio Padrão')
    axs[1, 1].set_title('Chromecast - Download por Hora')
    axs[1, 1].set_xlabel('Hora')
    axs[1, 1].set_ylabel('bps')
    axs[1, 1].set_xticks(horas)
    axs[1, 1].legend()
    
    plt.tight_layout()
    if salvar:
        plt.savefig('estatísticas por hora/estatisticas_por_hora.png')
    plt.show()

# Função para plotar boxplots por hora
def boxplots_por_hora(df_smart, df_chrome, salvar = False):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

    # Plot dos boxplot de download por hora para Smart TV
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_down', data=df_smart, color='blue')
    plt.title('Smart TV - Download por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    if salvar:
        plt.savefig('estatísticas por hora/boxplot_smart_down.png')
    plt.show()

    # Plot dos boxplot de upload por hora para Smart TV
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_up', data=df_smart, color='blue')
    plt.title('Smart TV - Upload por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    if salvar:
        plt.savefig('estatísticas por hora/boxplot_smart_up.png')
    plt.show()

    # Plot dos boxplot de download por hora para Chromecast
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_down', data=df_chrome, color='red')
    plt.title('Chromecast - Download por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    if salvar:
        plt.savefig('estatísticas por hora/boxplot_chrome_down.png')
    plt.show()

    # Plot dos boxplot de upload por hora para Chromecast
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_up', data=df_chrome, color='red')
    plt.title('Chromecast - Upload por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    if salvar:
        plt.savefig('estatísticas por hora/boxplot_chrome_up.png')
    plt.show()
    

if __name__ == '__main__':
    # Salvar os resultados
    salvar = True

    # Carregar os dados
    df1 = pd.read_csv('dados/smart_preprocessado.csv')
    df2 = pd.read_csv('dados/chrome_preprocessado.csv')

    # Estatísticas por hora
    medias_smart, variancias_smart, desvios_smart, medias_chrome, variancias_chrome, desvios_chrome = estatisticas_por_hora(df1, df2, salvar=salvar)

    # Plotar as estatísticas por hora
    plot_estatisticas_por_hora(medias_smart, desvios_smart, medias_chrome, desvios_chrome, salvar=salvar)
    
    # Boxplots por hora
    boxplots_por_hora(df1, df2, salvar=salvar)