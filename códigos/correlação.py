from codigos.preprocessamento import *

# Ajustar os dados para o mesmo tamanho usando interpolação
def ajustar_tamanho(df1, df2):
    """
    Ajusta os tamanhos de dois DataFrames para o menor deles, ordenando por data-hora e interpolando.

    Parâmetros:
    - df1, df2: DataFrames contendo os dados.

    Retorna:
    - df1_ajustado, df2_ajustado: DataFrames ajustados e interpolados por data-hora, com tamanhos iguais.
    """
    # Converter a coluna 'date_hour' para datetime, se necessário
    df1['date_hour'] = pd.to_datetime(df1['date_hour'])
    df2['date_hour'] = pd.to_datetime(df2['date_hour'])

    # Ordenar os DataFrames pela coluna de data-hora
    df1 = df1.sort_values(by='date_hour').reset_index(drop=True)
    df2 = df2.sort_values(by='date_hour').reset_index(drop=True)

    # Criar índices de referência comuns para interpolação
    indices_comuns = np.linspace(0, 1, max(len(df1), len(df2)))

    # Interpolar os valores
    df1_interpolado = pd.DataFrame()
    df1_interpolado['date_hour'] = np.interp(indices_comuns, np.linspace(0, 1, len(df1)), pd.to_numeric(df1['date_hour']))
    df1_interpolado['bytes_up'] = np.interp(indices_comuns, np.linspace(0, 1, len(df1)), df1['bytes_up'])

    df2_interpolado = pd.DataFrame()
    df2_interpolado['date_hour'] = np.interp(indices_comuns, np.linspace(0, 1, len(df2)), pd.to_numeric(df2['date_hour']))
    df2_interpolado['bytes_down'] = np.interp(indices_comuns, np.linspace(0, 1, len(df2)), df2['bytes_down'])

    return df1_interpolado, df2_interpolado

# Calculo da correlacao entre as taxas de upload e download para cada dispositivo
def correlacao(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar=False):
    # Calculo da correlacao
    correlacao_up = df_smart_up['bytes_up'].corr(df_smart_down['bytes_down'])
    correlacao_down = df_chrome_up['bytes_up'].corr(df_chrome_down['bytes_down'])

    # Salvar em arquivo
    if salvar:
        with open('correlacao/correlacao.txt', 'w') as f:
            f.write('Correlacao entre as taxas de upload dos datasets 1 e 3: {:.6f}\n'.format(correlacao_up))
            f.write('Correlacao entre as taxas de download dos datasets 2 e 4: {:.6f}\n'.format(correlacao_down))
    
    return correlacao_up, correlacao_down

# Scatter plot entre as taxas de upload e download para cada dispositivo
def scatter_plot(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar=False):
    # Criar scatter plot
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Scatter plot para Smart TV
    axs[0].scatter(df_smart_up['bytes_up'], df_smart_down['bytes_down'], color='red', alpha=0.6)
    axs[0].set_title('Dispositivo Smart-TV')
    axs[0].set_xlabel('Upload')
    axs[0].set_ylabel('Download')

    # Scatter plot para Chromecast
    axs[1].scatter(df_chrome_up['bytes_up'], df_chrome_down['bytes_down'], color='blue', alpha=0.6)
    axs[1].set_title('Dispositivo Chromecast')
    axs[1].set_xlabel('Upload')
    axs[1].set_ylabel('Download')

    plt.tight_layout()

    # Salvar em arquivo
    if salvar:
        plt.savefig('correlacao/scatter_plot.png')
    plt.show()

if __name__ == '__main__':
    # Carregar os datasets
    dataset_1 = pd.read_csv('dataset_1.csv')
    dataset_2 = pd.read_csv('dataset_2.csv')
    dataset_3 = pd.read_csv('dataset_3.csv')
    dataset_4 = pd.read_csv('dataset_4.csv')

    # Ajustar os dados para o mesmo tamanho e ordená-los por tempo usando interpolação
    dataset_1, dataset_2 = ajustar_tamanho(dataset_1, dataset_2)
    dataset_3, dataset_4 = ajustar_tamanho(dataset_3, dataset_4)

    # Calcular correlacao
    correlacao_up, correlacao_down = correlacao(dataset_1, dataset_2, dataset_3, dataset_4, salvar=True)
    print('Correlacao entre as taxas de upload dos datasets 1 e 3:', correlacao_up)
    print('Correlacao entre as taxas de download dos datasets 2 e 4:', correlacao_down)

    # Gerar scatter plot
    scatter_plot(dataset_1, dataset_2, dataset_3, dataset_4, salvar=True)
