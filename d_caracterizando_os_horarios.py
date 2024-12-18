from a_preprocessamento import *
from scipy import stats
import json

# Criando datasets com a maior taxa de upload e download por dispositivo
def passo_1(df_smart, df_chrome, horarios, salvar=False):
    # Extrair a hora da coluna 'date_hour"
    df_smart['hour'] = pd.to_datetime(df_smart['date_hour']).dt.hour
    df_chrome['hour'] = pd.to_datetime(df_chrome['date_hour']).dt.hour

    # Dataframe com a média de taxa de upload em uma hora, Smart TV
    df_smart_up = df_smart[df_smart['hour'] == horarios['smart_up']]

    # Dataframe com a média de taxa de download em uma hora, Smart TV
    df_smart_down = df_smart[df_smart['hour'] == horarios['smart_down']]

    # Dataframe com a média de taxa de upload em uma hora, Chromecast
    df_chrome_up = df_chrome[df_chrome['hour'] == horarios['chrome_up']]

    # Dataframe com a média de taxa de download em uma hora, Chromecast
    df_chrome_down = df_chrome[df_chrome['hour'] == horarios['chrome_down']]

    # Salvar os 4 datasets em 4 arquivos csv
    if salvar:
        df_smart_up.to_csv('dataset_1.csv', index=False)
        df_smart_down.to_csv('dataset_2.csv', index=False)
        df_chrome_up.to_csv('dataset_3.csv', index=False)
        df_chrome_down.to_csv('dataset_4.csv', index=False)

    return df_smart_up, df_smart_down, df_chrome_up, df_chrome_down

# Histograma dos datasets
def passo_2(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar = False):
    # Calculo do número de bins pelo método de Sturges: k = 1 + log2(n)
    n_smart_up = len(df_smart_up)
    k_smart_up = ceil(1 + np.log2(n_smart_up))
    print('Número de bins Smart TV Upload:', k_smart_up)
    n_smart_down = len(df_smart_down)
    k_smart_down = ceil(1 + np.log2(n_smart_down))
    print('Número de bins Smart TV Download:', k_smart_down)
    n_chrome_up = len(df_chrome_up)
    k_chrome_up = ceil(1 + np.log2(n_chrome_up))
    print('Número de bins Chromecast Upload:', k_chrome_up)
    n_chrome_down = len(df_chrome_down)
    k_chrome_down = ceil(1 + np.log2(n_chrome_down))
    print('Número de bins Chromecast Download:', k_chrome_down)

    # Configurações de exibição
    kde = False

    # Criação dos subplots
    plt.figure(figsize=(12, 6))

    # Smart TV - Upload
    plt.subplot(2, 2, 1)
    sns.histplot(df_smart_up['bytes_up'], bins=k_smart_up, color='blue', kde=kde)
    plt.title('Smart TV - Upload')
    plt.ylabel('Contagem')
    plt.xlabel('bps (log10)')

    # Smart TV - Download
    plt.subplot(2, 2, 2)
    sns.histplot(df_smart_down['bytes_down'], bins=k_smart_down, color='blue', kde=kde)
    plt.title('Smart TV - Download')
    plt.ylabel('Contagem')
    plt.xlabel('bps (log10)')

    # Chromecast - Upload
    plt.subplot(2, 2, 3)
    sns.histplot(df_chrome_up['bytes_up'], bins=k_chrome_up, color='red', kde=kde)
    plt.title('Chromecast - Upload')
    plt.ylabel('Contagem')
    plt.xlabel('bps (log10)')

    # Chromecast - Download
    plt.subplot(2, 2, 4)
    sns.histplot(df_chrome_down['bytes_down'], bins=k_chrome_down, color='red', kde=kde)
    plt.title('Chromecast - Download')
    plt.ylabel('Contagem')
    plt.xlabel('bps (log10)')


    # Ajustar layout e exibir o gráfico
    plt.tight_layout()
    if salvar:
        plt.savefig('caracterizando_os_horarios/histogramas.png')
    plt.show()

# Cálculo do MLE para distribuição Gaussiana e Gamma
def MLE(data):
    # Estimativa dos parâmetros da Gaussiana
    media = np.mean(data)
    variancia = np.var(data)

    # Estimativa dos parâmetros da Gamma
    a = media**2 / variancia
    b = variancia / media
    
    return media, variancia, a, b

# Cálculo do MLE para distribuição Gaussiana e Gamma
def passo_3(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar = False):
    # Cálculo do MLE para as distribuições
    media_smart_down, variancia_smart_down, a_smart_down, b_smart_down = MLE(df_smart_down['bytes_down'])
    media_smart_up, variancia_smart_up, a_smart_up, b_smart_up = MLE(df_smart_up['bytes_up'])
    media_chrome_down, variancia_chrome_down, a_chrome_down, b_chrome_down = MLE(df_chrome_down['bytes_down'])
    media_chrome_up, variancia_chrome_up, a_chrome_up, b_chrome_up = MLE(df_chrome_up['bytes_up'])

    # Adicionar os resultados às listas
    parametros_smart_up = {'media': media_smart_up, 'variancia': variancia_smart_up, 'a': a_smart_up, 'b': b_smart_up}
    parametros_smart_down = {'media': media_smart_down, 'variancia': variancia_smart_down, 'a': a_smart_down, 'b': b_smart_down}
    parametros_chrome_up = {'media': media_chrome_up, 'variancia': variancia_chrome_up, 'a': a_chrome_up, 'b': b_chrome_up}
    parametros_chrome_down = {'media': media_chrome_down, 'variancia': variancia_chrome_down, 'a': a_chrome_down, 'b': b_chrome_down}

    # Calcular a likelihood para a distribuição Gaussiana
    likelihood_smart_up_gaussiana = np.exp(np.sum(np.log(stats.norm.pdf(df_smart_up['bytes_up'], media_smart_up, np.sqrt(variancia_smart_up)))))
    likelihood_smart_down_gaussiana = np.exp(np.sum(np.log(stats.norm.pdf(df_smart_down['bytes_down'], media_smart_down, np.sqrt(variancia_smart_down)))))
    likelihood_chrome_up_gaussiana = np.exp(np.sum(np.log(stats.norm.pdf(df_chrome_up['bytes_up'], media_chrome_up, np.sqrt(variancia_chrome_up)))))
    likelihood_chrome_down_gaussiana = np.exp(np.sum(np.log(stats.norm.pdf(df_chrome_down['bytes_down'], media_chrome_down, np.sqrt(variancia_chrome_down)))))

    # Calcular a likelihood para a distribuição Gamma
    likelihood_smart_up_gamma = np.exp(np.sum(np.log(stats.gamma.pdf(df_smart_up['bytes_up'], a_smart_up, scale=b_smart_up))))
    likelihood_smart_down_gamma = np.exp(np.sum(np.log(stats.gamma.pdf(df_smart_down['bytes_down'], a_smart_down, scale=b_smart_down))))
    likelihood_chrome_up_gamma = np.exp(np.sum(np.log(stats.gamma.pdf(df_chrome_up['bytes_up'], a_chrome_up, scale=b_chrome_up))))
    likelihood_chrome_down_gamma = np.exp(np.sum(np.log(stats.gamma.pdf(df_chrome_down['bytes_down'], a_chrome_down, scale=b_chrome_down))))


    # Printar os resultados (parametros e likelihood)
    print('Smart TV - Download')
    print('MLE Gaussiana:', parametros_smart_down)
    print('MLE Gamma:', parametros_smart_down)
    print('Likelihood Gaussiana:', likelihood_smart_down_gaussiana)
    print('Likelihood Gamma:', likelihood_smart_down_gamma)
    print()
    print('Smart TV - Upload')
    print('MLE Gaussiana:', parametros_smart_up)
    print('MLE Gamma:', parametros_smart_up)
    print('Likelihood Gaussiana:', likelihood_smart_up_gaussiana)
    print('Likelihood Gamma:', likelihood_smart_up_gamma)
    print()
    print('Chromecast - Download')
    print('MLE Gaussiana:', parametros_chrome_down)
    print('MLE Gamma:', parametros_chrome_down)
    print('Likelihood Gaussiana:', likelihood_chrome_down_gaussiana)
    print('Likelihood Gamma:', likelihood_chrome_down_gamma)
    print()
    print('Chromecast - Upload')
    print('MLE Gaussiana:', parametros_chrome_up)
    print('MLE Gamma:', parametros_chrome_up)
    print('Likelihood Gaussiana:', likelihood_chrome_up_gaussiana)
    print('Likelihood Gamma:', likelihood_chrome_up_gamma)

    # Salvar os resultados em um arquivo de texto
    if salvar:
        data = {
            "Smart TV - Download": {
                "MLE Gaussiana": parametros_smart_down,
                "MLE Gamma": parametros_smart_down,
                "Likelihood Gaussiana": likelihood_smart_down_gaussiana,
                "Likelihood Gamma": likelihood_smart_down_gamma
            },
            "Smart TV - Upload": {
                "MLE Gaussiana": parametros_smart_up,
                "MLE Gamma": parametros_smart_up,
                "Likelihood Gaussiana": likelihood_smart_up_gaussiana,
                "Likelihood Gamma": likelihood_smart_up_gamma
            },
            "Chromecast - Download": {
                "MLE Gaussiana": parametros_chrome_down,
                "MLE Gamma": parametros_chrome_down,
                "Likelihood Gaussiana": likelihood_chrome_down_gaussiana,
                "Likelihood Gamma": likelihood_chrome_down_gamma
            },
            "Chromecast - Upload": {
                "MLE Gaussiana": parametros_chrome_up,
                "MLE Gamma": parametros_chrome_up,
                "Likelihood Gaussiana": likelihood_chrome_up_gaussiana,
                "Likelihood Gamma": likelihood_chrome_up_gamma
            }
        }

        # Escrever os dados no arquivo JSON
        with open('caracterizando_os_horarios/estatisticas_mle.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# Plotar histograma, pdf gaussiana e pdf gamma na mesma figura
def passo_4(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, file = "estatisticas_MLE.json", salvar = True):
    # Carregar os resultados do MLE
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        parametros_smart_down = data['Smart TV - Download']['MLE Gaussiana']
        parametros_smart_up = data['Smart TV - Upload']['MLE Gaussiana']
        parametros_chrome_down = data['Chromecast - Download']['MLE Gaussiana']
        parametros_chrome_up = data['Chromecast - Upload']['MLE Gaussiana']

    # Calculo do número de bins pelo método de Sturges: k = 1 + log2(n)
    n_smart_up = len(df_smart_up)
    k_smart_up = ceil(1 + np.log2(n_smart_up))
    print('Número de bins Smart TV Upload:', k_smart_up)
    n_smart_down = len(df_smart_down)
    k_smart_down = ceil(1 + np.log2(n_smart_down))
    print('Número de bins Smart TV Download:', k_smart_down)
    n_chrome_up = len(df_chrome_up)
    k_chrome_up = ceil(1 + np.log2(n_chrome_up))
    print('Número de bins Chromecast Upload:', k_chrome_up)
    n_chrome_down = len(df_chrome_down)
    k_chrome_down = ceil(1 + np.log2(n_chrome_down))
    print('Número de bins Chromecast Download:', k_chrome_down)
    
    # Configurações de exibição
    kde = False

    # Criação dos subplots
    plt.figure(figsize=(12, 6))

    # Smart TV - Upload
    plt.subplot(2, 2, 1)
    sns.histplot(df_smart_up['bytes_up'], bins=k_smart_up, color='blue', kde=kde, stat='density')
    x = np.linspace(df_smart_up['bytes_up'].min(), df_smart_up['bytes_up'].max(), 1000)
    y_gaussiana = stats.norm.pdf(x, parametros_smart_up['media'], np.sqrt(parametros_smart_up['variancia']))
    y_gamma = stats.gamma.pdf(x, parametros_smart_up['a'], scale=parametros_smart_up['b'])
    plt.plot(x, y_gaussiana, color='red', label='Gaussiana')
    plt.plot(x, y_gamma, color='green', label='Gamma')
    plt.title('Smart TV - Upload')
    plt.ylabel('Densidade')
    plt.xlabel('bps (log10)')
    plt.legend()

    # Smart TV - Download
    plt.subplot(2, 2, 2)
    sns.histplot(df_smart_down['bytes_down'], bins=k_smart_down, color='blue', kde=kde, stat='density')
    x = np.linspace(df_smart_down['bytes_down'].min(), df_smart_down['bytes_down'].max(), 1000)
    y_gaussiana = stats.norm.pdf(x, parametros_smart_down['media'], np.sqrt(parametros_smart_down['variancia']))
    y_gamma = stats.gamma.pdf(x, parametros_smart_down['a'], scale=parametros_smart_down['b'])
    plt.plot(x, y_gaussiana, color='red', label='Gaussiana')
    plt.plot(x, y_gamma, color='green', label='Gamma')
    plt.title('Smart TV - Download')
    plt.ylabel('Densidade')
    plt.xlabel('bps (log10)')
    plt.legend()

    # Chromecast - Upload
    plt.subplot(2, 2, 3)
    sns.histplot(df_chrome_up['bytes_up'], bins=k_chrome_up, color='red', kde=kde, stat='density')
    x = np.linspace(df_chrome_up['bytes_up'].min(), df_chrome_up['bytes_up'].max(), 1000)
    y_gaussiana = stats.norm.pdf(x, parametros_chrome_up['media'], np.sqrt(parametros_chrome_up['variancia']))
    y_gamma = stats.gamma.pdf(x, parametros_chrome_up['a'], scale=parametros_chrome_up['b'])
    plt.plot(x, y_gaussiana, color='blue', label='Gaussiana')
    plt.plot(x, y_gamma, color='green', label='Gamma')
    plt.title('Chromecast - Upload')
    plt.ylabel('Densidade')
    plt.xlabel('bps (log10)')
    plt.legend()

    
    # Chromecast - Download
    plt.subplot(2, 2, 4)
    sns.histplot(df_chrome_down['bytes_down'], bins=k_chrome_down, color='red', kde=kde, stat='density')
    x = np.linspace(df_chrome_down['bytes_down'].min(), df_chrome_down['bytes_down'].max(), 1000)
    y_gaussiana = stats.norm.pdf(x, parametros_chrome_down['media'], np.sqrt(parametros_chrome_down['variancia']))
    y_gamma = stats.gamma.pdf(x, parametros_chrome_down['a'], scale=parametros_chrome_down['b'])
    plt.plot(x, y_gaussiana, color='blue', label='Gaussiana')
    plt.plot(x, y_gamma, color='green', label='Gamma')
    plt.title('Chromecast - Download')
    plt.ylabel('Densidade')
    plt.xlabel('bps (log10)')
    plt.legend()


    # Ajustar layout e exibir o gráfico
    plt.tight_layout()
    if salvar:
        plt.savefig('caracterizando_os_horarios/histogramas_pdf.png')
    plt.show()


if __name__ == '__main__':
    # # passo 1: criar datasets com a maior taxa de upload e download por dispositivo
    # df1, df2 = preprocessamento()
    # horarios_maior_media = {'smart_up': 20, 'smart_down': 20, 'chrome_up': 22, 'chrome_down': 23}
    # dataset_1, dataset_2, dataset_3, dataset_4 = passo_1(df1, df2, horarios_maior_media, salvar=True)

    # Carregando os 4 datasets
    dataset_1 = pd.read_csv('dataset_1.csv')
    dataset_2 = pd.read_csv('dataset_2.csv')
    dataset_3 = pd.read_csv('dataset_3.csv')
    dataset_4 = pd.read_csv('dataset_4.csv')
        
    # # passo 2: histograma dos datasets (bins = 19, 19, 18, 18)
    # passo_2(dataset_1, dataset_2, dataset_3, dataset_4, salvar=True)

    # # passo 3: cálculo do MLE para distribuição Gaussiana e Gamma
    passo_3(dataset_1, dataset_2, dataset_3, dataset_4, salvar=False)

    # passo 4: plotar histograma, pdf gaussiana e pdf gamma na mesma figura?
    # passo_4(dataset_1, dataset_2, dataset_3, dataset_4, file = "caracterizando_os_horarios/estatisticas_mle.json", salvar = True)

