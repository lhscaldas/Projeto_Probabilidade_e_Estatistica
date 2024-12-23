from a_preprocessamento import *
from scipy.stats import chi2
import json

# Teste de hipótese G entre 2 conjuntos de dados
def G_test(dataset1, dataset2, bins='auto', salvar=False):
    """
    Realiza o G-test entre dois conjuntos de dados.

    Parâmetros:
    - dataset1, dataset2: Arrays ou listas contendo os valores.
    - bins: Número de bins ou método para histogramas (padrão: 'auto').

    Retorna:
    - G: Estatística do G-test.
    - p_value: p-valor associado ao teste.
    """
    # Determinar bins comuns a partir dos dois datasets
    bins_edges = np.histogram_bin_edges(np.concatenate([dataset1, dataset2]), bins=bins)
    
    # Calcular as frequências observadas para cada dataset
    freq1, _ = np.histogram(dataset1, bins=bins_edges)
    freq2, _ = np.histogram(dataset2, bins=bins_edges)
    
    # Total de observações em cada dataset
    total1 = freq1.sum()
    total2 = freq2.sum()
    total_combined = total1 + total2

    # Calcular as frequências esperadas para cada bin
    freq_total = freq1 + freq2
    freq_expected1 = freq_total * (total1 / total_combined)
    freq_expected2 = freq_total * (total2 / total_combined)

    # Evitar divisão por zero e log de zero
    freq1 = np.maximum(freq1, 1e-10)
    freq2 = np.maximum(freq2, 1e-10)
    freq_expected1 = np.maximum(freq_expected1, 1e-10)
    freq_expected2 = np.maximum(freq_expected2, 1e-10)

    # Calcular a estatística do G-test
    G1 = 2 * np.sum(freq1 * np.log(freq1 / freq_expected1))
    G2 = 2 * np.sum(freq2 * np.log(freq2 / freq_expected2))
    G = G1 + G2

    # Calcular os graus de liberdade
    df = len(bins_edges) - 1  # Número de bins - 1

    # Calcular o p-valor usando a distribuição qui-quadrado
    p_value = 1 - chi2.cdf(G, df=df)

    # Agrupar resultados em um dicionário
    resultados = {
        'G': G,
        'p_value': p_value,
        'bins_edges': bins_edges,
        'freq1': freq1,
        'freq2': freq2,
        'freq_expected1': freq_expected1,
        'freq_expected2': freq_expected2
    }

    return resultados


if __name__ == '__main__':
    # Salvar
    salvar = True

    # Carregar os datasets
    dataset_1 = pd.read_csv('dataset_1.csv')
    dataset_2 = pd.read_csv('dataset_2.csv')
    dataset_3 = pd.read_csv('dataset_3.csv')
    dataset_4 = pd.read_csv('dataset_4.csv')

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