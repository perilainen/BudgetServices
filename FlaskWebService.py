from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import settings
from datetime import timedelta
from flask import make_response, request, current_app, jsonify
from functools import update_wrapper
import json
import warnings

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def deprecated(func):

    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''
    def new_func(*args, **kwargs):
       warnings.warn("Call to deprecated function {}.".format(func.__name__),
                        category=DeprecationWarning)
       return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

app = Flask(__name__)
client = MongoClient(settings.databaseMongo)
@app.route('/api/users')
@crossdomain(origin='*')
def index():
    print "listin users"

    db = client[settings.dataBaseMongoTable]
    coll = db.collection_names()
    list = []
    for item in coll:
        jsonitem = {"name":item}
        list.append(jsonitem)
    return json.dumps(list)

@app.route('/api/adduser/<string:user>')
@crossdomain(origin='*')
def addUser(user):
    print 'adding user'
    #client = MongoClient(settings.databaseMongo)
    db = client[settings.dataBaseMongoTable]
    test = db.create_collection(user)
    print test
    return "test"

@app.route('/api/users/<string:user>')
@crossdomain(origin='*')
def getBudgetsOld(user):
    print 'listing budgets for '+user
    #client = MongoClient(settings.databaseMongo)
    db = client[settings.dataBaseMongoTable]
    coll = db[user]
    cursor = coll.find()
    output = []
    for doc in cursor:
        item = {"Objectid": str(doc['_id'])}
        item["name"]=doc['name']
        print str(doc['_id'])
        #output.append( ['name:'+doc['name'] +'; ObjectId:'+str(doc['_id'])])
        output.append(item)
    print output
    return json.dumps(output)


@app.route('/api/budgets/<string:user>')
@crossdomain(origin='*')
def getBudgets(user):
    print 'listing budgets for '+user
    #client = MongoClient(settings.databaseMongo)
    db = client[settings.dataBaseMongoTable]
    coll = db[user]
    cursor = coll.find()
    output = []
    for doc in cursor:
        item = {"Objectid": str(doc['_id'])}
        item["name"]=doc['name']
        print str(doc['_id'])
        #output.append( ['name:'+doc['name'] +'; ObjectId:'+str(doc['_id'])])
        output.append(item)
    print output
    return json.dumps(output)

@deprecated
@app.route('/api/users/<string:user>/<string:budget>')
@crossdomain(origin='*')
def getBudget(user,budget):
    print 'serving budget'
    #client = MongoClient(settings.databaseMongo)
    db = client[settings.dataBaseMongoTable]
    coll = db[user]

    print str(coll.find_one({"_id": ObjectId(budget)}))
    #return (str(coll.find_one({"_id": ObjectId(budget)})))
    return JSONEncoder().encode((coll.find_one({"_id": ObjectId(budget)})))
    #resp = Response(response json.dumps(json.loads(json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))))= ,status=200,mimetype="application/json" )
    #print json.dumps(json.loads(json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))))

    #return json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))
    #return coll.find_one({"_id": ObjectId(budget)})



@app.route('/api/saveBudget',methods=['PUT'])
def saveBudget():
    user= request.args.get('user')
    data = request.json
    db = client[settings.dataBaseMongoTable]
    coll = db[user]
    print data
    print type(data)
    coll.insert_one(data)
    return "budget saved"

@app.route('/api/deleteBudget', methods = ['DELETE'])
def deleteBudget():
    objektid = request.args.get('objectid')
    user = request.args.get('user')

    db = client[settings.dataBaseMongoTable]
    coll = db[user]

    coll.delete_one({ "_id" : ObjectId(objektid) } )
    return "Budget deleted"

@app.route('/api/getBudget')
@crossdomain(origin='*')
def getCurrBudget():
    print 'serving budget'
    budget = request.args.get('budget')
    user= request.args.get('user')
    #client = MongoClient(settings.databaseMongo)
    db = client[settings.dataBaseMongoTable]
    coll = db[user]

    print str(coll.find_one({"_id": ObjectId(budget)}))
    #return (str(coll.find_one({"_id": ObjectId(budget)})))
    return JSONEncoder().encode((coll.find_one({"_id": ObjectId(budget)})))
    #resp = Response(response json.dumps(json.loads(json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))))= ,status=200,mimetype="application/json" )
    #print json.dumps(json.loads(json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))))

    #return json.dumps(str(coll.find_one({"_id": ObjectId(budget)})))
    #return coll.find_one({"_id": ObjectId(budget)})


if __name__ == '__main__':
    app.run(debug=True, port=4000)
#    print "starting app"
#    CORS(app)



