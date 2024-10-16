
import pandas as pd

def get_dataframe(jogos):

    lista = []

    for i in jogos.all():
        lista.append(i.to_record()["fields"])
    df_jogos = pd.DataFrame(lista)
    cols = df_jogos.columns
    cols = cols.map(lambda x: x.replace(' ','_') if isinstance(x, (str)) else x)
    df_jogos.columns = cols
    df_jogos['Data_do_Jogo'] = pd.to_datetime(df_jogos['Data_do_Jogo']) # converte coluna de obj para datetime
    df_jogos['Temporada'] = df_jogos["Data_do_Jogo"].dt.year

    return df_jogos

def get_filtered_dataframe(filtro, df_jogos):
    # https://medium.com/horadecodar/como-usar-o-query-do-pandas-fdf4a00727dc (query pandas)
    df_jogos = df_jogos.query(filtro) if len(filtro) > 0 else df_jogos
    return df_jogos

def get_indicadores(df_jogos):    

    indicadores = {}

    total_jogos = len(df_jogos.index)
    pontos_possiveis = total_jogos * 3
    pontos_ganhos = df_jogos["Pontos"].sum()
    aproveitamento = 0 if pontos_possiveis == 0 else round(pontos_ganhos/pontos_possiveis*100,2)

    indicadores["Total de Jogos"]   = total_jogos
    indicadores["Pontos possiveis"] = pontos_possiveis
    indicadores["Pontos Ganhos"] = pontos_ganhos
    indicadores["Vitórias"] = len(df_jogos.loc[df_jogos["Resultado"] == "Vitória"])
    indicadores["Derrotas"] = len(df_jogos.loc[df_jogos["Resultado"] == "Derrota"])
    indicadores['Empates'] = len(df_jogos.loc[df_jogos["Resultado"] == "Empate"])
    indicadores['Aproveitamento'] = aproveitamento
    indicadores['Gols_Feitos'] = df_jogos["Gols_Pró"].sum()
    indicadores['Gols_Sofridos'] = df_jogos["Gols_Contra"].sum()
    
    return indicadores
