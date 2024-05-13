import os
from pyairtable import Api
import streamlit as st

# Set page title
st.title('Estatísticas do São Paulo')

# Input field for stock symbol
local = st.text_input('Informe Local do Jogo', value='*')

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('appt1Ti26Kq8T2LUq', 'tblmhR0EON7a45Sod')

if local == '*':
    lista_jogos = table.iterate()
else:
    lista_jogos = table.iterate(formula=f'Local = "{local}"')

for record in lista_jogos:
    pontos_possiveis = 0
    pontos_ganhos = 0
    for item in record:
        id_ = item['id']
        created_time = item['createdTime']
        pontos = item['fields']['Pontos']
        pontos_ganhos += int(pontos)
        pontos_possiveis += 3
        # print(f"ID: {id_}, Criado em: {created_time}, Pontos: {pontos}, Local {item['fields']['Local']}, Técnico {item['fields']['Técnico']}")

# print(f"Pontos Possíveis: {pontos_possiveis}, Pontos Ganhos: {pontos_ganhos}, Aproveitamento: {(pontos_ganhos/pontos_possiveis*100)}")


# Display company name and current stock price in bold

st.markdown(f'**Pontos Possíveis:** {pontos_possiveis}')
st.markdown(f'**Pontos Ganhos:** {pontos_ganhos}')

# Closing prices chart
st.subheader('Aproveitamento')
st.metric(label="Aproveitamento", value=str(round(pontos_ganhos/pontos_possiveis*100,2))+'%')

