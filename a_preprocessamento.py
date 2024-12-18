import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from math import ceil

# Função para Análise Exploratória de Dados
def eda():
    # carregando o dataset
    df_smart = pd.read_csv('dataset_smart-tv.csv')
    df_chrome = pd.read_csv('dataset_chromecast.csv')

    # verificando as primeiras linhas
    print(df_smart.head())
    print(df_chrome.head())

    # verificando as dimensões
    print(df_smart.shape)
    print(df_chrome.shape)

    # verificando dados faltantes
    print(df_smart.isnull().sum())
    print(df_chrome.isnull().sum())

    # verificando valores zero
    zero_smart_up = (df_smart['bytes_up'] == 0).sum()
    zero_smart_down = (df_smart['bytes_down'] == 0).sum()
    print(f"Smart TV - Valores zero: bytes_up={zero_smart_up}, bytes_down={zero_smart_down}")

    zero_chrome_up = (df_chrome['bytes_up'] == 0).sum()
    zero_chrome_down = (df_chrome['bytes_down'] == 0).sum()
    print(f"Chromecast - Valores zero: bytes_up={zero_chrome_up}, bytes_down={zero_chrome_down}")

    # verificando valores negativos
    neg_smart_up = (df_smart['bytes_up'] < 0).sum()
    neg_smart_down = (df_smart['bytes_down'] < 0).sum()
    print(f"Smart TV - Valores negativos: bytes_up={neg_smart_up}, bytes_down={neg_smart_down}")

    neg_chrome_up = (df_chrome['bytes_up'] < 0).sum()
    neg_chrome_down = (df_chrome['bytes_down'] < 0).sum()
    print(f"Chromecast - Valores negativos: bytes_up={neg_chrome_up}, bytes_down={neg_chrome_down}")


# Função para Pré-processamento
def preprocessamento():
    # carregando o dataset
    df_smart = pd.read_csv('dataset_smart-tv.csv')
    df_chrome = pd.read_csv('dataset_chromecast.csv')

    # fazendo um shift de 1 para evitar valores zero
    df_smart['bytes_up'] = df_smart['bytes_up'] + 1
    df_smart['bytes_down'] = df_smart['bytes_down'] + 1
    df_chrome['bytes_up'] = df_chrome['bytes_up'] + 1
    df_chrome['bytes_down'] = df_chrome['bytes_down'] + 1
    
    # reescalonando os dados em log10
    df_smart['bytes_up'] = np.log10(df_smart['bytes_up'])
    df_smart['bytes_down'] = np.log10(df_smart['bytes_down'])
    df_chrome['bytes_up'] = np.log10(df_chrome['bytes_up'])
    df_chrome['bytes_down'] = np.log10(df_chrome['bytes_down'])

    return df_smart, df_chrome

if __name__ == '__main__':
    eda()
    df1, df2 = preprocessamento()