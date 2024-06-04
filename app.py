import streamlit as st
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

linha1 = st.columns(3, gap='medium')
linha2 = st.columns(2, gap='medium')

import streamlit_shadcn_ui as ui

with linha1[0]:
    # st.metric(label="Total de Jogos", value=indicadores["Total de Jogos"])
    ui.metric_card(title="Total de Jogos", content=indicadores["Total de Jogos"], key="card1")

with linha1[1]:
    # st.metric(label="Pontos Ganhos", value=indicadores["Pontos Ganhos"])
    ui.metric_card(title="Pontos Ganhos", content=str(indicadores["Pontos Ganhos"]), key="card2")
    
with linha1[2]:
    # st.metric(label="Aproveitamento", value=str(indicadores["Aproveitamento"])+'%')
    ui.metric_card(title="Aproveitamento", content=str(indicadores["Aproveitamento"])+'%', key="card3")



with linha2[0]:
    # st.metric(label="Vitórias", value = indicadores["Vitórias"])
    st.subheader("Desempenho dos Jogos")
    resultados = df_filtrado.groupby(["Resultado"]).size()
    st.bar_chart(resultados)

with linha2[1]:
    st.subheader("Locais das Partidas")
    resultados = df_filtrado.groupby(["Local"]).size()
    st.bar_chart(resultados)

