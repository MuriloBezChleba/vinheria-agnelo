from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Usuario

@csrf_exempt
def Registro(request):

    data = json.loads(request.body)
    nome  = data.get("name")
    email = data.get("email")
    senha = data.get("senha")
    usuario = Usuario.objects.create(
        nome = nome,
        email = email,
        senha = senha
    )
    return JsonResponse({"nome": usuario.nome})