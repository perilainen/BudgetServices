import web
from pymongo import MongoClient
from bson.objectid import ObjectId
import settings


urls = (
    '/users', 'list_users',
    '/users/(.+)', 'list_budgets',
    '/users/(.+)/(.+)', 'get_budget'
)

app= web.application(urls,globals())


class list_users:
    def GET(self):
        print "listin users"
        client = MongoClient()
        db = client['test']
        coll = db.collection_names()
        return coll


class list_budgets:
    def GET(self, user):
        print 'listing budgets'
        client = MongoClient()
        db = client[settings.databaseMongo]
        coll = db[user]
        cursor = coll.find()
        output = 'Budgets:[';
        for doc in cursor:
            output += ('name:'+doc['name'])+'; ObjectId:'+str(doc['_id'])+ ','
        output += ']';
        return output
class get_budget:
    def GET(self,user,docId):
        print 'serving budget'
        client = MongoClient()
        db = client[settings.databaseMongo]
        coll = db[user]
        return coll.find_one({"_id": ObjectId(docId)})



if __name__ == "__main__":
    app.run()


