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
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from scrape import uniAuth
from scrape import authorExtractM
import re

# class URLViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     print("All is well.")
#     queryset = URL.objects.all()
#     serializer_class = URLSerializer
#
#     def post(self, request, format=None):
#         print(request.data)
#         serializer = URLSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def search_author(request):
    print('search_author called')
    if request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        serializer = URLSerializer(data=data)
        # authorExtractM.singleAuthorCrawl(data[0][:data[0].index('publication')+11:])
        for i in data:
            authorExtractM.singleAuthorCrawl(i[:i.index('publication')+11:]+'/search')
            print(i[:i.index('publication')+11:])
        data = {
            'message': "Please refresh your browser"
        }
        return JsonResponse(data)


def search_faculty(request):

    if request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        serializer = URLSerializer(data=data)
        print(data)
        

        if(re.match(regex, data[0]) is None):
            print("URL Validator dosen't validate the URL you provided.")
            data = {
                'bad request': True,
                'bad format': True
            }
            return JsonResponse(data)
        else:
            uniAuth.getAuthInfoLink(data[0], data[1])

            # if serializer.is_valid():
            #             #     # upper page won't return anything so we have to either edit those pages or we can search data from database as those pages are going to save the data into the database.
            #             #     serializer.save()
            #             #     return JsonResponse(serializer.data, status=201)
            # return JsonResponse(serializer.errors, status=200)
            data = {
                'done crawling': True
            }
            return JsonResponse(data)

    elif request.method == 'GET':
        print('got get request')
        snippets = URL.objects.all()
        serializer = URLSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

# 2 lines beneath
# trying to send data as a form from postman instead of json but failed
# unable to parse from request
@api_view(['POST'])
@parser_classes((JSONParser, FormParser, MultiPartParser))
def search_advanced_faculty(request):

    if request.method == 'POST':
        print(request)
        print("working")

        # data1 = FormParser.parse(request, stream, media_type=None, parser_context=None)
        # print(data1)
        data = JSONParser().parse(request)
        serializer = URLSerializer(data=data)
        print(data)
        if not re.match(regex, data[0]):
            print("URL Validator dosen't validate the URL you provided.")
            data = {
                'bad request': True,
                'bad format': True
            }
            return JsonResponse(data)
        else:
            print("URL validaion successful")
#TODO remove this method and add 3rd boolean argument in every request from frontend
            uniAuth.getAuthInfoLink(data[0], data[1], True)
            data = {
                'done crawling': True
            }
            return JsonResponse(data)

def localApplication(request):
    pass

# ===========================================================================