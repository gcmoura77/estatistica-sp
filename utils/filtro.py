from pyairtable.formulas import match, AND, GREATER_EQUAL, LESS_EQUAL
from datetime import date

def get_filtro(temporada, torneio, tecnico, local):
    if temporada != 'Todas':
        df_filtro = f'Temporada == {temporada}'
    else:
        df_filtro = ''

    if torneio != 'Todos':
        filtro_aux = f'Torneio == "{torneio}"'
        df_filtro = filtro_aux if len(df_filtro) == 0 else df_filtro + ' & ' + filtro_aux

    if tecnico != 'Todos':
        filtro_aux = f'Técnico == "{tecnico}"'
        df_filtro = filtro_aux if len(df_filtro) == 0 else df_filtro + ' & ' + filtro_aux

    if len(local) == 1:
        filtro_aux = f'Local == "{local[0]}"'
        df_filtro = filtro_aux if len(df_filtro) == 0 else df_filtro + ' & ' + filtro_aux
    
    return df_filtro

def get_monta_filtro(local, torneio, tecnico, temporada):
    # monta o filtro dos dados
    filtro = {}
    if len(local) == 1:
        filtro["Local"] = local[0]

    if torneio != "Todos":
        filtro["Torneio"] = torneio

    if tecnico != "Todos":
        filtro["Técnico"] = tecnico

    # if temporada != "Todas":

    return match(filtro) 
