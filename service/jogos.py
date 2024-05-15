from models.jogos import Jogos

def get_total_jogos(formula_str):
    jogos = Jogos()
    return (len(jogos.all(fields="Local",formula=formula_str)))

def get_kpi(formula_str):    
    
    indicadores = {}

    total_jogos = get_total_jogos(formula_str)
    pontos_possiveis = total_jogos * 3
    pontos_ganhos = 0
    vitorias = 0 
    derrotas = 0
    empates = 0

    jogos = Jogos()
    for jogo in jogos.all(formula=formula_str):
        pontos_ganhos += jogo.pontos
        vitorias += 1 if jogo.pontos == 3 else 0
        empates += 1 if jogo.pontos == 1 else 0
        derrotas += 1 if jogo.pontos == 0 else 0 

    aproveitamento = 0 if pontos_possiveis == 0 else round(pontos_ganhos/pontos_possiveis*100,2)

    indicadores["Total de Jogos"]   = total_jogos
    indicadores["Pontos possiveis"] = pontos_possiveis
    indicadores["Pontos Ganhos"] = pontos_ganhos
    indicadores["Vitórias"] = vitorias
    indicadores["Derrotas"] = derrotas
    indicadores['Empates'] = empates
    indicadores['Aproveitamento'] = aproveitamento

    return indicadores
