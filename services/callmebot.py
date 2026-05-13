import requests
from django.conf import settings
import os
from urllib.parse import quote


class CallMeBot:
    
    def __init__(self):
        self.__base_url = settings.CALLMEBOT_API_URL
        self.__phone_number = settings.CALLMEBOT_PHONE_NUMBER
        self.__api_key = settings.CALLMEBOT_API_KEY
        
    def send_message(self, message):
        
        encoded_message = quote(message) # quote transforma caracteres “problemáticos” em um formato seguro para colocar dentro de URLs
        
        response = requests.get(
            url=f'{self.__base_url}?phone={self.__phone_number}&text={encoded_message}&apikey={self.__api_key}',
        )
        return response.text