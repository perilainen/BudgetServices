from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()

#client = MongoClient("mongodb://mongodb0.example.net:27019")

inputData = {"name":"name","inkomster":[],"investeringar":[{"namn":"delinvestering","value":0,"avskrTid":5,"id":1},{"namn":"delinvestering","value":0,"avskrTid":5,"id":2},{"namn":"delinvestering","value":0,"avskrTid":5,"id":3}],"kostnader":[]}
db = client['test']

db["test"].insert_one(inputData)

coll = db["test"]

print coll

cursor = coll.find()

##post = coll.find_one()

id = "56a779a8a72abd178203b133"
post ='ObjectId("56a779a8a72abd178203b133")'
res= coll.find_one({"_id": ObjectId(id)})
print res

coll = db.collection_names()
print coll

#print posts
#print cursor

for doc in cursor:
            print (doc['name'])