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
        filtro_aux = f'tecnico == "{tecnico}"'
        df_filtro = filtro_aux if len(df_filtro) == 0 else df_filtro + ' & ' + filtro_aux

    if len(local) == 1:
        filtro_aux = f'local == "{local[0]}"'
        df_filtro = filtro_aux if len(df_filtro) == 0 else df_filtro + ' & ' + filtro_aux
    
    return df_filtro
 
