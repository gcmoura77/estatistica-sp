import streamlit as st
import streamlit_shadcn_ui as ui
from utils.filtro import get_filtro
from service.jogos import get_indicadores, get_filtered_dataframe, media_avaliacao_jogos, get_jogos
import plotly.graph_objects as go

df_jogos = get_jogos()

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
    
    temporadas = sorted(df_jogos["Temporada"].unique().tolist(), reverse=True)
    temporadas.insert(0, 'Todas')
    temporada = st.selectbox('Informe a temporada', temporadas, index=0)

    torneios = sorted(df_jogos["torneio"].unique().tolist())
    torneios.insert(0, 'Todos')
    torneio = st.selectbox('Informe o torneio', torneios, index=0)
    
    tecnicos = sorted(df_jogos["tecnico"].unique().tolist())
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
linha4 = st.columns(1)

primeira_data = df_filtrado.sort_values(by='data_jogo').iloc[0]["data_jogo"]
ultima_data = df_filtrado.sort_values(by='data_jogo').iloc[-1]["data_jogo"]
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
    resultados = df_filtrado.groupby(["resultado"]).size()
    st.bar_chart(resultados,color="#FF0000")

with linha2[1]:
    st.subheader("Notas dos Jogos")
    avaliacao = df_filtrado.groupby(["nota"]).size()
    st.bar_chart(avaliacao,color="#000000")

with titulo[0]:
    st.subheader("Últimos resultados")    
    
item = 4
for index, row in df_filtrado.sort_values(by='data_jogo').iloc[-5:].iterrows():
    if row['local'] == 'Casa':
        descricao_jogo = 'São Paulo ' + str(row["gols_pro"]) + ' x ' + str(row["gols_contra"]) + ' ' + row['adversario']
    else:
        descricao_jogo = row['adversario'] + ' ' + str(row["gols_contra"]) + ' x ' +  str(row["gols_pro"]) + ' São Paulo'
    
    if row["resultado"] == 'Vitória':
        cor = 'bg-green-500 text-white inline-flex '
    elif row["resultado"] == 'Empate':
        cor = 'bg-black text-white inline-flex'
    else:
        cor = 'bg-red-500 text-white inline-flex'
    
    with linha3[item]:
        ui.button(row["resultado"][0], key="item_"+str(item), class_name=cor)
        st.caption(descricao_jogo)
    
    item = item - 1

with linha4[0]:
    media_avaliacao = round(media_avaliacao_jogos(df_filtrado),2)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = media_avaliacao,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {"text" : "Avaliação A&T", "font": {"size": 32, "color": "black"}},
        gauge = {'axis': {'range': [None, 5]},
                'bar': {'color': "gray", "thickness": 0.3, },
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 4], 'color': 'yellow'},
                    {'range': [4, 5], 'color': 'green'},],
                },))
    
    st.plotly_chart(fig, use_container_width=True)
    
    

    
    
