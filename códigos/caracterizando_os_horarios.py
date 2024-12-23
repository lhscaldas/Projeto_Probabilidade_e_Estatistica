from codigos.preprocessamento import *
from scipy import stats
from scipy.special import digamma
from scipy.optimize import newton
from scipy.stats import gamma
from scipy.stats import kstest
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
    # Estimativa da gaussiana
    media = np.mean(data)
    variancia = np.var(data)

    # Verificar se data tem valores menores que zero
    if (data < 0).any():
        raise ValueError('Os dados contêm valores negativos. A distribuição Gamma não pode ser usada.')
    
    # Estimar parâmetros da gamma
    epsilon = 1e-6
    a, loc, scale = gamma.fit(data+epsilon, floc=0)
    b = scale  # Em scipy, scale é equivalente a 'b'

    # Teste de Kolmogorov-Smirnov para Gaussiana
    ks_stat, p_value = kstest(data, 'norm', args=(media, np.sqrt(variancia)))
    print(f"KS-Test Gaussiana: Estatística={ks_stat}, p-valor={p_value}")

    # Teste de Kolmogorov-Smirnov para Gamma
    ks_stat, p_value = kstest(data, 'gamma', args=(a, 0, b))
    print(f"KS-Test Gamma: Estatística={ks_stat}, p-valor={p_value}")
    
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

    # Calcular a log-likelihood para a distribuição Gaussiana
    epsilon = 1e-10
    log_likelihood_smart_up_gaussiana = np.sum(np.log(stats.norm.pdf(df_smart_up['bytes_up']+epsilon, media_smart_up, np.sqrt(variancia_smart_up))))
    log_likelihood_smart_down_gaussiana = np.sum(np.log(stats.norm.pdf(df_smart_down['bytes_down']+epsilon, media_smart_down, np.sqrt(variancia_smart_down))))
    log_likelihood_chrome_up_gaussiana = np.sum(np.log(stats.norm.pdf(df_chrome_up['bytes_up']+epsilon, media_chrome_up, np.sqrt(variancia_chrome_up))))
    log_likelihood_chrome_down_gaussiana = np.sum(np.log(stats.norm.pdf(df_chrome_down['bytes_down']+epsilon, media_chrome_down, np.sqrt(variancia_chrome_down))))

    # Calcular a log-likelihood para a distribuição Gamma
    log_likelihood_smart_up_gamma = np.sum(np.log(stats.gamma.pdf(df_smart_up['bytes_up']+epsilon, a_smart_up, scale=b_smart_up)))
    log_likelihood_smart_down_gamma = np.sum(np.log(stats.gamma.pdf(df_smart_down['bytes_down']+epsilon, a_smart_down, scale=b_smart_down)))
    log_likelihood_chrome_up_gamma = np.sum(np.log(stats.gamma.pdf(df_chrome_up['bytes_up']+epsilon, a_chrome_up, scale=b_chrome_up)))
    log_likelihood_chrome_down_gamma = np.sum(np.log(stats.gamma.pdf(df_chrome_down['bytes_down']+epsilon, a_chrome_down, scale=b_chrome_down)))

    # Calcular a likelihood para as duas distribuições
    likelihood_smart_up_gaussiana = np.exp(log_likelihood_smart_up_gaussiana)
    likelihood_smart_down_gaussiana = np.exp(log_likelihood_smart_down_gaussiana)
    likelihood_chrome_up_gaussiana = np.exp(log_likelihood_chrome_up_gaussiana)
    likelihood_chrome_down_gaussiana = np.exp(log_likelihood_chrome_down_gaussiana)

    likelihood_smart_up_gamma = np.exp(log_likelihood_smart_up_gamma)
    likelihood_smart_down_gamma = np.exp(log_likelihood_smart_down_gamma)
    likelihood_chrome_up_gamma = np.exp(log_likelihood_chrome_up_gamma)
    likelihood_chrome_down_gamma = np.exp(log_likelihood_chrome_down_gamma)


    # Printar os resultados (parametros e likelihood)
    print('Smart TV - Download')
    print('MLE:', parametros_smart_down)
    print('Log-likelihood Gaussiana:', log_likelihood_smart_down_gaussiana)
    print('Likelihood Gaussiana:', likelihood_smart_down_gaussiana)
    print('Log-likelihood Gamma:', log_likelihood_smart_down_gamma)
    print('Likelihood Gamma:', likelihood_smart_down_gamma)
    print()
    print('Smart TV - Upload')
    print('MLE:', parametros_smart_up)
    print('Log-likelihood Gaussiana:', log_likelihood_smart_up_gaussiana)
    print('Likelihood Gaussiana:', likelihood_smart_up_gaussiana)
    print('Log-likelihood Gamma:', log_likelihood_smart_up_gamma)
    print('Likelihood Gamma:', likelihood_smart_up_gamma)
    print()
    print('Chromecast - Download')
    print('MLE:', parametros_chrome_down)
    print('Log-likelihood Gaussiana:', log_likelihood_chrome_down_gaussiana)
    print('Likelihood Gaussiana:', likelihood_chrome_down_gaussiana)
    print('Log-likelihood Gamma:', log_likelihood_chrome_down_gamma)
    print('Likelihood Gamma:', likelihood_chrome_down_gamma)
    print()
    print('Chromecast - Upload')
    print('MLE:', parametros_chrome_up)
    print('Log-likelihood Gaussiana:', log_likelihood_chrome_up_gaussiana)
    print('Likelihood Gaussiana:', likelihood_chrome_up_gaussiana)
    print('Log-likelihood Gamma:', log_likelihood_chrome_up_gamma)
    print('Likelihood Gamma:', likelihood_chrome_up_gamma)

    # Salvar os resultados em um arquivo de texto
    if salvar:
        data = {
            "Smart TV - Download": {
                "MLE": parametros_smart_down,
                "Log-likelihood Gaussiana": log_likelihood_smart_down_gaussiana,
                "Likelihood Gaussiana": likelihood_smart_down_gaussiana,
                "Log-likelihood Gamma": log_likelihood_smart_down_gamma,
                "Likelihood Gamma": likelihood_smart_down_gamma
            },
            "Smart TV - Upload": {
                "MLE": parametros_smart_up,
                "Log-likelihood Gaussiana": log_likelihood_smart_up_gaussiana,
                "Likelihood Gaussiana": likelihood_smart_up_gaussiana,
                "Log-likelihood Gamma": log_likelihood_smart_up_gamma,
                "Likelihood Gamma": likelihood_smart_up_gamma
            },
            "Chromecast - Download": {
                "MLE": parametros_chrome_down,
                "Log-likelihood Gaussiana": log_likelihood_chrome_down_gaussiana,
                "Likelihood Gaussiana": likelihood_chrome_down_gaussiana,
                "Log-likelihood Gamma": log_likelihood_chrome_down_gamma,
                "Likelihood Gamma": likelihood_chrome_down_gamma
            },
            "Chromecast - Upload": {
                "MLE": parametros_chrome_up,
                "Log-likelihood Gaussiana": log_likelihood_chrome_up_gaussiana,
                "Likelihood Gaussiana": likelihood_chrome_up_gaussiana,
                "Log-likelihood Gamma": log_likelihood_chrome_up_gamma,
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
        parametros_smart_down = data['Smart TV - Download']['MLE']
        parametros_smart_up = data['Smart TV - Upload']['MLE']
        parametros_chrome_down = data['Chromecast - Download']['MLE']
        parametros_chrome_up = data['Chromecast - Upload']['MLE']

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

# probability plot comparando o dataset com uma distribuição normal parametrizada
def gaussian_probability_plot(dataset, params):
    """
    Plota um Probability Plot comparando o dataset com uma distribuição normal parametrizada.

    Parâmetros:
        dataset (array-like): Os dados reais para comparar com a distribuição.
        params (dict): Um dicionário com os parâmetros da distribuição normal.
            - 'media': Média da distribuição.
            - 'variancia': Variância da distribuição.
    """
    # Extrair parâmetros da distribuição
    media = params['media']
    variancia = params['variancia']
    desvio_padrao = np.sqrt(variancia)

    # Configurar a distribuição normal parametrizada
    dist = stats.norm(loc=media, scale=desvio_padrao)

    # Criar o Probability Plot
    stats.probplot(dataset, dist=dist, plot=plt)
    plt.title("Probability Plot: Dados vs. Distribuição Normal Parametrizada")
    plt.xlabel("Quantis Teóricos")
    plt.ylabel("Quantis Amostrais")
    plt.grid(True)

# probability plot comparando o dataset com uma distribuição gamma parametrizada
def gamma_probability_plot(dataset, params):
    """
    Plota um Probability Plot comparando o dataset com uma distribuição gamma parametrizada.

    Parâmetros:
        dataset (array-like): Os dados reais para comparar com a distribuição.
        params (dict): Um dicionário com os parâmetros da distribuição gamma.
            - 'a': Parâmetro 'a' da distribuição.
            - 'b': Parâmetro 'b' da distribuição.
    """
    # Extrair parâmetros da distribuição
    a = params['a']
    b = params['b']

    # Configurar a distribuição gamma parametrizada
    dist = stats.gamma(a=a, scale=b)

    # Criar o Probability Plot
    stats.probplot(dataset, dist=dist, plot=plt)
    plt.title("Probability Plot: Dados vs. Distribuição Gamma Parametrizada")
    plt.xlabel("Quantis Teóricos")
    plt.ylabel("Quantis Amostrais")
    plt.grid(True)

# Probability plot para cada distribuição usando os parametros do MLE
def passo_5(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, file = "estatisticas_MLE.json", salvar = True):
    # Carregar os resultados do MLE
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        parametros_smart_down = data['Smart TV - Download']['MLE']
        parametros_smart_up = data['Smart TV - Upload']['MLE']
        parametros_chrome_down = data['Chromecast - Download']['MLE']
        parametros_chrome_up = data['Chromecast - Upload']['MLE']

    # plot da distribuição gaussiana
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    gaussian_probability_plot(df_smart_up['bytes_up'], parametros_smart_up)
    plt.title('Smart TV - Upload')
    plt.subplot(2, 2, 2)
    gaussian_probability_plot(df_smart_down['bytes_down'], parametros_smart_down)
    plt.title('Smart TV - Download')
    plt.subplot(2, 2, 3)
    gaussian_probability_plot(df_chrome_up['bytes_up'], parametros_chrome_up)
    plt.title('Chromecast - Upload')
    plt.subplot(2, 2, 4)
    gaussian_probability_plot(df_chrome_down['bytes_down'], parametros_chrome_down)
    plt.title('Chromecast - Download')
    plt.tight_layout()
    if salvar:
        plt.savefig('caracterizando_os_horarios/probplot.png')
    plt.show()

    # plot da distribuição gamma
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    gamma_probability_plot(df_smart_up['bytes_up'], parametros_smart_up)
    plt.title('Smart TV - Upload')
    plt.subplot(2, 2, 2)
    gamma_probability_plot(df_smart_down['bytes_down'], parametros_smart_down)
    plt.title('Smart TV - Download')
    plt.subplot(2, 2, 3)
    gamma_probability_plot(df_chrome_up['bytes_up'], parametros_chrome_up)
    plt.title('Chromecast - Upload')
    plt.subplot(2, 2, 4)
    gamma_probability_plot(df_chrome_down['bytes_down'], parametros_chrome_down)
    plt.title('Chromecast - Download')
    plt.tight_layout()
    if salvar:
        plt.savefig('caracterizando_os_horarios/probplot_gamma.png')
    plt.show()

# Q Q plot comparando os datasets 1 e 3, e os datasets 2 e 4
def passo_6(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar=False):
    # Ordenar os dados
    smart_up_sorted = np.sort(df_smart_up['bytes_up'])
    chrome_up_sorted = np.sort(df_chrome_up['bytes_up'])
    smart_down_sorted = np.sort(df_smart_down['bytes_down'])
    chrome_down_sorted = np.sort(df_chrome_down['bytes_down'])

    # Quantis para os conjuntos menores
    quantis_smart_up = np.linspace(0, 1, len(smart_up_sorted))
    quantis_chrome_up = np.linspace(0, 1, len(chrome_up_sorted))
    quantis_smart_down = np.linspace(0, 1, len(smart_down_sorted))
    quantis_chrome_down = np.linspace(0, 1, len(chrome_down_sorted))

    # Interpolação linear para alinhar os conjuntos
    chrome_up_interp = np.interp(quantis_smart_up, quantis_chrome_up, chrome_up_sorted)
    chrome_down_interp = np.interp(quantis_smart_down, quantis_chrome_down, chrome_down_sorted)

    # Plot do QQ Plot para upload
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(smart_up_sorted, chrome_up_interp, alpha=0.6)
    plt.plot([smart_up_sorted.min(), smart_up_sorted.max()], [smart_up_sorted.min(), smart_up_sorted.max()], 'r--')
    plt.title("QQ Plot: Smart TV Upload vs. Chromecast Upload")
    plt.xlabel("Smart TV Upload Quantiles")
    plt.ylabel("Chromecast Upload Quantiles")
    plt.grid(True)

    # Plot do QQ Plot para download
    plt.subplot(1, 2, 2)
    plt.scatter(smart_down_sorted, chrome_down_interp, alpha=0.6)
    plt.plot([smart_down_sorted.min(), smart_down_sorted.max()], [smart_down_sorted.min(), smart_down_sorted.max()], 'r--')
    plt.title("QQ Plot: Smart TV Download vs. Chromecast Download")
    plt.xlabel("Smart TV Download Quantiles")
    plt.ylabel("Chromecast Download Quantiles")
    plt.grid(True)

    plt.tight_layout()
    if salvar:
        plt.savefig('caracterizando_os_horarios/qq_plot.png')
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
    # passo_3(dataset_1, dataset_2, dataset_3, dataset_4, salvar=True)

    # # passo 4: plotar histograma, pdf gaussiana e pdf gamma na mesma figura
    # passo_4(dataset_1, dataset_2, dataset_3, dataset_4, file = "caracterizando_os_horarios/estatisticas_mle.json", salvar = True)

    # # passo 5: probability plot para cada distribuição usando os parametros do MLE
    # passo_5(dataset_1, dataset_2, dataset_3, dataset_4, file = "caracterizando_os_horarios/estatisticas_mle.json", salvar = True)

    # # passo 6: Q Q plot comparando os datasets 1 e 3, e os datasets 2 e 4
    passo_6(dataset_1, dataset_2, dataset_3, dataset_4, salvar=True)

