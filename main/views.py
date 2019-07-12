from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

# Create your views here.

def index(request):
    print("working")
    data = {
        'Message': 'All is well.'
    }
    return JsonResponse(data)
    pass