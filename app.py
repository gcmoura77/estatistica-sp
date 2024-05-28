import streamlit as st
from utils.filtro import get_monta_filtro
from service.jogos import get_kpi

# page configuration
st.set_page_config(
    page_title="Estatísticas do São Paulo",
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded")

# create a sidebar
with st.sidebar:
    st.title('Estatísticas do São Paulo')
    
    # Input field for stock symbol
    torneio = st.selectbox('Informe o torneio', ["Campeonato Paulista","Supercopa","Libertadores", "Brasileirão", "Copa do Brasil", "Todos"], index=5)
    tecnico = st.selectbox('Informe o técnico', ["Carpini","Milton Cruz","Zubeldia", "Todos"], index=3)
    local = st.multiselect('Informe o local do Jogo', ["Casa","Fora"],["Casa","Fora"])

indicadores = get_kpi(get_monta_filtro(local,torneio,tecnico))

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


