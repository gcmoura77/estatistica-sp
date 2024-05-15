import streamlit as st
from utils.filtro import get_monta_filtro
from service.jogos import get_kpi

# Set page title
st.title('Estatísticas do São Paulo')

# Input field for stock symbol
torneio = st.selectbox('Informe o torneio', ["Campeonato Paulista","Supercopa","Libertadores", "Brasileirão", "Copa do Brasil", "Todos"], index=5)
tecnico = st.selectbox('Informe o técnico', ["Carpini","Milton Cruz","Zubeldia", "Todos"], index=3)
local = st.multiselect('Informe o local do Jogo', ["Casa","Fora"],["Casa","Fora"])

indicadores = get_kpi(get_monta_filtro(local,torneio,tecnico))

# Display company name and current stock price in bold
st.markdown(f'**Total de Jogos:** {indicadores["Total de Jogos"]}')
st.markdown(f'**Pontos Possíveis:** {indicadores["Pontos possiveis"]}')
st.markdown(f'**Pontos Ganhos:** {indicadores["Pontos Ganhos"]}')
st.markdown(f'**Vitórias:** {indicadores["Vitórias"]}')
st.markdown(f'**Empates:** {indicadores["Empates"]}')
st.markdown(f'**Derrotas:** {indicadores["Derrotas"]}')

# Closing prices chart
st.subheader('Aproveitamento')
st.metric(label="Aproveitamento", value=str(indicadores["Aproveitamento"])+'%')

