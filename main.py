from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import List, Optional
from uuid import uuid4 #códigosMaioresAleatórios
from fastapi import HTTPException, status, Response
from models import Animal, Conta


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
    api_key = "00ccfa5448a38fbd2f78cf20a9aecebb"

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
            return {'Cidade removida com Sucesso'}
        else:
            return {'error': 'Cidade não encontrada'}
        


'''
Criando API: Animais
'''


banco2: List[Animal] = [] #Armazenar lista de animais


@app.get('/animais') #Listar todos os animais da lista
def listar_animais():
    return banco2
 

@app.get('/animais/{animal_id}') #Consultar animal pelo id
def obter_animal(animal_id: str):
    for animal in banco2:
        if animal.id == animal_id:
            return animal
    return {'error': 'Animal não encontrado'}
#para cada animal em banco:
    #se o id do animal for igual ao animal id recebido da rota:
        #retorno o animal


@app.delete('/animais/{animal_id}') #Deletar animal de acordo com o id
def remover_animal(animal_id: str):
    for indexItem in range(len(banco2)):
        if banco2[indexItem].id == animal_id:
            banco2.pop(indexItem)
            return {f'Removido com Sucesso'}
    else:
        return {'error': 'Animal não encontrado'}



@app.post('/animais') #Cadastrar um novo animal
def criar_animal(animal: Animal):
    animal.id = str(uuid4())
    banco2.append(animal)
    return {'Animal cadastrado com sucesso'}



"""
Consumindo API Felipe: Conversor 
"""

@app.get('/moeda') 
async def moeda():
    request = requests.get('http://10.21.62.224:8000/v1/accounts/').json()
    return request


@app.get('/moeda/{cpf}')
async def moeda(cpf:str):
    request = requests.get(f'http://10.21.62.224:8000/v1/accounts/{cpf}').json()
    return request


@app.get('/moeda/{cpf}/convert')
async def moeda(cpf:str):
    request = requests.get(f'http://10.21.62.224:8000/v1/accounts/{cpf}/convert').json()
    return request


@app.post('/moeda')
async def moeda(modelo: Conta):
    request = requests.post('http://10.21.62.224:8000/v1/accounts', json={
        "name": modelo.name,
        "BRL": modelo.BRL,
        "CPF": modelo.CPF
    })
    return request.status_code


if __name__ == '__main__':
    import uvicorn 
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)