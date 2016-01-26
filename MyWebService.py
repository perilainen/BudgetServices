import web
import xml.etree.ElementTree as ET

tree = ET.parse('user_data.xml')
root = tree.getroot()

urls = (
    '/users', 'list_users','/users/(.*)', 'get_user'
)

app= web.application(urls,globals())

class list_users:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        output = 'users:[';
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        #output.headers["content-type"] ="application/json"
        return output

class get_user:
    def GET(self, user):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        for child in root:
            if child.attrib['id'] == user:
                return str(child.attrib)



if __name__ == "__main__":
    app.run()
