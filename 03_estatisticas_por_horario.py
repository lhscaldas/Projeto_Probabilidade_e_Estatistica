from preprocessamento import *

# Função para calcular as estadísticas por hora
def estatisticas_por_hora(df_smart, df_chrome):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

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

    return medias_smart, variancias_smart, desvios_smart, medias_chrome, variancias_chrome, desvios_chrome

# Função para plotar o boxplot por hora
def boxplot_por_hora(df_smart, df_chrome):
    pass

if __name__ == '__main__':
    df1, df2 = preprocessamento()

    # Estatísticas por hora
    estatisticas_por_hora(df1, df2)