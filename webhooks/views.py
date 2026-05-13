from django.shortcuts import render
from rest_framework import views, response, status
from webhooks.models import Webhook
import json
from webhooks.messages import outtflow_message
from services.callmebot import CallMeBot

class WebhookOrderView(views.APIView):
    
    def post(self, request):
        data = request.data
        print("data: ", data)
        
        # Cadastrar o webhook recebido no banco de dados
        Webhook.objects.create(
            event_type=data.get('event_type'),
            event=json.dumps(data, ensure_ascii=False), # ensure_ascii=False serve para não quebrar caracteres especiais e acentos
        )
        
        # Extrai os dados para montar a mensagem do CallMeBot
        product_name = data.get('product')
        quantity = data.get('quantity')
        product_cost_price = data.get('product_cost_price')
        product_selling_price = data.get('product_selling_price')
        total_value = product_selling_price * quantity
        profit = total_value - (product_cost_price * quantity)
        
        # Montar a mensagem para o CallMeBot
        message = outtflow_message.format(
            product_name,
            quantity,
            total_value,
            profit,
        )
        
        # Envio da mensagem para o CallMeBot
        callmebot = CallMeBot()
        callmebot.send_message(message)

        return response.Response(
            data=data,
            status=status.HTTP_200_OK,
        )


