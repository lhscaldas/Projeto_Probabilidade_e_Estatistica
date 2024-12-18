from a_preprocessamento import *

# Função para calcular as estadísticas por hora
def estatisticas_por_hora(df_smart, df_chrome):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

    # Zerar o arquivo de texto
    with open('estatisticas_por_hora/estatisticas_por_hora.txt', 'w', encoding='utf-8') as f:
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
        medias_smart.append((media_smart_down, media_smart_up))
        variancias_smart.append((variancia_smart_down, variancia_smart_up))
        desvios_smart.append((desvio_smart_down, desvio_smart_up))
        medias_chrome.append((media_chrome_down, media_chrome_up))
        variancias_chrome.append((variancia_chrome_down, variancia_chrome_up))
        desvios_chrome.append((desvio_chrome_down, desvio_chrome_up))

        # printar as estatísticas
        print(f'Hora {hour}: Smart TV - Download: média={media_smart_down:.2f}, variância={variancia_smart_down:.2f}, desvio padrão={desvio_smart_down:.2f}')
        print(f'Hora {hour}: Smart TV - Upload: média={media_smart_up:.2f}, variância={variancia_smart_up:.2f}, desvio padrão={desvio_smart_up:.2f}')
        print(f'Hora {hour}: Chromecast - Download: média={media_chrome_down:.2f}, variância={variancia_chrome_down:.2f}, desvio padrão={desvio_chrome_down:.2f}')
        print(f'Hora {hour}: Chromecast - Upload: média={media_chrome_up:.2f}, variância={variancia_chrome_up:.2f}, desvio padrão={desvio_chrome_up:.2f}')

        # salvar as estatísticas em um arquivo de texto
        with open('estatisticas_por_hora/estatisticas_por_hora.txt', 'a', encoding='utf-8') as f:
            f.write(f'Hora {hour}: Smart TV - Download: média={media_smart_down:.2f}, variância={variancia_smart_down:.2f}, desvio padrão={desvio_smart_down:.2f}\n')
            f.write(f'Hora {hour}: Smart TV - Upload: média={media_smart_up:.2f}, variância={variancia_smart_up:.2f}, desvio padrão={desvio_smart_up:.2f}\n')
            f.write(f'Hora {hour}: Chromecast - Download: média={media_chrome_down:.2f}, variância={variancia_chrome_down:.2f}, desvio padrão={desvio_chrome_down:.2f}\n')
            f.write(f'Hora {hour}: Chromecast - Upload: média={media_chrome_up:.2f}, variância={variancia_chrome_up:.2f}, desvio padrão={desvio_chrome_up:.2f}\n\n')

    return medias_smart, variancias_smart, desvios_smart, medias_chrome, variancias_chrome, desvios_chrome

def boxplots_por_hora(df_smart, df_chrome):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

    # Plot dos boxplot de download por hora para Smart TV
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_down', data=df_smart, color='blue')
    plt.title('Smart TV - Download por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    plt.savefig('estatisticas_por_hora/boxplot_smart_down.png')
    plt.show()

    # Plot dos boxplot de upload por hora para Smart TV
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_up', data=df_smart, color='blue')
    plt.title('Smart TV - Upload por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    plt.savefig('estatisticas_por_hora/boxplot_smart_up.png')
    plt.show()

    # Plot dos boxplot de download por hora para Chromecast
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_down', data=df_chrome, color='red')
    plt.title('Chromecast - Download por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    plt.savefig('estatisticas_por_hora/boxplot_chrome_down.png')
    plt.show()

    # Plot dos boxplot de upload por hora para Chromecast
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='bytes_up', data=df_chrome, color='red')
    plt.title('Chromecast - Upload por hora')
    plt.xlabel('Hora')
    plt.ylabel('bps (log10)')
    plt.savefig('estatisticas_por_hora/boxplot_chrome_up.png')
    plt.show()
    

if __name__ == '__main__':
    df1, df2 = preprocessamento()

    # Estatísticas por hora
    medias_smart, variancias_smart, desvios_smart, medias_chrome, variancias_chrome, desvios_chrome = estatisticas_por_hora(df1, df2)
    
    # Boxplots por hora
    boxplots_por_hora(df1, df2)