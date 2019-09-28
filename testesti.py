myList = [1,2,3,4,5,'hello']
import json
myJsonList = json.dumps(myList)
print(myJsonList)

abc = "['a','b','c']"
print(abc)
jsonDec = json.decoder.JSONDecoder()
myPythonList = jsonDec.decode(myJsonList)
print(myPythonList)

# ==============================================

import pymongo
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
mycol = mydb["forum_article"]
gg = {"user_id":"1","title":"Science","discription":"What is science","tags":"['a','b','c']"}
bb = {"$set":{"user_id":"1","title":"Sciencehhhh","discription":"What is jjjj science","tags":myJsonList}}
# mycol.update_one(gg, bb)

mydoc = mycol.find()
for x in mydoc:
     print(x['tags'])
     print(x['tags'][0])
     List = jsonDec.decode(x['tags'])
     print(List)
     print(List[0])



