from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Restaurant, MenuItem, Base
from sqlalchemy import create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker
from operator import itemgetter
from urlparse import urlparse, parse_qs


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parseResult = urlparse(self.path)
        path = parseResult.path
        qs = parse_qs(parseResult.query)
        if path.endswith('/restaurants'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            #build html
            self.wfile.write(buildRestaurantListHTML())
            return


        elif path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            restaurantId = qs['id'][0]
            restaurant = session.query(Restaurant).filter(Restaurant.id==restaurantId).one()
            output = ""
            output += "<html><body>"
            output += "<h1>Editing "+restaurant.name+" </h1>"
            output += """<form method='POST' enctype='multipart/form-data' action="/edit?id="""+str(restaurant.id)+'">'
            output += '''<h2>Rename it to??</h2><input name="new_name" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
        elif path.endswith("/delete"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            restaurantId = qs['id'][0]
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
            output = ""
            output += "<html><body>"
            output += "<h1>Confirm deletion of "+restaurant.name+" ?</h1>"
            output += '''<form method='POST' action="confirm-delete?id='''+str(restaurant.id)+'">'
            output += '''<button type=submit>Delete</button></form></body></html>'''

            self.wfile.write(output)
        elif path.endswith('/restaurants/new'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += "<html><body>"
            output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"""
            output += '''<h2>Enter new restaurant name</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"

            self.wfile.write(output)
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        parseResult = urlparse(self.path)
        path = parseResult.path
        qs = parse_qs(parseResult.query)
        print path
        print qs
        try:
            if path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                print ctype, pdict
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurantName = fields.get('new_name')
                    restaurantId = qs['id']
                    renameRestaurant(restaurantId[0], new_restaurantName[0])

                self.send_response(301)
                self.send_header('Location', 'http://localhost:8080/restaurants')
                self.end_headers()
            elif path.endswith('/confirm-delete'):
                restaurantId = qs['id'][0]
                deleteRestaurant(restaurantId)
                self.send_response(301)
                self.send_header('Location', 'http://localhost:8080/restaurants')
                self.end_headers()
            elif path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                print ctype, pdict
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurantName = fields.get('name')
                    addNewRestaurant(new_restaurantName[0])

                self.send_response(301)
                self.send_header('Location', 'http://localhost:8080/restaurants')
                self.end_headers()
        except:
            pass

def setupDB():
    global session
    engine = create_engine('sqlite:///restaurantmenu.db', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

def buildRestaurantListHTML():
    output = ''
    output+='<head><body>'
    output+='<p><a href="http://localhost:8080/restaurants/new">Create new Restaurant</a></p>'
    for restaurant in session.query(Restaurant).all():
        output+='<p><h4>'+restaurant.name+'</h4>'
        output+='<a href="http://localhost:8080/edit?id='+str(restaurant.id)+'">Edit</a>'
        output+='</br><a href="http://localhost:8080/delete?id='+str(restaurant.id)+'">Delete</a></p>'
    return output+'</body></head>'

def renameRestaurant(id, newName):
    oldRestaurant = session.query(Restaurant).\
                            filter(Restaurant.id==id).one()
    oldRestaurant.name = newName
    session.add(oldRestaurant)
    session.commit()

def addNewRestaurant(newName):
    session.add(Restaurant(name=newName))
    session.commit()
def deleteRestaurant(id):
    restaurant = session.query(Restaurant).\
                        filter(Restaurant.id == id).one()
    session.delete(restaurant)
    session.commit()
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " Stopping web server...."
        server.socket.close()
        session.close()

if __name__ == '__main__':
    setupDB()
    main()
