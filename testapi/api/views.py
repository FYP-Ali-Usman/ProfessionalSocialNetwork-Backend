from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import URLSerializer
from .models import URL
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from scrape import uniAuth
import re
