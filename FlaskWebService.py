from flask import Flask
import web
from pymongo import MongoClient
from bson.objectid import ObjectId
import settings


app = Flask(__name__)

@app.route('/users')
def index():
    print "listin users"
    client = MongoClient()
    db = client['test']
    coll = db.collection_names()
    return str(coll)

@app.route('/users/<string:user>')
def getBudgets(user):
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


@app.route('/users/<string:user>/<string:budget>')
def getBudget(user,budget):
    print 'serving budget'
    client = MongoClient()
    db = client[settings.databaseMongo]
    coll = db[user]
    return str(coll.find_one({"_id": ObjectId(budget)}))

if __name__ == '__main__':
    app.run(debug=True)