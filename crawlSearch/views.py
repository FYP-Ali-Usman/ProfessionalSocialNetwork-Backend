from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pymongo
from bson import json_util
from rest_framework.permissions import IsAuthenticated
from accounts.api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.decorators import api_view, throttle_classes, permission_classes
import json
from bson import ObjectId
import re

# ===================================================
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]
authors=[]
publications=[]
# ========================================================
# Create your views here.
class AuthorSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('name',None))
        data=authorCol.find({"Name":re.compile(".*"+query+".*", re.IGNORECASE)})
        authors=[]
        for i in data:
            data2=json.dumps(i, default=json_util.default)
            authors.append(data2)
        # print(authors)
        return Response(authors)

class OneAuthorSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('id',None))
        data=authorCol.find({"_id":ObjectId(query)})
        authors=[]
        for i in data:
            data2=json.dumps(i, default=json_util.default)
            authors.append(data2)
        # print(authors)
        return Response(authors)

class PublSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('id',None))
        data=pubCol.find({"author":ObjectId(query)})
        publications=[]
        for i in data:
            data2=json.dumps(i, default=json_util.default)
            publications.append(data2)
        # print(authors)
        return Response(publications)

class CoautherSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    