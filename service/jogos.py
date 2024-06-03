
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

def get_indicadores(filtro, df_jogos):    

    df_jogos = df_jogos.query(filtro) if len(filtro) > 0 else df_jogos
    indicadores = {}

    total_jogos = len(df_jogos.index)
    pontos_possiveis = total_jogos * 3
    pontos_ganhos = 0
    vitorias = 0 
    derrotas = 0
    empates = 0

    # for jogo in jogos.all(formula=formula_str):
    #     pontos_ganhos += jogo.pontos
    #     vitorias += 1 if jogo.pontos == 3 else 0
    #     empates += 1 if jogo.pontos == 1 else 0
    #     derrotas += 1 if jogo.pontos == 0 else 0 

    aproveitamento = 0 if pontos_possiveis == 0 else round(pontos_ganhos/pontos_possiveis*100,2)

    indicadores["Total de Jogos"]   = total_jogos
    indicadores["Pontos possiveis"] = pontos_possiveis
    indicadores["Pontos Ganhos"] = pontos_ganhos
    indicadores["Vitórias"] = vitorias
    indicadores["Derrotas"] = derrotas
    indicadores['Empates'] = empates
    indicadores['Aproveitamento'] = aproveitamento

    return indicadores
