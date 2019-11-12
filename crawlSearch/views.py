from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import pymongo
from bson import json_util
from rest_framework.permissions import IsAuthenticated
from accounts.api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.decorators import api_view, throttle_classes, permission_classes
import json
from bson import ObjectId
import re
from crawlSearch import scrapAuth
from crawlSearch import authorExtractl


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
        returnObj = {
            'rauthor': [],
            'rpublications': []
        }
        query=str(request.GET.get('name',None))
        data=authorCol.find({"Name": {"$regex": "^"+query, "$options": "i"}})
        
        # if ' ' in query:
        #     pubData=pubCol.find({"title":{ "$regex": "^"+query, "$options": "i"}})
        # print(data)

        if data.count()==0:
            # for i in range(1):
            #     scrapAuth.getAuthInfoLink(query)
            data1=authorCol.find({"Name": re.compile(".*"+query+".*", re.IGNORECASE)})
            # authors=[]
            for i in data1:
                data2=json.dumps(i, default=json_util.default)
                # authors.append(data2)
                returnObj['rauthor'].append(data2)
        else:
            data1=authorCol.find({"Name":re.compile(".*"+query+".*",re.IGNORECASE)})
            for i in data1:
                returnObj['rauthor'].append(i)

        print(returnObj)
        page_sanitized = json.loads(json_util.dumps(returnObj))
        return JsonResponse(page_sanitized)
        # scrapAuth.getAuthInfoLink(query)

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
    def get(self, request, format=None):
        query=str(request.GET.get('url',None))
        print(query)
        urll=str(query[:query.index('publication')+11:])
        print(urll)
        for i in range(1):
            authorExtractl.singleAuthorCrawl(urll)
        data1=authorCol.find({'urlLink': urll}, {'urlLink': 1})
        authors=[]
        for i in data1:
            data2=json.dumps(i, default=json_util.default)
            authors.append(data2)
        print(authors)
        return Response(authors)

class onePublSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('id',None))
        data=pubCol.find({"_id":ObjectId(query)})
        publications=[]
        for i in data:
            data2=json.dumps(i, default=json_util.default)
            publications.append(data2)
        # print(authors)
        return Response(publications)