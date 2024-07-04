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
titulo = st.columns(1)
linha3 = st.columns(5, gap='medium')

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
    st.bar_chart(resultados,color="#FF0000")

with linha2[1]:
    st.subheader("Notas dos Jogos")
    avaliacao = df_filtrado.groupby(["Avaliação"]).size()
    st.bar_chart(avaliacao,color="#000000")

with titulo[0]:
    st.subheader("Últimos resultados")    
    
lista = []
cor = []
for result in df_filtrado.sort_values(by='Data_do_Jogo').iloc[-5:]["Resultado"]:
    lista.insert(0,result[0])
    if result[0] == 'V':
        cor.insert(0, 'bg-green-500 text-white inline-flex ')
    elif result[0] == 'E':
        cor.insert(0,'bg-black text-white inline-flex')
    else:
        cor.insert(0,'bg-red-500 text-white inline-flex')

import streamlit_shadcn_ui as ui

with linha3[0]:
    ui.button(lista[0], key="item_1", class_name=cor[0])
with linha3[1]:
    ui.button(lista[1], key="item_2", class_name=cor[1])
with linha3[2]:
    ui.button(lista[2], key="item_3", class_name=cor[2])
with linha3[3]:
    ui.button(lista[3], key="item_4", class_name=cor[3])
with linha3[4]:
    ui.button(lista[4], key="item_5", class_name=cor[4])

