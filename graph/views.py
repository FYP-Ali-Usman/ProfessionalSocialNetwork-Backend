import pymongo
from bson import json_util, ObjectId
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]
networkCol = mydb["Networks"]

network = {
    'organization': '',
    'authors': [],
    'publications': []
}

returnCopy = {
    'organization': '',
    'authors': [
        {
            '_id': '',
            'Name': '',
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCoAuthor': '',
            'totalCitation': ''
        }
    ],
    'publications' :[
        {
            '_id': '',
            'title': '',
            'year': '',
            'overview': '',
            'catogories': [],
            'author': '',
            'coAuthors': [
                {
                    'name': '',
                    'linkUrl': ''
                }
            ],
            'papaerLink': ''
        }
    ]
}

# Create your views here.
def generateNetwork(org):
    #extract the data and fill both network and the returnCopy
    #save the network only

    returnCopy['organization'] = org
    network['organization'] = org
    for x in authorCol.find({'affiliation': org}):
        returnCopy['authors'].append(x)
        network['authors'].append(x['_id'])
        for j in pubCol.find({'author': x['_id']}):
            returnCopy['publications'].append(j)
            network['publications'].append(j['_id'])
    networkCol.save(network)

def develop(request):
    if request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        print(data)
        print(data['organization'])

        #find if a network of that organization is already present or not
        #if yes, return it
        #if not, generate it then return

        finding = networkCol.find({"organization": data['organization']})
        if finding.count() <= 0:
            print("didn't find the network, creating a newone")
            generateNetwork(data['organization'])

        else:
            print('{0} {1}'.format(finding.count(), ' records found.'))

        if returnCopy['organization'] == '':
            print("return copy is empty")

            for x in finding:
                returnCopy['organization'] = x['organization']
                for j in x['authors']:
                    returnCopy['authors'].append(authorCol.find_one({'_id': j}))
                for j in x['publications']:
                    returnCopy['publications'].append(pubCol.find_one({'_id': j}))

        page_sanitized = json.loads(json_util.dumps(returnCopy))
        return JsonResponse(page_sanitized)