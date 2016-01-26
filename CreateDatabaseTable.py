
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import json
con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
table = sys.argv[1]

inputData = {"name":"name","inkomster":[],"investeringar":[{"namn":"delinvestering","value":0,"avskrTid":5,"id":1},{"namn":"delinvestering","value":0,"avskrTid":5,"id":2},{"namn":"delinvestering","value":0,"avskrTid":5,"id":3}],"kostnader":[]}
#inputData = {'age': '38', 'id': '3', 'name': 'Melinda'}
data = json.dumps(inputData)
print type(data)
print type("fdsfds")
print data

print "INSERT INTO %s(Budget) VALUES(%s)" %(table,data)
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS %s"% table)
    cur.execute("CREATE TABLE %s (Id INT PRIMARY KEY AUTO_INCREMENT, \
                 Budget BLOB)"%table)

    cur.execute("INSERT INTO %s(Budget) VALUES('%s')" %(table,data))
    print "created table for: %s" %table

