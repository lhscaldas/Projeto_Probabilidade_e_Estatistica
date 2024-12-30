import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Calculo da correlacao entre as taxas de upload e download para cada dispositivo
def correlacao(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar=False):
    # Calculo da correlacao
    correlacao_smart = df_smart_up['bytes_up'].corr(df_smart_down['bytes_down'])
    correlacao_chrome = df_chrome_up['bytes_up'].corr(df_chrome_down['bytes_down'])

    # Salvar em arquivo
    if salvar:
        with open('correlação/correlacao.txt', 'w') as f:
            f.write('Correlacao entre as taxas de upload dos datasets 1 e 2: {:.6f}\n'.format(correlacao_smart))
            f.write('Correlacao entre as taxas de download dos datasets 3 e 4: {:.6f}\n'.format(correlacao_chrome))
    
    return correlacao_smart, correlacao_chrome

# Scatter plot entre as taxas de upload e download para cada dispositivo
def scatter_plot(df_smart_up, df_smart_down, df_chrome_up, df_chrome_down, salvar=False):
    # Criar scatter plot
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Scatter plot para Smart TV
    sns.scatterplot(x=df_smart_up['bytes_up'], y=df_smart_down['bytes_down'], ax=axs[0], color='blue', alpha=0.6)
    axs[0].set_title('Dispositivo Smart-TV')
    axs[0].set_xlabel('Upload')
    axs[0].set_ylabel('Download')

    # Scatter plot para Chromecast
    sns.scatterplot(x=df_chrome_up['bytes_up'], y=df_chrome_down['bytes_down'], ax=axs[1], color='red', alpha=0.6)
    axs[1].set_title('Dispositivo Chromecast')
    axs[1].set_xlabel('Upload')
    axs[1].set_ylabel('Download')

    plt.tight_layout()

    # Salvar em arquivo
    if salvar:
        plt.savefig('correlação/scatter_plot.png')
    plt.show()

if __name__ == '__main__':
    # Salvar os resultados
    salvar = True
    
    # Carregar os datasets
    dataset_1 = pd.read_csv('dados/dataset_1.csv')
    dataset_2 = pd.read_csv('dados/dataset_2.csv')
    dataset_3 = pd.read_csv('dados/dataset_3.csv')
    dataset_4 = pd.read_csv('dados/dataset_4.csv')

    # Calcular correlacao
    correlacao_smart, correlacao_chrome = correlacao(dataset_1, dataset_2, dataset_3, dataset_4, salvar=salvar)
    print('Correlacao entre as taxas de upload dos datasets 1 e 2:', correlacao_smart)
    print('Correlacao entre as taxas de download dos datasets 3 e 4:', correlacao_chrome)

    # Gerar scatter plot
    scatter_plot(dataset_1, dataset_2, dataset_3, dataset_4, salvar=salvar)
