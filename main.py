"""
API utilizada: OpenWeather
 
"""

import requests

api_key = "00ccfa5448a38fbd2f78cf20a9aecebb"
cidade = "campinas"


link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid={api_key}&lang=pt_br"


requisicao = requests.get(link)
requisicao_dict = requisicao.json()
descricao = requisicao_dict['weather'][0]['description']
temperatura = requisicao_dict['main']['temp']

print(descricao, temperatura)