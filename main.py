from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


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
    descricao = requisicao_dict['weather'][0]['description']
    temperatura = requisicao_dict['main']['temp']
    temperatura_max = requisicao_dict['main']['temp_max']
    temperatura_min = requisicao_dict['main']['temp_min']
    
    # Dados a serem exibidos
    return {
        "descricao" : descricao,
        "temperatura" : temperatura,
        "temperatura_min" : temperatura_min,
        "temperatura_max" : temperatura_max
    }


@app.get("/clima-completo/{cidade}")
async def get_weather_completo(cidade: str):
    api_key = "00ccfa5448a38fbd2f78cf20a9aecebb"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid={api_key}&lang=pt_br"

    requisicao = requests.get(link)

    return requisicao.json()
    
