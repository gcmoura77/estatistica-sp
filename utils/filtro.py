from pyairtable.formulas import match

def get_monta_filtro(local, torneio, tecnico):
    # monta o filtro dos dados
    filtro = {}
    if len(local) == 1:
        filtro["Local"] = local[0]

    if torneio != "Todos":
        filtro["Torneio"] = torneio

    if tecnico != "Todos":
        filtro["Técnico"] = tecnico

    return match(filtro) 
