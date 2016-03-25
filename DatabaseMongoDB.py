from pymongo import MongoClient
from bson.objectid import ObjectId
#client = MongoClient()
import settings

client = MongoClient(settings.databaseMongo)
inputData = {"name":"new name100","inkomster":[],"investeringar":[{"namn":"delinvestering","value":0,"avskrTid":5,"id":1},{"namn":"delinvestering","value":0,"avskrTid":5,"id":2},{"namn":"delinvestering","value":0,"avskrTid":5,"id":3}],"kostnader":[]}
inputData =  {"name":"ffff","utgifter":[{"id":0,"belopp":7,"antal":1,"beskrivning":"besk1","kategori":"kat1"}],"inkomster":[{"id":0,"belopp":7,"antal":1,"beskrivning":"besk1","kategori":"kat1","kostnad":0}],"investeringar":[{"id":0,"belopp":6000000,"antal":1,"beskrivning":"tomt","kategori":"byggnad","years":50},{"id":1,"belopp":2000000,"antal":1,"beskrivning":"hus","kategori":"byggnad","years":25},{"id":2,"belopp":10000,"antal":2,"beskrivning":"dator","kategori":"inventarier","years":2},{"id":3,"belopp":150000,"antal":1,"beskrivning":"bil","kategori":"fordon","years":5}]}
print type(inputData)


#db = client['mybudget']
db = client["mybudget"]
print db['test'].find()
db['test'].insert_one(inputData)

#coll = db["test"]

#print coll

#cursor = coll.find()

##post = coll.find_one()

#id = "56a779a8a72abd178203b133"
#post ='ObjectId("56a779a8a72abd178203b133")'
#res= coll.find_one({"_id": ObjectId(id)})
#print res

#coll = db.collection_names()
#print coll

#print posts
#print cursor

#for doc in cursor:
#            print (doc['name'])