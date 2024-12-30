import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, chi2
import json

# Função para calcular o G-test entre dois datasets usando scipy.stats.chi2_contingency
def G_test(dataset1, dataset2, bins='auto', salvar=False):
    """
    Realiza o G-test entre dois conjuntos de dados.

    Parâmetros:
    - dataset1, dataset2: Arrays ou listas contendo os valores.
    - bins: Número de bins ou método para histogramas (padrão: 'auto').
    - salvar: Flag para salvar resultados (não implementado na função atual).

    Retorna:
    - resultados: Dicionário com estatística G, p-valor, bins e frequências observadas e esperadas.
    """
    # Determinar bins comuns para os dois datasets
    bins_edges = np.histogram_bin_edges(np.concatenate([dataset1, dataset2]), bins=bins)

    # Calcular as frequências observadas para cada dataset
    freq1, _ = np.histogram(dataset1, bins=bins_edges)
    freq2, _ = np.histogram(dataset2, bins=bins_edges)

    # Criar matriz de contingência
    contingency_table = np.array([freq1, freq2])

    # Calcular os valores esperados usando chi2_contingency
    _, _, _, expected_freq = chi2_contingency(contingency_table, lambda_="log-likelihood")

    # Prevenir divisão por zero e log de zero
    freq1 = np.maximum(freq1, 1e-10)
    freq2 = np.maximum(freq2, 1e-10)
    expected_freq = np.maximum(expected_freq, 1e-10)

    # Calcular a estatística do G-test manualmente
    G = 2 * np.sum(freq1 * np.log(freq1 / expected_freq[0]) + freq2 * np.log(freq2 / expected_freq[1]))

    # Calcular os graus de liberdade
    df = len(bins_edges) - 2  # Número de bins - 1 para frequência - 1 adicional para soma restrita

    # Calcular o p-valor usando a distribuição qui-quadrado
    p_value = 1 - chi2.cdf(G, df=df)

    # Retornar resultados em um dicionário estruturado
    resultados = {
        'G': G,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'bins_edges': bins_edges,
        'freq1': freq1,
        'freq2': freq2,
        'expected_freq': expected_freq
    }

    return resultados



if __name__ == '__main__':
    # Salvar os resultados
    salvar = True

    # Carregar os datasets
    dataset_1 = pd.read_csv('dados/dataset_1.csv')
    dataset_2 = pd.read_csv('dados/dataset_2.csv')
    dataset_3 = pd.read_csv('dados/dataset_3.csv')
    dataset_4 = pd.read_csv('dados/dataset_4.csv')

    # Teste de hipótese G
    bins = 18
    resultados_13 = G_test(dataset_1['bytes_up'], dataset_3['bytes_up'], bins=bins)
    print("Teste de hipótese G entre os datasets 1 e 3:")
    print("Estatística de teste para upload:", resultados_13['G'])
    print("p-valor associado ao teste:", resultados_13['p_value'])
    resultados_24 = G_test(dataset_1['bytes_up'], dataset_4['bytes_up'], bins=bins)
    print("\nTeste de hipótese G entre os datasets 2 e 4:")
    print("Estatística de teste para upload:", resultados_24['G'])
    print("p-valor associado ao teste:", resultados_24['p_value'])

    # Salvar resultados
    if salvar:
        with open('G_test/resultados_13.json', 'w') as f:
            resultados_13_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in resultados_13.items()}
            json.dump(resultados_13_serializable, f, indent=4)
        with open('G_test/resultados_24.json', 'w') as f:
            resultados_24_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in resultados_24.items()}
            json.dump(resultados_24_serializable, f, indent=4)