import web
import xml.etree.ElementTree as ET

import MySQLdb as mdb
import settings
import sys

tree = ET.parse('user_data.xml')
root = tree.getroot()

urls = (
    '/users', 'list_users','/users/(.*)', 'get_table'
)

app= web.application(urls,globals())

class list_users:
    def GET(self):
        con = mdb.connect(settings.databasehost, settings.databaseuser, settings.databasepassword, settings.database);

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        output = 'users:[';
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        #output.headers["content-type"] ="application/json"
        return output

class get_table:
    def GET(self, table):

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        con = mdb.connect(settings.databasehost, settings.databaseuser, settings.databasepassword, settings.database);
        with con:
            cur = con.cursor()
            cur.execute("select Budget from %s" %table)

            return cur.fetchall()



if __name__ == "__main__":
    app.run()
