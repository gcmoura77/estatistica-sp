import streamlit as st
from utils.filtro import get_monta_filtro, get_filtro
from service.jogos import get_indicadores, get_dataframe
from models.jogos import Jogos

jogos = Jogos()
df_jogos = get_dataframe(jogos)

# page configuration
st.set_page_config(
    page_title="Estatísticas do São Paulo",
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded")

# create a sidebar
with st.sidebar:
    st.title('Estatísticas do São Paulo')

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

    # https://medium.com/horadecodar/como-usar-o-query-do-pandas-fdf4a00727dc (query pandas)
    df_filtro = get_filtro(temporada, torneio, tecnico, local)

    print('Filtro: ',df_filtro)
    # if len(df_filtro) > 0:
    #     novo = df_jogos.query(df_filtro) 
    #     print(novo)        
    # else:
    #     print(df_jogos.head())


indicadores = get_indicadores(df_filtro, df_jogos)

#######################
# Dashboard Main Panel

linha1 = st.columns(3, gap='medium')
linha2 = st.columns(3, gap='medium')
linha3 = st.columns(3, gap='medium')

with linha1[0]:
    st.metric(label="Total de Jogos", value=indicadores["Total de Jogos"])

with linha1[1]:
    st.metric(label="Pontos Ganhos", value=indicadores["Pontos Ganhos"])
    
with linha1[2]:
    st.metric(label="Aproveitamento", value=str(indicadores["Aproveitamento"])+'%')

with linha2[0]:
    st.metric(label="Vitórias", value = indicadores["Vitórias"])

with linha2[1]:
    st.metric(label="Empates", value=indicadores["Empates"])

with linha2[2]:        
    st.metric(label="Derrotas", value=indicadores["Derrotas"])


