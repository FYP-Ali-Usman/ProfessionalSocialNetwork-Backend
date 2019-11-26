from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pymongo
from django.http import StreamingHttpResponse
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
profileCol=mydb["profiles_profile"]

authors=[]
publications=[]
uniqueAuthors=[]
uniquePublications=[]
# ========================================================
# Create your views here.
def yeildMethod(query):
    returnObj = {
        'rauthor': [],
        'rpublications': [],
        'crawl': ''
    }
    global uniqueAuthors
    global uniquePublications
    uniqueAuthors = []
    uniquePublications = []

    ########## checking if words in query match some publications ###########

    data = pubCol.find({"title": {"$regex": "^"+query, "$options": "i"}})
    if data.count() > 0:
        for i in data:
            if i['title'] not in uniquePublications:
                returnObj['rpublications'].append(json.dumps(i, default=json_util.default))
                uniquePublications.append(json.dumps(i['title'], default=json_util.default))


    ########## checking if words in query match some catogories ###########

    words = query.split()
    for i in words:
        print(i)
        # search each word in publication category
        thisPublication = pubCol.find({'catogories': re.compile(".*"+i+".*", re.IGNORECASE)})
        for j in thisPublication:
            if j['title'] not in uniquePublications:
                returnObj['rpublications'].append(json.dumps(j, default=json_util.default))
                uniquePublications.append(json.dumps(j['title'], default=json_util.default))
# ===========================================================
        # search each word in author interests
    thisAuthor = authorCol.find({'researchInterest': query})
    for j in thisAuthor:
        if j['Name'] not in uniqueAuthors:
            returnObj['rauthor'].append(json.dumps(j, default=json_util.default))
            uniqueAuthors.append(json.dumps(j['Name'], default=json_util.default))
# ==============================================================

    ########## checking if words in query match some organizations ###########

    # if found, store them in separate variable and append the variable after searching for author
    foundAuthors = []
    data=authorCol.find({"affiliation":re.compile(".*"+query+".*", re.IGNORECASE)})
    if data.count() != 0:
        for i in data:
            if i['Name'] not in uniqueAuthors:
                foundAuthors.append(i)
                uniqueAuthors.append(json.dumps(i['Name'], default=json_util.default))

    ########## checking if words in query match some authors ###########

    data=authorCol.find({"Name": {"$regex": "^"+query, "$options": "i"}})

    if data.count()==0:
        returnObj['crawl']='crawlAgain'
        for i in foundAuthors:
            returnObj['rauthor'].append(json.dumps(i, default=json_util.default))
        page_sanitized = json.loads(json_util.dumps(returnObj))
        return returnObj
        # ======================
        # for i in range(1):
        #     scrapAuth.getAuthInfoLink(query)
        # data1=authorCol.find({"Name": re.compile(".*"+query+".*", re.IGNORECASE)})
        # for i in data1:
        #     if i['Name'] not in uniqueAuthors:
        #         returnObj['rauthor'].append(i)
        #         uniqueAuthors.append(i['Name'])
        
    else:
        data1=authorCol.find({"Name":re.compile(".*"+query+".*", re.IGNORECASE)})
        for i in data1:
            if i['Name'] not in uniqueAuthors:
                returnObj['rauthor'].append(json.dumps(i, default=json_util.default))
                uniqueAuthors.append(json.dumps(i['Name'], default=json_util.default))
        returnObj['crawl']='crawlAgainNot'
        # returnObj['rauthor'] = returnObj['rauthor'] + foundAuthors
        for i in foundAuthors:
            returnObj['rauthor'].append(json.dumps(i, default=json_util.default))
        page_sanitized = json.loads(json_util.dumps(returnObj))
        return returnObj

def yeildMethod2(query):
    returnObj = {
        'rauthor': []
    }
    global uniqueAuthors
    uniqueAuthors = []
    # for i in range(1):
    #     scrapAuth.getAuthInfoLink(query)
    data1=authorCol.find({"Name": re.compile(".*"+query+".*", re.IGNORECASE)})
    for i in data1:
        if i['Name'] not in uniqueAuthors:
            returnObj['rauthor'].append(json.dumps(i, default=json_util.default))
            uniqueAuthors.append(json.dumps(i['Name'], default=json_util.default))
    page_sanitized = json.loads(json_util.dumps(returnObj))
    return returnObj

class AuthorSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('name', None))
        return Response(yeildMethod(query))

class AfterCrawlSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('name', None))
        return Response(yeildMethod2(query))
        

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

class Favourites(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=str(request.GET.get('id',None))
        # print(query)
        data=profileCol.find_one({"user_id":int(query)})
        # print(data['favouriteAuthors'])
        if data['favouriteAuthors']==None:
            favouriteAuthorss=[]
        else:
            favouriteAuthorss=json.loads(data['favouriteAuthors'])
        authors2=[]
        for ii in favouriteAuthorss:
            # print(ii)
            # print('pp')
            data21=authorCol.find_one({"_id":ObjectId(ii)})
            # print(data2)
            data2=json.dumps(data21, default=json_util.default)
            authors2.append(data2)

        print(authors2)
        return Response(authors2)