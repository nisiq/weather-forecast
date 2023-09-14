from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import List, Optional
from uuid import uuid4 #códigosMaioresAleatórios
from fastapi import HTTPException, status, Response


'''
Consumindo API: Openweathermap
Previsão do Tempo Atual
'''

app = FastAPI()
load_dotenv() #Carrega dados do arquivo dotenv


#Armazenar cidades já pesquisadas
banco: List = []
    

#Buscar previsão resumida da cidade escolhida - OK
@app.get("/clima/{cidade}")
async def get_weather(cidade: str):  # Aceita o parâmetro cidade do caminho

    # Chave da API do OpenWeatherMap
    api_key = os.getenv("api_key")

    # Consulta da API com base na cidade 
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid={api_key}&lang=pt_br"

    # Faz a req GET para obter os dados
    requisicao = requests.get(link)

    # Todas as infos 
    requisicao_dict = requisicao.json()

    # "Filtro" das infos
    id = requisicao_dict['sys']['id']
    descricao = requisicao_dict['weather'][0]['description']
    temperatura = requisicao_dict['main']['temp']
    temperatura_max = requisicao_dict['main']['temp_max']
    temperatura_min = requisicao_dict['main']['temp_min']
    
    retorno = {
        "id": id,
        "cidade" : cidade,
        "descricao" : descricao,
        "temperatura" : temperatura,
        "temperatura_min" : temperatura_min,
        "temperatura_max" : temperatura_max}

    #Add infos no banco
    banco.append(retorno)
    # Dados a serem exibidos
    return retorno
   
    
#Buscar histórico das cidades já consultadas - OK
@app.get('/cidades-consultadas')
def listar_cidades():
    #cidade.id = str(uuid4())
    return banco



#Buscar previsão completa da cidade escolhida - OK
@app.get("/clima-completo/{cidade}")
async def get_weather_completo(cidade: str):
    api_key = "00ccfa5448a38fbd2f78cf20a9aecebb"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid={api_key}&lang=pt_br"
    requisicao = requests.get(link)
    return requisicao.json()



#Deletar previsão resumida da cidade escolhida - 
@app.delete('/deletar-clima/{cidade_id}')
async def deletar_cidade(cidade_id: int):
    for cidade in banco:
        if cidade['id'] == cidade_id:
            banco.remove(cidade)
            return cidade.nome, {'Cidade removida com Sucesso'}
        else:
            return {'error': 'Cidade não encontrada'}