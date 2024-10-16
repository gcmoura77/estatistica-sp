import streamlit as st
import streamlit_shadcn_ui as ui
from datetime import datetime
from utils.filtro import get_filtro
from service.jogos import get_indicadores, get_dataframe, get_filtered_dataframe
from models.jogos import Jogos

jogos = Jogos()
df_jogos = get_dataframe(jogos)

# page configuration
st.set_page_config(
    page_title="Estatísticas do São Paulo",
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded")

st.logo('https://media.api-sports.io/football/teams/126.png')

# create a sidebar
with st.sidebar:
    st.title('Estatísticas do São Paulo')
    # st.image('https://media.api-sports.io/football/teams/126.png',)
    
    temporadas = df_jogos["Temporada"].unique().tolist()
    temporadas.insert(0, 'Todas')
    temporada = st.selectbox('Informe a temporada', temporadas, index=0)

    torneios = df_jogos["Torneio"].unique().tolist()
    torneios.insert(0, 'Todos')
    torneio = st.selectbox('Informe o torneio', torneios, index=0)
    
    tecnicos = df_jogos["Técnico"].unique().tolist()
    tecnicos.insert(0, 'Todos')
    tecnico = st.selectbox('Informe o técnico', tecnicos, index=0)

    local = st.multiselect('Informe o local do Jogo', ["Casa","Fora"],["Casa","Fora"])

df_filtro = get_filtro(temporada, torneio, tecnico, local)
df_filtrado = get_filtered_dataframe(df_filtro, df_jogos)
indicadores = get_indicadores(df_filtrado)

#######################
# Dashboard Main Panel

linha1 = st.columns(5, gap='small')
linha2 = st.columns(2, gap='medium')
titulo = st.columns(1)
linha3 = st.columns(5, gap='medium')

primeira_data = df_filtrado.sort_values(by='Data_do_Jogo').iloc[0]["Data_do_Jogo"]
ultima_data = df_filtrado.sort_values(by='Data_do_Jogo').iloc[-1]["Data_do_Jogo"]
quantidade_dias = abs((ultima_data - primeira_data).days)
jogos_dias = round(quantidade_dias/indicadores["Total de Jogos"],2)

with linha1[0]:
    ui.metric_card(title="Total de Jogos", content=indicadores["Total de Jogos"], description="1 jogo a cada "+str(jogos_dias)+" dias", key="card1")


with linha1[1]:
    pontos_por_jogo = indicadores["Pontos Ganhos"]/indicadores["Total de Jogos"]
    ui.metric_card(title="Pontos Ganhos", content=str(indicadores["Pontos Ganhos"]), description=str(round(pontos_por_jogo,2))+" pontos/jogo", key="card2")
    
with linha1[2]:
    ui.metric_card(title="Aproveitamento", content=str(indicadores["Aproveitamento"])+'%', key="card3")

with linha1[3]:
    gols_por_jogo = indicadores["Gols_Feitos"]/indicadores["Total de Jogos"]
    ui.metric_card(title="Gols Feitos", content=str(indicadores["Gols_Feitos"]), description=str(round(gols_por_jogo,2))+" gols/jogo", key="card4")

with linha1[4]:
    gols_por_jogo = indicadores["Gols_Sofridos"]/indicadores["Total de Jogos"]
    ui.metric_card(title="Gols Sofridos", content=str(indicadores["Gols_Sofridos"]), description=str(round(gols_por_jogo,2))+" gols/jogo", key="card5")

with linha2[0]:
    st.subheader("Desempenho dos Jogos")
    resultados = df_filtrado.groupby(["Resultado"]).size()
    st.bar_chart(resultados,color="#FF0000")

with linha2[1]:
    st.subheader("Notas dos Jogos")
    avaliacao = df_filtrado.groupby(["Avaliação"]).size()
    st.bar_chart(avaliacao,color="#000000")

with titulo[0]:
    st.subheader("Últimos resultados")    
    
item = 4
for index, row in df_filtrado.sort_values(by='Data_do_Jogo').iloc[-5:].iterrows():
    if row['Local'] == 'Casa':
        descricao_jogo = 'São Paulo ' + str(row["Gols_Pró"]) + ' x ' + str(row["Gols_Contra"]) + ' ' + row['Adversário']
    else:
        descricao_jogo = row['Adversário'] + ' ' + str(row["Gols_Contra"]) + ' x ' +  str(row["Gols_Pró"]) + ' São Paulo'
    
    if row["Resultado"] == 'Vitória':
        cor = 'bg-green-500 text-white inline-flex '
    elif row["Resultado"] == 'Empate':
        cor = 'bg-black text-white inline-flex'
    else:
        cor = 'bg-red-500 text-white inline-flex'
    
    with linha3[item]:
        ui.button(row["Resultado"][0], key="item_"+str(item), class_name=cor)
        st.caption(descricao_jogo)
    
    item = item - 1

