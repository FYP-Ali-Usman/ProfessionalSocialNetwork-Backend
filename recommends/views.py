from django.shortcuts import render
from bson import json_util
import json
from rest_framework.views import APIView
from django.http import JsonResponse
from difflib import SequenceMatcher
import pymongo
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from accounts.api.permissions import IsOwnerOrReadOnly
from bson import json_util, ObjectId
import random

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]
profileCol=mydb["profiles_profile"]

# Create your views here.

class RecommendSearch(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        query=request.GET.get('id',None)
        print(query+'ll')
        data=profileCol.find_one({"user_id":int(query)})

        print(data)
        authInterest=json.loads(data['authInterest'])
        pubInterest=json.loads(data['pubInterest'])
        print(authInterest)
        print(pubInterest)
        getObj = {'author':authInterest,'publication':pubInterest}
        # getObj = {
        #     'author': [
        #         {
        #             'id': '5dbace9b98c5030f80d031bd',
        #             'respect' : 5
        #         },
        #         {
        #             'id': '5db9e1bcb493f95dfeffc688',
        #             'respect' : 2
        #         },
        #         {
        #             'id': '5db9e69cb493f95dfeffc702',
        #             'respect' : 1
        #         },
        #         {
        #             'id': '5d8f9ad7e00db78b02d66092',
        #             'respect' : 2
        #         },
        #         {
        #             'id': '5db9e6b5b493f95dfeffc706',
        #             'respect' : 1
        #         }
        #     ],
        #     'publication': [
        #         {
        #             'id': '5dbad37398c5030f80d0323f',
        #             'respect' : 3
        #         },
        #         {
        #             'id': '5dbacfb698c5030f80d031d9',
        #             'respect' : 8
        #         },
        #         {
        #             'id': '5dbacf0998c5030f80d031c8',
        #             'respect' : 4
        #         },
        #         {
        #             'id': '5db368c5dbea9dd9458eab8a',
        #             'respect' : 3
        #         },
        #         {
        #             'id': '5d8f28f907aa8f22c0e15a05',
        #             'respect' : 4
        #         },
        #         {
        #             'id': '5db9e1c6b493f95dfeffc689',
        #             'respect' : 2
        #         },
        #         {
        #             'id': '5db9e6bcb493f95dfeffc707',
        #             'respect' : 1
        #         },
        #         {
        #             'id': '5db9e6c1b493f95dfeffc708',
        #             'respect': 2
        #         }
        #     ]
        # }

        unsortedAuthorId = []
        unsortedAuthorRespect = []
        unsortedPublicationId = []
        unsortedPublicationRespect = []

        for i in getObj['author']:
            unsortedAuthorId.append(i['id'])
            unsortedAuthorRespect.append(i['respect'])

        for i in getObj['publication']:
            unsortedPublicationId.append(i['id'])
            unsortedPublicationRespect.append(i['respect'])

        # now selection sorting
        # although no need to sort, it will only help in getting things first that is mostly viewed
        authorId = []
        authorRespect = []
        publicationId = []
        publicationRespect = []

        for i in range(len(unsortedAuthorRespect)):
            maxx = max(unsortedAuthorRespect)
            authorRespect.append(maxx)
            authorId.append(unsortedAuthorId[unsortedAuthorRespect.index(maxx)])
            unsortedAuthorId.pop(unsortedAuthorRespect.index(maxx))
            unsortedAuthorRespect.pop(unsortedAuthorRespect.index(maxx))

        for i in range(len(unsortedPublicationRespect)):
            maxx = max(unsortedPublicationRespect)
            publicationRespect.append(maxx)
            publicationId.append(unsortedPublicationId[unsortedPublicationRespect.index(maxx)])
            unsortedPublicationId.pop(unsortedPublicationRespect.index(maxx))
            unsortedPublicationRespect.pop(unsortedPublicationRespect.index(maxx))

        noOfRecommendsbyAuthor = 6
        noOfRecommendsbyPublications = 10
        twentyfivePercentPublication = 2.0

        totalPartsAuthor = 0
        totalPartsPUblications = 0
        for i in authorRespect:
            totalPartsAuthor += i
        for i in publicationRespect:
            totalPartsPUblications += i

        singleAuthorPartSize = noOfRecommendsbyAuthor/totalPartsAuthor
        singlePublicationPartSize = noOfRecommendsbyPublications/totalPartsPUblications

        authorPartsDivision = {}
        publicationPartsDivision = {}

        for idx, i in enumerate(authorId):
            singlePart = authorRespect[idx] * singleAuthorPartSize
            authorPartsDivision[i] = singlePart

        for idx, i in enumerate(publicationId):
            singlePart = publicationRespect[idx] * singlePublicationPartSize
            publicationPartsDivision[i] = singlePart

        spaceLeft = noOfRecommendsbyAuthor

        returnObj = [
            {
                'id': '',
                'title': '',
                'year': '',
                'category': [],
                'author': '',
                'url': ''
            }
        ]

        returnObj.pop() # either write it here or before return

        # Author and Publication respects will take specific space from the limited recommendation size
        # Author's publications will be recommended accordingly by random selection

        for x, y in authorPartsDivision.items():
            reservedPlaces = round(y)
            if reservedPlaces > 0 and spaceLeft >= 0:
                # print('remaining no of spaces are: {}'.format(spaceLeft))
                spaceLeft = spaceLeft - reservedPlaces
                tempObj = {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': [],
                    'author': '',
                    'url': ''
                }
                tempName = ''
                authorList = authorCol.find({'_id': ObjectId(x)})
                if authorList.count() > 0:
                    tempName = authorList[0]['Name']
                publicationList = pubCol.find({'author':ObjectId(x)})
                publicationListIds = []
                publicationListIndexes = []
                if publicationList.count() > 0:
                    allPublicationObjects = [
                        {
                            'id': '',
                            'title': '',
                            'year': '',
                            'category': [
                                
                            ],
                            'author': '',
                            'url': ''
                        }
                    ]
                    allPublicationObjects.pop()
                    for idx1, i in enumerate(publicationList):
                        publicationListIndexes.append(idx1)
                        tempPublication = {
                            'id': '',
                            'title': '',
                            'year': '',
                            'category': [
                                
                            ],
                            'author': '',
                            'url': ''
                        }
                        tempPublication['id'] = i['_id']
                        tempPublication['title'] = i['title']
                        tempPublication['year'] = i['year']
                        tempPublication['category'] = i['catogories']
                        tempPublication['author'] = tempName
                        tempPublication['url'] = i['papaerLink']
                        allPublicationObjects.append(tempPublication)
                    if spaceLeft < 0:
                        toBeRemoved = 0
                        for i in range(0, spaceLeft, -1):
                            toBeRemoved += 1
                        for i in random.sample(publicationListIndexes, len(range(reservedPlaces - toBeRemoved))):
                            returnObj.append(allPublicationObjects[i])
                    else:
        #                 print(random.sample(publicationListIndexes,len(range(reservedPlaces))))
                        for i in random.sample(publicationListIndexes,len(range(reservedPlaces))):
                            # print(i)
        #                     print(publicationList[i])
        #                     print(publicationList.count())
        #                     print(publicationList)
        #                     for idx2, j in enumerate(publicationList):
        #                         if idx2 == i:
        #                             print('running if')
        #                             print(j)
        #                     print(allPublicationObjects[i])
                            returnObj.append(allPublicationObjects[i])

        #                     tempObj['id'] = str(publicationList[i]['_id'])
        #                     tempObj['title'] = publicationList[i]['title']
        #                     tempObj['year'] = publicationList[i]['year']
        #                     tempObj['category'] = publicationList[i]['category']
        #                     print(tempObj)

        # Publication that takes 20% space will be returned 
        spaceLeft = noOfRecommendsbyPublications

        for x, y in publicationPartsDivision.items():
            reservedPlaces = round(y)
            if reservedPlaces > 0 and spaceLeft >= 0:
        #         print('remaining no of spaces are: {}'.format(spaceLeft))
                tempObj = {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': [],
                    'author': '',
                    'url': ''
                }
                if y > twentyfivePercentPublication:
                    # reserve one place from history
                    thisPublication = pubCol.find_one({'_id': ObjectId(x)})
                    
                    tempObj['id'] = x
                    tempObj['title'] = thisPublication['title']
                    tempObj['year'] = thisPublication['year']
                    tempObj['category'] = thisPublication['catogories']
                    thisAuthor = authorCol.find_one({'_id': thisPublication['author']})
                    tempObj['author'] = thisAuthor['Name']
                    tempObj['url'] = thisPublication['papaerLink']
                    returnObj.append(tempObj)
                    
                    publicationPartsDivision[x] = y - 1
                    spaceLeft = spaceLeft - 1
                
        allCategories = []
                    
        # all the categoires of publications are added

        for x, y in publicationPartsDivision.items():
            thisPublication = pubCol.find_one({'_id': ObjectId(x)})
            allCategories += allCategories + thisPublication['catogories']
            
        # see that max number of categories size in our db

        maxSize = 0
        for i in pubCol.aggregate([{'$group': {'_id': None, 'maxSize': {'$max': {'$size': '$catogories'}}}}]):
            maxSize = i['maxSize']

        # combinational search in categories for greater than 2 because we surely can find single categories

        # print('spaceLeft is : {}'.format(spaceLeft))

        requiredPublications = spaceLeft
        searchMixedCategories = [2,3]
        uniquePublications = []

        while requiredPublications > 0:
            tempObj = {
                'id': '',
                'title': '',
                'year': '',
                'category': [],
                'author': '',
                'url': ''
            }
            thisCategory = random.sample(allCategories, random.sample(searchMixedCategories,1)[0])
            thisPublication = pubCol.find({"catogories": {"$all": thisCategory}})
            if thisPublication.count() >= 1:
                selectedPublication = random.sample(list(thisPublication), 1)
                if selectedPublication[0]['title'] not in uniquePublications:
                    tempObj['id'] = str(selectedPublication[0]['_id'])
                    tempObj['title'] = selectedPublication[0]['title']
                    tempObj['year'] = selectedPublication[0]['year']
                    tempObj['category'] = thisCategory
                    thisAuthor = authorCol.find_one({'_id': selectedPublication[0]['author']})
                    tempObj['author'] = thisAuthor['Name']
                    tempObj['url'] = selectedPublication[0]['papaerLink']
                    returnObj.append(tempObj)
                    uniquePublications.append(selectedPublication[0]['title'])
                    requiredPublications -= 1
            
        # for i in returnObj:
        #     print(i)
        #     print('\n\n')

        page_sanitized = json.loads(json_util.dumps(returnObj))
        # print(authorReturnCopy)
        return JsonResponse(page_sanitized)


def recommend(request):
    if request.method == 'GET':

        pubId = request.GET.get('id')

        returnObj = {
            'sameAuthor': [
                {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': [],
                    'url': ''
                }
            ],
            'notSameAuthor': [
                {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': [],
                    'url': ''
                }
            ]
        }

        sourceCategories = []
        source = pubCol.find_one({'_id': ObjectId(pubId)})
        print(source['catogories'])
        sourceCategories = source['catogories']

        print(pubCol.find({'author': source['author']}).count())
        for i in pubCol.find({'author': source['author']}):
            count0 = 0
            leng0 = len(i['catogories'])
            # print('count0 is {} and leng0 is {} '.format(count0, leng0))
            if i['_id'] == source['_id']:
                continue
            while i['catogories']:
                count0 += 1
                count1 = 0
                leng1 = len(sourceCategories)
                # print('count0 is {} '.format(count0))
                # print('count1 is {} and leng1 is {} '.format(count1, leng1))
                while count1 < leng1:
                    count1 += 1
                    # print('count1 is {} '.format(count1))
                    # print("i['catogories'][count0-1] is {} ".format(i['catogories']))
                    # print("sourceCategories[count1-1] is {} ".format(sourceCategories))
                    if SequenceMatcher(None, i['catogories'][-1], sourceCategories[count1-1]).ratio() >= 0.6:
                        print(i['_id'])
                        tempObj = {
                            'id': '',
                            'title': '',
                            'year': '',
                            'category': [],
                            'url': ''
                        }
                        tempObj['id'] = str(i['_id'])
                        tempObj['title'] = i['title']
                        tempObj['year'] = i['year']
                        tempObj['category'].append(sourceCategories[count1-1])
                        tempObj['url'] = i['papaerLink']

                        for j in i['catogories'][-1]:
                            if j in sourceCategories and j not in tempObj['category']:
                                tempObj['category'].append(j)

                        returnObj['sameAuthor'].append(tempObj)

                        count1 = leng1
                        for j in range(leng0-count0):
                            i['catogories'].pop()

                i['catogories'].pop(-1)
        returnObj['sameAuthor'].pop(0)

        tempArr = []
        for i in sourceCategories:
            for j in pubCol.find({"catogories": {"$all": [i]}}):
                if j['_id'] == source['_id']:
                    continue
                tempObj = {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': '',
                    'url': ''
                }
                tempObj['id'] = str(j['_id'])
                tempObj['title'] = j['title']
                tempObj['year'] = j['year']
                tempObj['category'] = i
                tempObj['url'] = j['papaerLink']
                tempArr.append(tempObj)

        # Now, to merge the different objects with same fields(except categories)
        uniqueIds = []
        uniqueTitles = []
        uniqueYears = []
        uniqueCategories = []
        uniqueUrls = []
        for i in tempArr:
            if i['title'] not in uniqueTitles:
                uniqueIds.append(i['id'])
                uniqueTitles.append(i['title'])
                uniqueYears.append(i['year'])
                uniqueCategories.append([i['category']])
                uniqueUrls.append(i['url'])
            else:
                tempIndex = uniqueTitles.index(i['title'])
                if i['category'] not in uniqueCategories[tempIndex]:
                    uniqueCategories[uniqueIds.index(i['id'])].append(i['category'])

        for idx, i in enumerate(uniqueIds):
            # print('id: {}, title: {}, year: {}, category: {}'.format(uniqueIds[idx], uniqueTitles[idx], uniqueYears[idx], uniqueCategories[idx]))
            tempObj = {
                'id': '',
                'title': '',
                'year': '',
                'category': [],
                'url': ''
            }
            tempObj['id'] = uniqueIds[idx]
            tempObj['title'] = uniqueTitles[idx]
            tempObj['year'] = uniqueYears[idx]
            tempObj['category'] = uniqueCategories[idx]
            tempObj['url'] = uniqueUrls[idx]

            returnObj['notSameAuthor'].append(tempObj)

        returnObj['notSameAuthor'].pop(0)

        page_sanitized = json.loads(json_util.dumps(returnObj))
        # print(authorReturnCopy)
        return JsonResponse(page_sanitized)