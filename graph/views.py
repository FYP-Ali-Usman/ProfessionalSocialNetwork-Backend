import pymongo
from bson import json_util, ObjectId
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
import random
from time import sleep
import pprint

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]
networkCol = mydb["Networks"]
# authorNetworkCol = mydb["AuthorNetwork"]

# organization to be saved in the database
network = {
    'organization': '',
    'authors': [],
    'publications': []
}

# contains full information of organization network
FullCopy = {
    'organization': '',
    'authors': [
        {
            '_id': '',
            'Name': '',
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': ''
        }
    ],
    'publications': [
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

# organize information in fullcopy to be returned
#  of organization network
returnCopy = {
    'organization': '',
    'nodes': [
        {
            'id': '',
            'name': '',
            'group': 0,
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': '',
            'degreeCentrality': 0,
            'closenessCentrality': 0,
            'betweennessCentrality': 0,
            'eigenvectorCentrality': 0
        }
    ],
    'links': [
        {
            'source': '',
            'target': '',
            'value': 0,
            'title': '',
            'year': '',
            'overview': '',
            'catogories': [],
            'papaerLink': ''
        }
    ]
}

# contains full information of author network
authorFullCopy = {
    'author': '',
    'organization': '',
    'authors': [
        {
            '_id': '',
            'Name': '',
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': ''
        }
    ],
    'publications': [
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
            'papaerLink': '',
            'color': ''
        }
    ]
}

# organize information in authorFullcopy to be returned
#  of author network
authorReturnCopy = {
    'author': '',
    'organization': '',
    'nodes': [
        {
            'id': '',
            'name': '',
            'group': 0,
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': '',
            'degreeCentrality': 0,
            'closenessCentrality': 0,
            'betweennessCentrality': 0,
            'eigenvectorCentrality': 0,
            'level': 0
        }
    ],
    'links': [
        {
            'source': '',
            'target': '',
            'value': 0,
            'title': '',
            'year': '',
            'overview': '',
            'catogories': [],
            'papaerLink': '',
            'color': ''
        }
    ]
}

# data arrangement for centrality approaches

newArrangement = {
    'subNetworks': [
        {
            'no_id': 0,
            'authors': [],
            'coauthors': [],
            'relations': [
                {
                    'a_id': '',
                    'ca_id': '',
                    'distance': 0
                }
            ]
        }
    ]
}

totalUniqueAuthors = []


# generate the network of organization
def generateNetwork(org):
    # empty the objects before precessing

    network['organization'] = ''
    network['authors'] = []
    network['publications'] = []

    FullCopy['organization'] = ''
    FullCopy['authors'] = [
        {
            '_id': '',
            'Name': '',
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': ''
        }
    ]
    FullCopy['publications'] = [
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

    # extract the data and fill both network and the FullCopy
    # save the network only

    FullCopy['organization'] = org
    network['organization'] = org
    for x in authorCol.find({'affiliation': org}):
        FullCopy['authors'].append(x)
        network['authors'].append(x['_id'])
        for j in pubCol.find({'author': x['_id']}):
            FullCopy['publications'].append(j)
            network['publications'].append(j['_id'])
    networkCol.save(network)


# generate the network of author
def generateAuthorNetwork(personURL, org):
    # empty the objects before precessing

    authorFullCopy['author'] = ''
    authorFullCopy['organization'] = ''
    authorFullCopy['authors'] = [
        {
            '_id': '',
            'Name': '',
            'urlLink': '',
            'affiliation': '',
            'researchInterest': [],
            'totalPaper': '',
            'totalCitation': ''
        }
    ]
    authorFullCopy['publications'] = [
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

    authorFullCopy['author'] = personURL
    authorFullCopy['organization'] = org

    print((personURL))
    # for x in (pubCol.find({"coAuthors.linkUrl": personURL})):
    #     print(x)
    # print('count is')
    # print(pubCol.find({"coAuthors.linkUrl": personURL}).count())

    # authorFullCopy['authors'].pop()
    # authorFullCopy['publications'].pop()

    # see if the personURL is of the author
    # if yes then no need to look for him as a coauthor in the publications because he is the same person
    # if he is not the main entity in our db then he may be present in our publications
    # is said "may be" because some user may directly put the URl into the link without searching on our web

    if authorCol.find({"urlLink": personURL}).count() > 0:

        for x in authorCol.find({"urlLink": personURL}):
            if x['_id'] not in totalUniqueAuthors:
                totalUniqueAuthors.append(str(x['_id']))
            authorFullCopy['authors'].append(x)
            # authorNetwork['authors'].append(x['_id'])

            for j in pubCol.find({'author': x['_id']}):
                authorFullCopy['publications'].append(j)
                # authorNetwork['publications'].append(j['_id'])

                for k in j['coAuthors']:
                    # see if this coauthor is also an author in our db
                    for l in authorCol.find({'Name': k['name'], 'urlLink': k['linkUrl']}):
                        if l['_id'] not in totalUniqueAuthors:
                            totalUniqueAuthors.append(str(l['_id']))
                        authorFullCopy['authors'].append(l)
                        for m in pubCol.find({'author': l['_id']}):
                            authorFullCopy['publications'].append(m)  # may insert duplicate but we'll clean it later

                    # see if this coauthor is also coauthor in another publication
                    for l in pubCol.find({"coAuthors.name": k['name'], "coAuthors.linkUrl": k['linkUrl']}):
                        if l != j:
                            authorFullCopy['publications'].append(l)
                            for m in authorCol.find({'Name': l[
                                '_id']}):  # although no need for loop as this list will contain only one element, but same case exist on many other places on this file so i stick to one way
                                if m['_id'] not in totalUniqueAuthors:
                                    totalUniqueAuthors.append(str(m['_id']))
                                authorFullCopy['authors'].append(m)

    else:

        for x in pubCol.find({"coAuthors.linkUrl": personURL}):
            print(authorCol.find({'_id': x['author']}).count())
            for j in authorCol.find({'_id': x['author']}):  # loop will run one time
                if j['_id'] not in totalUniqueAuthors:
                    totalUniqueAuthors.append(str(j['_id']))
                authorFullCopy['authors'].append(j)

                for k in pubCol.find({'author': j['_id']}):
                    authorFullCopy['publications'].append(k)

    # print(authorFullCopy)


# coppied from https://stackoverflow.com/questions/33469897/dfs-to-implement-a-graph-python
def dfs(graph, start, end, path, result):
    path += [start]
    if start == end:
        result.append(path)
    else:
        for node in graph[start]:
            if node not in path:
                dfs(graph, node, end, path[:], result)


# Create your views here.

def develop(request):
    if request.method == 'POST':

        returnCopy['organization'] = ''
        returnCopy['nodes'] = [
            {
                'id': '',
                'name': '',
                'group': 0,
                'urlLink': '',
                'affiliation': '',
                'researchInterest': [],
                'totalPaper': '',
                'totalCitation': '',
                'degreeCentrality': 0,
                'closenessCentrality': 0,
                'betweennessCentrality': 0,
                'eigenvectorCentrality': 0
            }
        ]
        returnCopy['links'] = [
            {
                'source': '',
                'target': '',
                'value': 0,
                'title': '',
                'year': '',
                'overview': '',
                'catogories': [],
                'papaerLink': ''
            }
        ]

        newArrangement['subNetworks'] = [
            {
                'no_id': 0,
                'authors': [],
                'coauthors': [],
                'relations': [
                    {
                        'a_id': '',
                        'ca_id': '',
                        'distance': 0
                    }
                ]
            }
        ]

        # print(request)
        data = JSONParser().parse(request)
        # print(data)
        # print(data['organization'])

        # find if a network of that organization is already present or not
        # if yes, return it
        # if not, generate it then return

        finding = networkCol.find({"organization": data['organization']})
        if finding.count() <= 0:
            print("didn't find the network, creating a newone")
            generateNetwork(data['organization'])

        else:
            print('{0} {1}'.format(finding.count(), ' records found.'))

        if FullCopy['organization'] == '':
            # print("return copy is empty")

            for x in finding:
                FullCopy['organization'] = x['organization']
                for j in x['authors']:
                    FullCopy['authors'].append(authorCol.find_one({'_id': j}))
                for j in x['publications']:
                    FullCopy['publications'].append(pubCol.find_one({'_id': j}))

        # print("calling fillReturnCopy")

        ############## Code for filling the return copy ################

        returnCopy['organization'] = FullCopy['organization']
        idx = 0
        idx1 = 0
        tempLinks = []
        tempIds = []
        # for idx, j in enumerate(FullCopy['authors']):
        for j in FullCopy['authors'][1:]:
            tempNodes = {
                'id': '',
                'name': '',
                'group': 0,
                'urlLink': '',
                'affiliation': '',
                'researchInterest': [],
                'totalPaper': '',
                'totalCitation': '',
                'degreeCentrality': 0,
                'closenessCentrality': 0,
                'betweennessCentrality': 0,
                'eigenvectorCentrality': 0
            }

            if j == None:
                continue

            tempNodes['id'] = str(j['_id'])
            tempNodes['name'] = j['Name']
            tempNodes['group'] = 1
            tempNodes['urlLink'] = j['urlLink']
            tempNodes['affiliation'] = j['affiliation']
            tempNodes['researchInterest'] = j['researchInterest']
            tempNodes['totalPaper'] = j['totalPaper']
            tempNodes['totalCitation'] = j['totalCitation']
            # print(tempNodes)
            returnCopy['nodes'].append(tempNodes)
            # print(returnCopy['nodes'][-1])

            idx += 1
            tempLinks.append(j['urlLink'])
            tempIds.append(j['_id'])
        idx += 1

        # print(returnCopy['nodes'])
        returnCopy['nodes'].pop(0)

        for j in FullCopy['publications'][1:]:
            # an array to check duplicate coauthors (a previous programming mistake was corrected so this part of code is not needed actually)

            if j == None:
                continue

            duplicateCoauhthorCheck = []
            for k in j['coAuthors']:
                if k['name'] == '' and k['linkUrl'] == '' or k['linkUrl'] in duplicateCoauhthorCheck:
                    continue

                duplicateCoauhthorCheck.append(k['linkUrl'])

                tempNodes = {
                    'id': '',
                    'name': '',
                    'group': 0,
                    'urlLink': '',
                    'affiliation': '',
                    'researchInterest': [],
                    'totalPaper': '',
                    'totalCitation': '',
                    'degreeCentrality': 0,
                    'closenessCentrality': 0,
                    'betweennessCentrality': 0,
                    'eigenvectorCentrality': 0
                }
                tempLinksNodes = {
                    'source': '',
                    'target': '',
                    'value': 0,
                    'title': '',
                    'year': '',
                    'overview': '',
                    'catogories': [],
                    'papaerLink': ''
                }

                tempLinksNodes['value'] = 1
                tempLinksNodes['title'] = j['title']
                tempLinksNodes['year'] = j['year']
                tempLinksNodes['overview'] = j['overview']
                tempLinksNodes['catogories'] = j['catogories']
                tempLinksNodes['papaerLink'] = j['papaerLink']
                tempLinksNodes['source'] = str(j['author'])

                if k['linkUrl'] not in tempLinks:
                    tempNodes['id'] = str(idx1) + str(idx1) + str(idx1)
                    tempNodes['name'] = k['name']
                    tempNodes['group'] = 0
                    tempNodes['urlLink'] = k['linkUrl']
                    returnCopy['nodes'].append(tempNodes)

                    tempLinks.append(k['linkUrl'])
                    tempIds.append(tempNodes['id'])
                    tempLinksNodes['target'] = tempNodes['id']

                else:
                    idx2 = tempLinks.index(k['linkUrl'])
                    tempLinksNodes['target'] = tempIds[idx2]

                returnCopy['links'].append(tempLinksNodes)

                idx1 += 1
                idx += 1
        returnCopy['links'].pop(0)

        ########### Code for filling the return copy ends here ###########

        # make them null to save memory
        network = ''

        ######## starts the code of the filling of newArrangement ########

        # iter = 0
        newArrangement['subNetworks'].pop()
        # for i in returnCopy['links'][112::]:
        for i in returnCopy['links']:

            # the purpose is to pick one element and develop a relation of it with any subnetwork

            match = 0
            tempid = 0
            for j in newArrangement['subNetworks'][::-1]:
                # iter += 1
                tempid = j['no_id']
                if i['source'] in j['authors']:
                    match = 1
                    break
                elif i['target'] in j['coauthors']:
                    match = 2
                    break

            tempArrangement = {
                'no_id': 0,
                'authors': [],
                'coauthors': [],
                'relations': [
                    {
                        'a_id': '',
                        'ca_id': '',
                        'distance': 0
                    }
                ]
            }
            # if iter == 15:
            #     break
            temprelation = {
                'a_id': i['source'],
                'ca_id': i['target'],
                'distance': i['value']
            }
            if match == 1:
                # edit network tempid author
                for j in newArrangement['subNetworks'][::-1]:
                    if j['no_id'] == tempid:
                        if i['target'] not in j['coauthors']:
                            j['coauthors'].append(i['target'])
                        j['relations'].append(temprelation)
                        break

            elif match == 2:
                # edit network tempid coauthor
                for j in newArrangement['subNetworks'][::-1]:
                    if j['no_id'] == tempid:
                        if i['source'] not in j['authors']:
                            j['authors'].append(i['source'])
                        j['relations'].append(temprelation)
                        break

            else:
                # save as new network with tempid += 1

                tempArrangement['no_id'] = len(newArrangement['subNetworks']) + 1
                tempArrangement['authors'].append(i['source'])
                tempArrangement['coauthors'].append((i['target']))
                tempArrangement['relations'].pop()
                tempArrangement['relations'].append(temprelation)

                newArrangement['subNetworks'].append(tempArrangement)

        # print(newArrangement)

        ######## ends the code of the filling of newArrangement ########

        ######### code for the degree cardanility calculation starts here #########

        fullAuthorId = []
        fullAuthorNumbers = []
        fullCoauthorId = []
        fullCoauthorNumbers = []

        for i in newArrangement['subNetworks']:
            authorId = []
            authorDegree = []
            coAuthorId = []
            coAuthorDegree = []

            for j in i['relations']:
                if j['a_id'] in authorId:
                    authorDegree[authorId.index(j['a_id'])] += 1
                else:
                    authorId.append(j['a_id'])
                    authorDegree.append(0)
                    authorDegree[authorId.index(j['a_id'])] = 1
                if j['ca_id'] in coAuthorId:
                    coAuthorDegree[coAuthorId.index(j['ca_id'])] += 1
                else:
                    coAuthorId.append(j['ca_id'])
                    coAuthorDegree.append(0)
                    coAuthorDegree[coAuthorId.index(j['ca_id'])] = 1

            fullAuthorId = fullAuthorId + authorId
            fullAuthorNumbers = fullAuthorNumbers + authorDegree
            fullCoauthorId = fullCoauthorId + coAuthorId
            fullCoauthorNumbers = fullCoauthorNumbers + coAuthorDegree

        for i in returnCopy['nodes']:
            if i['id'] in fullAuthorId:
                i['degreeCentrality'] = fullAuthorNumbers[fullAuthorId.index(i['id'])]
            elif i['id'] in fullCoauthorId:
                i['degreeCentrality'] = fullCoauthorNumbers[fullCoauthorId.index(i['id'])]

        ########## code for the degree cardanility calculation ends here ##########

        ######### code for the closeness and betweenness cardanility calculation begins here #########

        fullAuthorId = []  # working for closeness centrality
        fullAuthorNumbers = []  # working for closeness centrality
        fullCoauthorId = []  # working for betweeneness centrality
        fullCoauthorNumbers = []  # working for betweeneness centrality

        for i in newArrangement['subNetworks']:

            totalNodes = i['authors'] + i['coauthors']

            # Below 4 lines descript my method but I found stackoverflow method more interesting

            # first, search currentStartNode in the network, it can be either author or coauthor
            # see, how many different nodes are connected to this start node
            # explore each node till the end node is reached, keep an eye on the value(cost)
            # explore means to find the path from each node in connections to currentEndNode

            # Implementatiion from here
            # https://stackoverflow.com/questions/33469897/dfs-to-implement-a-graph-python

            graph = {}

            for j in totalNodes:
                graph[j] = []

            for j in i['relations']:
                if j['a_id'] not in graph[j['ca_id']]:
                    graph[j['ca_id']].append(j['a_id'])
                if j['ca_id'] not in graph[j['a_id']]:
                    graph[j['a_id']].append(j['ca_id'])

            allShortestPaths = []  # all shortest paths between 2 nodes
            noOfShortestPaths = []  # e.g first element is 2 then first 2 lists in allShortestPaths are between same nodes

            uniqueStartNode = []
            uniqueEndNode = []
            uniqueResults = []

            for idx3, j in enumerate(totalNodes[:-1:]):
                currentStartNode = j
                sumOfDistanceOfAllNodesFromJ = 0
                closenessCentralityOfJ = 0

                # find shortes path from j to j+1 and others except with itself
                # for k in totalNodes[totalNodes.index(j)+1::]: # .index takes very muct time to execute
                # for k in totalNodes[idx3+1::]:
                for k in totalNodes[::]:
                    if k == j:
                        continue

                    currentEndNode = k

                    # find all paths from j to k
                    result = []

                    for l, ll in enumerate(uniqueStartNode[::]):
                        if ll == currentStartNode and uniqueEndNode[l] == currentEndNode:
                            result = uniqueResults[l]
                        elif ll == currentEndNode and uniqueEndNode[l] == currentStartNode:
                            result = uniqueResults[l]

                    if not result:
                        uniqueStartNode.append(currentStartNode)
                        uniqueEndNode.append(currentEndNode)
                        dfs(graph, currentStartNode, currentEndNode, [], result)
                        uniqueResults.append(result)
                    # sleep(0.25)
                    # print(result)

                    distances = []
                    shortestDistance = 0
                    noOfShortestDistances = 0
                    for l in result:
                        # for m in l[:len(l)-1:]:
                        for idx4, m in enumerate(l[:len(l) - 1:]):
                            # nextM = l[l.index(m)+1]
                            nextM = l[idx4 + 1]  # .index takes very much execution time
                            # distance between m and nextM
                            for o in i['relations']:
                                if o['a_id'] == m and o['ca_id'] == nextM or o['a_id'] == nextM and o['ca_id'] == m:
                                    shortestDistance += o['distance']
                        distances.append(shortestDistance)
                    shortestDistance = min(distances)  # distance between j and k

                    for idx, l in enumerate(distances):
                        if l == shortestDistance:
                            noOfShortestDistances += 1
                            allShortestPaths.append(result[idx])
                    noOfShortestPaths.append(noOfShortestDistances)

                    sumOfDistanceOfAllNodesFromJ += shortestDistance

                # print(sumOfDistanceOfAllNodesFromJ)
                try:
                    closenessCentralityOfJ = sumOfDistanceOfAllNodesFromJ / (len(totalNodes) - 1)
                except:
                    # print('End of a Subnetwork {}'.format(i['authors']))
                    pass
                fullAuthorId.append(j)
                fullAuthorNumbers.append(closenessCentralityOfJ)

            # print(allShortestPaths)
            # print(noOfShortestPaths)

            for j in totalNodes:
                # if '158215821582' == j:
                # print(allShortestPaths)
                # print(totalNodes)

                betweennessOfJ = 0
                inBetween = 0
                totalPaths = 0
                prevStartNode = ''
                prevEndNode = ''

                skip = True  # skip due to not being in between
                hisAuthors = []

                for k in returnCopy['links']:
                    if k['source'] == j:
                        skip = False
                    if k['target'] == j:
                        if k['source'] not in hisAuthors:
                            # if j == '158015801580':
                            #     print(hisAuthors)
                            hisAuthors.append(k['source'])

                        # if j == '158015801580':
                        #     print('{} \n {}'.format(k, len(hisAuthors)))

                        if len(hisAuthors) > 1:
                            skip = False

                if not skip:
                    for idx, k in enumerate(allShortestPaths):
                        startNode = k[0]
                        endNode = k[-1]

                        totalPaths += 1

                        if j in k[::]:  # if j in between the path
                            inBetween += 1

                        # if '5cd9b2314c1c3a308240f938' == j: #zaid ahmed
                        #     print('{}, {}, {}, {}'.format(k, totalPaths, inBetween, betweennessOfJ))

                        if startNode != prevStartNode or endNode != prevEndNode:
                            if idx != (len(allShortestPaths) - 1):
                                betweennessOfJ = betweennessOfJ + inBetween / totalPaths
                            totalPaths = 0
                            inBetween = 0

                        prevStartNode = startNode
                        prevEndNode = endNode
                fullCoauthorId.append(j)
                fullCoauthorNumbers.append(betweennessOfJ)

        for i in returnCopy['nodes']:
            if i['id'] in fullAuthorId:
                i['closenessCentrality'] = fullAuthorNumbers[fullAuthorId.index(i['id'])]
            if i['id'] in fullCoauthorId:
                i['betweennessCentrality'] = fullCoauthorNumbers[fullCoauthorId.index(i['id'])]

        ########## code for the closeness and betweenness cardanility calculation ends here ##########

        page_sanitized = json.loads(json_util.dumps(returnCopy))
        return JsonResponse(page_sanitized)


def entity(request):
    if request.method == 'GET':

        authorReturnCopy['author'] = ''
        authorReturnCopy['organization'] = ''
        authorReturnCopy['nodes'] = [
            {
                'id': '',
                'name': '',
                'group': 0,
                'urlLink': '',
                'affiliation': '',
                'researchInterest': [],
                'totalPaper': '',
                'totalCitation': '',
                'degreeCentrality': 0,
                'closenessCentrality': 0,
                'betweennessCentrality': 0,
                'eigenvectorCentrality': 0,
                'level': 0
            }
        ]
        authorReturnCopy['links'] = [
            {
                'source': '',
                'target': '',
                'value': 0,
                'title': '',
                'year': '',
                'overview': '',
                'catogories': [],
                'papaerLink': '',
                'color': ''
            }
        ]

        newArrangement['subNetworks'] = [
            {
                'no_id': 0,
                'authors': [],
                'coauthors': [],
                'relations': [
                    {
                        'a_id': '',
                        'ca_id': '',
                        'distance': 0
                    }
                ]
            }
        ]

        personURL = request.GET.get('nodeId')
        affiliation = request.GET.get('affiliation')

        generateAuthorNetwork(personURL, affiliation)
        # print(authorFullCopy)

        ############## Code for filling the authorReturnCopy #################

        authorReturnCopy['author'] = authorFullCopy['author']
        authorReturnCopy['organization'] = authorFullCopy['organization']

        idx = 0  # index count
        idx1 = 0  # index count
        tempLinks = []  # for duplicate check in nodes with ids
        tempIds = []  # for duplicate check in nodes with links because coauthors don't have ids

        for j in authorFullCopy['authors'][1:]:

            if j['_id'] in tempIds:
                continue

            tempNodes = {
                'id': '',
                'name': '',
                'group': 0,
                'urlLink': '',
                'affiliation': '',
                'researchInterest': [],
                'totalPaper': '',
                'totalCitation': '',
                'degreeCentrality': 0,
                'closenessCentrality': 0,
                'betweennessCentrality': 0,
                'eigenvectorCentrality': 0,
                'level': 0
            }

            tempNodes['id'] = str(j['_id'])
            tempNodes['name'] = j['Name']
            tempNodes['group'] = 1
            tempNodes['urlLink'] = j['urlLink']
            tempNodes['affiliation'] = j['affiliation']
            tempNodes['researchInterest'] = j['researchInterest']
            tempNodes['totalPaper'] = j['totalPaper']
            tempNodes['totalCitation'] = j['totalCitation']
            # print(tempNodes)

            authorReturnCopy['nodes'].append(tempNodes)
            # print(authorReturnCopy['nodes'][-1])

            idx += 1
            tempLinks.append(j['urlLink'])
            tempIds.append(j['_id'])
        idx += 1
        authorReturnCopy['nodes'].pop(0)
        # print(authorReturnCopy['nodes'])

        print(totalUniqueAuthors)
        number_of_colors = totalUniqueAuthors
        color = []

        for i in range(len(number_of_colors)):
            oka = False
            while not oka:
                thisColor = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                if ((thisColor[1:3:] == 'FF') or (thisColor[3:5:] == 'FF') or (thisColor[5:7:] == 'FF')):
                    oka = False
                else:
                    oka = True
            color.append(thisColor)

        # color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        #          for i in range(len(number_of_colors))]
        print(color)

        for j in authorFullCopy['publications'][1:]:

            for k in j['coAuthors']:

                tempNodes = {
                    'id': '',
                    'name': '',
                    'group': 0,
                    'urlLink': '',
                    'affiliation': '',
                    'researchInterest': [],
                    'totalPaper': '',
                    'totalCitation': '',
                    'degreeCentrality': 0,
                    'closenessCentrality': 0,
                    'betweennessCentrality': 0,
                    'eigenvectorCentrality': 0,
                    'level': 0
                }
                tempLinksNodes = {
                    'source': '',
                    'target': '',
                    'value': 0,
                    'title': '',
                    'year': '',
                    'overview': '',
                    'catogories': [],
                    'papaerLink': '',
                    'color': color[totalUniqueAuthors.index(str(j['author']))]
                }

                # print(color[totalUniqueAuthors.index(str(j['author']))])
                tempLinksNodes['value'] = 1
                tempLinksNodes['title'] = j['title']
                tempLinksNodes['year'] = j['year']
                tempLinksNodes['overview'] = j['overview']
                tempLinksNodes['catogories'] = j['catogories']
                tempLinksNodes['papaerLink'] = j['papaerLink']
                tempLinksNodes['source'] = str(j['author'])

                if k['linkUrl'] not in tempLinks:  # if this is a coauthor

                    tempNodes['id'] = str(idx1) + str(idx1) + str(idx1)
                    tempNodes['name'] = k['name']
                    tempNodes['group'] = 0
                    tempNodes['urlLink'] = k['linkUrl']
                    authorReturnCopy['nodes'].append(tempNodes)

                    tempLinks.append(k['linkUrl'])
                    tempIds.append(tempNodes['id'])
                    tempLinksNodes['target'] = tempNodes['id']

                else:
                    idx2 = tempLinks.index(k['linkUrl'])
                    tempLinksNodes['target'] = tempIds[idx2]

                authorReturnCopy['links'].append(tempLinksNodes)

                idx1 += 1
                idx += 1
        authorReturnCopy['links'].pop(0)

        ########### Code for filling the authorReturnCopy ends here ############

        # make them null to save memory
        network = ''

        ######## starts the code of the filling of newArrangement ########

        # following dictionary will save source and targets to see if the start and end nodes don't have any node between them then no needd to calculate path by doing recursion.
        # directPathHelper = {}

        # sourceList = []
        # targetList = []
        #
        # for i in authorReturnCopy['links']:
        #     # directPathHelper[i['source']] = i['target']
        #     sourceList.append(i['source'])
        #     targetList.append(i['target'])

        # iter = 0
        newArrangement['subNetworks'].pop()
        # for i in authorReturnCopy['links'][112::]:
        for i in authorReturnCopy['links']:

            # the purpose is to pick one element and develop a relation of it with any subnetwork

            match = 0
            tempid = 0
            for j in newArrangement['subNetworks'][::-1]:  # check if record already exists in one subnetwork
                # iter += 1
                tempid = j['no_id']
                if i['source'] in j['authors']:
                    match = 1
                    break
                elif i['target'] in j['coauthors']:
                    match = 2
                    break

            tempArrangement = {
                'no_id': 0,
                'authors': [],
                'coauthors': [],
                'relations': [
                    {
                        'a_id': '',
                        'ca_id': '',
                        'distance': 0
                    }
                ]
            }
            # if iter == 15:
            #     break
            temprelation = {
                'a_id': i['source'],
                'ca_id': i['target'],
                'distance': i['value']
            }
            if match == 1:
                # edit network tempid author
                for j in newArrangement['subNetworks'][::-1]:
                    if j['no_id'] == tempid:
                        if i['target'] not in j['coauthors']:
                            j['coauthors'].append(i['target'])
                        j['relations'].append(temprelation)
                        break

            elif match == 2:
                # edit network tempid coauthor
                for j in newArrangement['subNetworks'][::-1]:
                    if j['no_id'] == tempid:
                        if i['source'] not in j['authors']:
                            j['authors'].append(i['source'])
                        j['relations'].append(temprelation)
                        break

            else:
                # save as new network with tempid += 1

                tempArrangement['no_id'] = len(newArrangement['subNetworks']) + 1
                tempArrangement['authors'].append(i['source'])
                tempArrangement['coauthors'].append((i['target']))
                tempArrangement['relations'].pop()
                tempArrangement['relations'].append(temprelation)

                newArrangement['subNetworks'].append(tempArrangement)

        # print(newArrangement)

        ######## ends the code of the filling of newArrangement ########

        # following 10 lines of code checks for the duplicate enteries in the development environment

        # duplicateCheck = []
        # for i in newArrangement['subNetworks']:
        #     duplicateCheck = i['authors'] + i['coauthors']
        #     print(len(duplicateCheck))
        #     print(len(set(duplicateCheck)))
        #     if (len(duplicateCheck) != len(set(duplicateCheck))):
        #         print('duplicate')
        #     else:
        #         print('no duplicate')

        ######### code for the degree cardanility calculation starts here #########

        fullAuthorId = []
        fullAuthorNumbers = []
        fullCoauthorId = []
        fullCoauthorNumbers = []

        for i in newArrangement['subNetworks']:
            authorId = []
            authorDegree = []
            coAuthorId = []
            coAuthorDegree = []

            for j in i['relations']:
                if j['a_id'] in authorId:
                    authorDegree[authorId.index(j['a_id'])] += 1
                else:
                    authorId.append(j['a_id'])
                    authorDegree.append(0)
                    authorDegree[authorId.index(j['a_id'])] = 1
                if j['ca_id'] in coAuthorId:
                    coAuthorDegree[coAuthorId.index(j['ca_id'])] += 1
                else:
                    coAuthorId.append(j['ca_id'])
                    coAuthorDegree.append(0)
                    coAuthorDegree[coAuthorId.index(j['ca_id'])] = 1

            fullAuthorId = fullAuthorId + authorId
            fullAuthorNumbers = fullAuthorNumbers + authorDegree
            fullCoauthorId = fullCoauthorId + coAuthorId
            fullCoauthorNumbers = fullCoauthorNumbers + coAuthorDegree

        for i in authorReturnCopy['nodes']:
            if i['id'] in fullAuthorId:
                i['degreeCentrality'] = fullAuthorNumbers[fullAuthorId.index(i['id'])]
            elif i['id'] in fullCoauthorId:
                i['degreeCentrality'] = fullCoauthorNumbers[fullCoauthorId.index(i['id'])]

        ########## code for the degree cardanility calculation ends here ##########

        ######### code for the closeness and betweenness cardanility calculation begins here #########

        fullAuthorId = []  # working for closeness centrality
        fullAuthorNumbers = []  # working for closeness centrality
        fullCoauthorId = []  # working for betweeneness centrality
        fullCoauthorNumbers = []  # working for betweeneness centrality
        shortestCoauthorLevel = [] # to know what is the level of the graph

        for i in newArrangement['subNetworks']:

            totalNodes = i['authors'] + i['coauthors']
            # if (len(totalNodes) != len(set(totalNodes))):
            #     print('total nodes: {}, duplicate'.format(len(totalNodes)))
            # else:
            #     print('total nodes: {},  no duplicate'.format(len(totalNodes)))

            # Below 4 lines descript my method but I found stackoverflow method more interesting

            # first, search currentStartNode in the network, it can be either author or coauthor
            # see, how many different nodes are connected to this start node
            # explore each node till the end node is reached, keep an eye on the value(cost)
            # explore means to find the path from each node in connections to currentEndNode

            # Implementatiion from here
            # https://stackoverflow.com/questions/33469897/dfs-to-implement-a-graph-python

            graph = {}

            # graph example = {
            #   'A': ['B', 'C'],
            #   'B': ['A'],
            #   'C': ['A', 'D'],
            #   'D': ['C']

            for j in totalNodes:
                graph[j] = []

            for j in i['relations']:
                if j['a_id'] not in graph[j['ca_id']]:
                    graph[j['ca_id']].append(j['a_id'])
                if j['ca_id'] not in graph[j['a_id']]:
                    graph[j['a_id']].append(j['ca_id'])
            # print(len(graph))

            allShortestPaths = []  # all shortest paths between 2 nodes
            noOfShortestPaths = []  # e.g first element is 2 then first 2 lists in allShortestPaths are between same nodes

            # pprint.pprint(graph)
            # print(graph)

            uniqueStartNode = []
            uniqueEndNode = []
            uniqueResults = []
            # print(totalNodes)

            for idx3, j in enumerate(totalNodes[:-1:]):
                currentStartNode = j
                sumOfDistanceOfAllNodesFromJ = 0
                closenessCentralityOfJ = 0

                print('Path from node: {} ({}/{})'.format(j, idx3, len(totalNodes)))

                # find shortes path from j to j+1 and others except with itself
                # for k in totalNodes[totalNodes.index(j)+1::]: # .index takes very much time to execute
                # for k in totalNodes[idx3+1::]:
                for k in totalNodes[::]:
                    if k == j:
                        continue

                    currentEndNode = k
                    result = []

                    # print(directPathHelper)
                    # if currentStartNode in directPathHelper.keys():
                    #     if currentEndNode == directPathHelper[currentStartNode]:
                    #         # result = [[currentStartNode, currentEndNode]]
                    #         result.append([currentStartNode, currentEndNode])
                    # elif currentStartNode in directPathHelper.values():
                    #     for sourcee, targett in directPathHelper.items():
                    #         if sourcee == currentEndNode and targett == currentStartNode:
                    #             result.append([currentEndNode, currentStartNode])
                    #             # result = [[currentEndNode, currentStartNode]]

                    # if currentStartNode in sourceList:
                    #     if currentEndNode == targetList[sourceList.index(currentStartNode)]:
                    #         result = [[currentStartNode, currentEndNode]]
                    # elif currentStartNode in targetList:
                    #     if currentEndNode == sourceList[targetList.index(currentStartNode)]:
                    #         result = [[currentEndNode, currentStartNode]]
                    #
                    # else:
                    for l, ll in enumerate(uniqueStartNode[::]):
                        if ll == currentStartNode and uniqueEndNode[l] == currentEndNode:
                            result = uniqueResults[l]
                        elif ll == currentEndNode and uniqueEndNode[l] == currentStartNode:
                            result = uniqueResults[l]

                    if not result:
                        uniqueStartNode.append(currentStartNode)
                        uniqueEndNode.append(currentEndNode)
                        dfs(graph, currentStartNode, currentEndNode, [], result)
                        uniqueResults.append(result)
                    # sleep(0.25)
                    # print(result)

                    shortestConnectionLevel = [] # of coauthor with author
                    # this will only run for author
                    if currentStartNode in i['authors'] and currentEndNode in i['coauthors']:
                        if len(result) > 0: # if they are connected
                            step = len(result[0])-1
                            for l in result[1:len(result):]:
                                if ((len(l))-1) < step:
                                    step = len(l)-1

                            for l in authorReturnCopy['nodes']:
                                if l['id'] == currentEndNode:
                                    l['level'] = step

                    distances = []
                    shortestDistance = 0
                    noOfShortestDistances = 0
                    for l in result:
                        # for m in l[:len(l)-1:]:
                        for idx4, m in enumerate(l[:len(l) - 1:]):
                            # nextM = l[l.index(m)+1]
                            nextM = l[idx4 + 1]  # .index takes very much execution time
                            # distance between m and nextM
                            for o in i['relations']:
                                if o['a_id'] == m and o['ca_id'] == nextM or o['a_id'] == nextM and o['ca_id'] == m:
                                    shortestDistance += o['distance']
                        distances.append(shortestDistance)
                    shortestDistance = min(distances)  # distance between j and k

                    for idx, l in enumerate(distances):
                        if l == shortestDistance:
                            noOfShortestDistances += 1
                            allShortestPaths.append(result[idx])
                    noOfShortestPaths.append(noOfShortestDistances)

                    sumOfDistanceOfAllNodesFromJ += shortestDistance

                # print(sumOfDistanceOfAllNodesFromJ)
                try:
                    closenessCentralityOfJ = sumOfDistanceOfAllNodesFromJ / (len(totalNodes) - 1)
                except:
                    # print('End of a Subnetwork {}'.format(i['authors']))
                    pass
                fullAuthorId.append(j)
                fullAuthorNumbers.append(closenessCentralityOfJ)

            # print(allShortestPaths)
            # print(noOfShortestPaths)

            for j in totalNodes:
                # if '158215821582' == j:
                # print(allShortestPaths)
                # print(totalNodes)

                betweennessOfJ = 0
                inBetween = 0
                totalPaths = 0
                prevStartNode = ''
                prevEndNode = ''

                skip = True  # skip due to not being in between
                hisAuthors = []

                for k in authorReturnCopy['links']:
                    if k['source'] == j:
                        skip = False
                    if k['target'] == j:
                        if k['source'] not in hisAuthors:
                            # if j == '158015801580':
                            #     print(hisAuthors)
                            hisAuthors.append(k['source'])

                        # if j == '158015801580':
                        #     print('{} \n {}'.format(k, len(hisAuthors)))

                        if len(hisAuthors) > 1:
                            skip = False

                if not skip:
                    for idx, k in enumerate(allShortestPaths):
                        startNode = k[0]
                        endNode = k[-1]

                        totalPaths += 1

                        if j in k[::]:  # if j in between the path
                            inBetween += 1

                        # if '5cd9b2314c1c3a308240f938' == j: #zaid ahmed
                        #     print('{}, {}, {}, {}'.format(k, totalPaths, inBetween, betweennessOfJ))

                        if startNode != prevStartNode or endNode != prevEndNode:
                            if idx != (len(allShortestPaths) - 1):
                                betweennessOfJ = betweennessOfJ + inBetween / totalPaths
                            totalPaths = 0
                            inBetween = 0

                        prevStartNode = startNode
                        prevEndNode = endNode
                fullCoauthorId.append(j)
                fullCoauthorNumbers.append(betweennessOfJ)

        for i in authorReturnCopy['nodes']:
            if i['id'] in fullAuthorId:
                i['closenessCentrality'] = fullAuthorNumbers[fullAuthorId.index(i['id'])]
            if i['id'] in fullCoauthorId:
                i['betweennessCentrality'] = fullCoauthorNumbers[fullCoauthorId.index(i['id'])]

        ########## code for the closeness and betweenness cardanility calculation ends here ##########

        page_sanitized = json.loads(json_util.dumps(authorReturnCopy))
        # print(authorReturnCopy)
        return JsonResponse(page_sanitized)