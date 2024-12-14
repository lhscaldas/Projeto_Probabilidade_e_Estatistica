from preprocessamento import *

def passo_1(df_smart, df_chrome, horarios):
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

    return df_smart_up, df_smart_down, df_chrome_up, df_chrome_down


if __name__ == '__main__':
    df1, df2 = preprocessamento()
    horarios_maior_media = {'smart_up': 20, 'smart_down': 20, 'chrome_up': 22, 'chrome_down': 23}

    # passo 1
    dataset_1, dataset_2, dataset_3, dataset_4 = passo_1(df1, df2, horarios_maior_media)
    print(dataset_1.describe())
    print(dataset_1.head())
    print(dataset_2.describe())
    print(dataset_2.head())
    print(dataset_3.describe())
    print(dataset_3.head())
    print(dataset_4.describe())
    print(dataset_4.head())

    # passo 2
