import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from math import ceil
import os

# Função para Análise Exploratória de Dados
def eda(salvar=False):
    # carregando o dataset
    print("Current working directory:", os.getcwd())
    df_smart = pd.read_csv('dados/dataset_smart-tv.csv')
    df_chrome = pd.read_csv('dados/dataset_chromecast.csv')

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

    # salvando a EDA
    if salvar:
        with open('EDA/eda.txt', 'w') as f:
            # salvando as primeiras linhas de cada dataset
            f.write("Smart TV - Primeiras linhas\n")
            f.write(str(df_smart.head()) + '\n\n')
            f.write("Chromecast - Primeiras linhas\n")
            f.write(str(df_chrome.head()) + '\n\n')
            # salvando as dimensões
            f.write(f"Smart TV - Dimensões: {df_smart.shape}\n")
            f.write(f"Chromecast - Dimensões: {df_chrome.shape}\n")
            # salvando os dados faltantes
            f.write("Smart TV - Dados faltantes\n")
            f.write(str(df_smart.isnull().sum()) + '\n\n')
            f.write("Chromecast - Dados faltantes\n")
            f.write(str(df_chrome.isnull().sum()) + '\n\n')
            # salvando os valores zero por dispositivo
            f.write(f"Smart TV - Valores zero: bytes_up={zero_smart_up}, bytes_down={zero_smart_down}\n")
            f.write(f"Chromecast - Valores zero: bytes_up={zero_chrome_up}, bytes_down={zero_chrome_down}\n")
            # salvando os valores negativos por dispositivo
            f.write(f"Smart TV - Valores negativos: bytes_up={neg_smart_up}, bytes_down={neg_smart_down}\n")
            f.write(f"Chromecast - Valores negativos: bytes_up={neg_chrome_up}, bytes_down={neg_chrome_down}\n")


# Função para Pré-processamento
def preprocessamento(salvar=False):
    # carregando o dataset
    df_smart = pd.read_csv('dados/dataset_smart-tv.csv')
    df_chrome = pd.read_csv('dados/dataset_chromecast.csv')

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

    # ordenando os dados pela coluna date_hour
    df_smart = df_smart.sort_values(by='date_hour', ascending=True)
    df_chrome = df_chrome.sort_values(by='date_hour', ascending=True)

    # salvando os datasets pré-processados
    if salvar:
        df_smart.to_csv('dados/dataset_smart-tv-preprocessado.csv', index=False)
        df_chrome.to_csv('dados/dataset_chromecast-preprocessado.csv', index=False)
    else:
        print(df_smart.head())
        print(df_chrome.head())

if __name__ == '__main__':
    salvar = True
    eda(salvar=salvar)
    preprocessamento(salvar=salvar)