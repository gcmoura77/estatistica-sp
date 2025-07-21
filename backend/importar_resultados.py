import requests
import csv
import os
from datetime import datetime

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, 'migration/jogos.csv')

hearders = {
    "accept": "application/json",    
    "Content-Type": "application/json",
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzUzNzI1NjY2fQ.ZJ9dmmUbTN0YxV6gGXG6D8lGdf1x0x9ImYM8HSGFXPA"
}


# Leitura do CSV e inserção no banco
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile: # utf-8-sig removes BOM from the beginning of the file
    reader = csv.DictReader(csvfile)
    for row in reader:
        payload = {
            "adversario": row.get('Adversário', ''),
            "local": row.get('Local', ''),
            "gols_pro": int(row.get('Gols Pró', 0)),
            "gols_contra": int(row.get('Gols Contra', 0)),
            "torneio": row.get('Torneio', ''),
            "data_jogo": str(datetime.strptime(row.get('Data do Jogo', ''), '%d/%m/%Y') if row.get('Data do Jogo') else datetime.now()),
            "nota": float(row.get('Avaliação')) if row.get('Avaliação') else None,
            "tecnico": row.get('Técnico', ''),
        }
        response = requests.post("http://127.0.0.1:8000/jogos/resultado", headers=hearders, json=payload)
        print(response.status_code, response.json())
        
# 422 {'detail': [{'type': 'float_type', 'loc': ['body', 'nota'], 'msg': 'Input should be a valid number', 'input': None}]}
