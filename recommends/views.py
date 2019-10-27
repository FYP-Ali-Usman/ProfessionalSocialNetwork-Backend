from django.shortcuts import render
from bson import json_util
import json
from django.http import JsonResponse
from difflib import SequenceMatcher
import pymongo
from bson import json_util, ObjectId

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]

# Create your views here.

def recommend(request):
    if request.method == 'GET':

        pubId = request.GET.get('id')

        returnObj = {
            'sameAuthor': [
                {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': []
                }
            ],
            'notSameAuthor': [
                {
                    'id': '',
                    'title': '',
                    'year': '',
                    'category': []
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
                            'category': []
                        }
                        tempObj['id'] = str(i['_id'])
                        tempObj['title'] = i['title']
                        tempObj['year'] = i['year']
                        tempObj['category'].append(sourceCategories[count1-1])

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
                    'category': ''
                }
                tempObj['id'] = str(j['_id'])
                tempObj['title'] = j['title']
                tempObj['year'] = j['year']
                tempObj['category'] = i
                tempArr.append(tempObj)

        # Now, to merge the different objects with same fields(except categories)
        uniqueIds = []
        uniqueTitles = []
        uniqueYears = []
        uniqueCategories = []
        for i in tempArr:
            if i['title'] not in uniqueTitles:
                uniqueIds.append(i['id'])
                uniqueTitles.append(i['title'])
                uniqueYears.append(i['year'])
                uniqueCategories.append([i['category']])
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
                'category': []
            }
            tempObj['id'] = uniqueIds[idx]
            tempObj['title'] = uniqueTitles[idx]
            tempObj['year'] = uniqueYears[idx]
            tempObj['category'] = uniqueCategories[idx]

            returnObj['notSameAuthor'].append(tempObj)

        returnObj['notSameAuthor'].pop(0)

        page_sanitized = json.loads(json_util.dumps(returnObj))
        # print(authorReturnCopy)
        return JsonResponse(page_sanitized)