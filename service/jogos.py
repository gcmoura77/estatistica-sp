import pandas as pd
import requests
import os
from dotenv import load_dotenv

def get_jogos():
    load_dotenv() 

    url = os.environ['ADDRESS_API']
    token = os.environ['API_TOKEN']

    headers = {
        "accept": "application/json",    
        "Content-Type": "application/json",
        "Authorization" : f"Bearer {token}"
    }

    listar = url+'jogos/listar'
    response = requests.get(listar, headers=headers)
    if response.status_code != 200:
        print("Error: ", response.status_code)
        exit()

    response = response.json()
    
    data = response["resultados"]    
    df = pd.DataFrame(data)
    df["data_jogo"] = pd.to_datetime(df["data_jogo"])
    df['Temporada'] = df["data_jogo"].dt.year
    return df

def get_filtered_dataframe(filtro, df_jogos):
    # https://medium.com/horadecodar/como-usar-o-query-do-pandas-fdf4a00727dc (query pandas)
    df_jogos = df_jogos.query(filtro) if len(filtro) > 0 else df_jogos
    return df_jogos

def get_indicadores(df_jogos):    

    indicadores = {}

    total_jogos = len(df_jogos.index)
    pontos_possiveis = total_jogos * 3
    pontos_ganhos = df_jogos["pontos"].sum()
    aproveitamento = 0 if pontos_possiveis == 0 else round(pontos_ganhos/pontos_possiveis*100,2)

    indicadores["Total de Jogos"]   = total_jogos
    indicadores["Pontos possiveis"] = pontos_possiveis
    indicadores["Pontos Ganhos"] = pontos_ganhos
    indicadores["Vitórias"] = len(df_jogos.loc[df_jogos["resultado"] == "Vitória"])
    indicadores["Derrotas"] = len(df_jogos.loc[df_jogos["resultado"] == "Derrota"])
    indicadores['Empates'] = len(df_jogos.loc[df_jogos["resultado"] == "Empate"])
    indicadores['Aproveitamento'] = aproveitamento
    indicadores['Gols_Feitos'] = df_jogos["gols_pro"].sum()
    indicadores['Gols_Sofridos'] = df_jogos["gols_contra"].sum()
    
    return indicadores

def media_avaliacao_jogos(df, ano=None):
    df = df.loc[df["ano"] == ano] if ano else df
    return df["nota"].mean()