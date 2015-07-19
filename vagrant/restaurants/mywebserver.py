#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Restaurant, MenuItem
import cgi

# TIP for BaseHTTPRequestHandler

# self.rfile: Contains an input stream, positioned at the start of the
# optional input data.
#
# self.wfile: Contains the output stream for writing a response back to the
# client. Proper adherence to the HTTP protocol must be used when writing
# to this stream.


def get_a_database_session(database_name="restaurantmenu.db"):
    """
    Return a new 'session' that you can use to operate on the database.

    Parameters
    ----------
    database_name : str
        The database filename.
    """
    # The create_engine function let's our program know with which database we
    # want to communicate with
    engine = create_engine('sqlite:///restaurantmenu.db')

    # Bind the engine to the base class. This will make the connections between
    # our class definitions and the corresponding tables in our database
    Base.metadata.bind = engine


    # Create a sessionmaker object. This stablishs a link of communication
    # between our code executions and the engine we just created.
    DBSession = sessionmaker(bind=engine)

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # In order to create, read, delete or update information on our database,
    # SQLAlchemy executes database operations via an interface called "a
    # session". A session allows us to write down all the commands we want to
    # execute, but not send them to the database until we call a "commit".

    # Let's create a session so that we can send commands
    session = DBSession()
    return session


def get_the_list_of_restaurants(database_name="restaurantmenu.db"):
    """
    Return a list of tuples with the restaurant ids and names in the
    provided database.

    Parameters
    ----------
    database_name : str
        The database filename.

    Returns
    -------
    restaurantes : list of tuples
        A lista of restaurantes ids and names in the form
        [(id1,name1), (id2,name2), ...]
    """
    session = get_a_database_session(database_name)
    restaurants = session.query(Restaurant).all()
    names = [(r.id, r.name) for r in restaurants]

    return names



# xxxxxxxxxx Handler class xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Will indicate what code to run based on the type of HTTP request
class WebserverHandler(BaseHTTPRequestHandler):
    def answer_get_hello(self):
        """
        Call this method in do_GET if the URL ends with "/hello".
        """
        # If "path" ends with /hello we send a response of 200
        # indicating a success GET request.
        self.send_response(200)
        # Writes a specific HTTP header to the output
        # stream. keyword should specify the header keyword, with
        # value specifying its value.
        self.send_header('Cotent-type', 'text-html')
        # Sends a blank line, indicating the end of the HTTP
        # headers in the response.
        self.end_headers()

        # Response that we will send to the client
        output = ""
        output += "<html><body>Hello"
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"

        # Send a message back to the client
        self.wfile.write(output)

        # Print in the terminal what was sent to the client
        print output

    def answer_get_hola(self):
        """
        Call this method in do_GET if the URL ends with "/hola".
        """
        self.send_response(200)
        self.send_header('Cotent-type', 'text-html')
        self.end_headers()

        # Response that we will send to the client
        output = ""
        output += "<html><body>&#161Hola"
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"

        # Send a message back to the client
        self.wfile.write(output)

        # Print in the terminal what was sent to the client
        print output

    def answer_get_restaurants(self):
        """
        Call this method in do_GET if the URL ends with "/restaurants".
        """
        self.send_response(200)
        self.send_header('Cotent-type', 'text-html')
        self.end_headers()

        # Create the restaurant list of names, including the 'Edit' and
        # 'Delete' links for each restaurant
        RESTAURANT_HTML = ('<div class="restaurant">'
                             '<div class="restaurant-title">'
                             '{0}'
                             '</div>'
                             '<div class="restaurant-buttons">'
                               '<a href="/restaurants/{1}/edit">Edit</a> </br>'
                               '<a href="/restaurants/{1}/delete">Delete</a> </br></br>'
                             '</div>'
                           '</div>')
        restaurant_html_div_list = [RESTAURANT_HTML.format(r[1], r[0]) for r in get_the_list_of_restaurants()]

        # HTML for the link to create a new restaurant
        restaurant_html_creat_new = '<a href="/restaurants/new">Make a new restairant here</a></br></br>'

        output = "<html><body>"
        output += restaurant_html_creat_new
        output += '\n'.join(restaurant_html_div_list)
        output += "</body></html>"

        # Send a message back to the client
        self.wfile.write(output)

        # Print in the terminal what was sent to the client
        print output

    def answer_get_restaurants_new(self):
        """
        Call this method in do_GET if the URL ends with "/restaurants/new".

        This page will have a form to create a new restaurant.
        """
        self.send_response(200)
        self.send_header('Cotent-type', 'text-html')
        self.end_headers()

        FORM_HTML = ('<form '
                     'method="POST" '
                     'enctype="multipart/form-data">'
                       '<h1>Make a New Restaurant</h1>'
                       '<input name="restaurant_name" type="text" placeholder="New Restaurant Name">'
                       '<input type="submit" value="Create">'
                     '</form>')

        output = "<html><body>"
        output += FORM_HTML
        output += "</body></html>"

        # Send a message back to the client
        self.wfile.write(output)

        # Print in the terminal what was sent to the client
        print output

    def answer_get_restaurants_edit(self):
        """
        Call this method in do_GET if the URL ends with "/restaurants/{number}/edit".

        This page will have a form to edit an existing restaurant.
        """
        self.send_response(200)
        self.send_header('Cotent-type', 'text-html')
        self.end_headers()

        # The URL in in the form 'something/id/edit'. Let's get the id part
        restaurant_id = self.path.split('/')[2]

        session = get_a_database_session()

        try:
            # Get the restaurant from the ID
            restaurant = session.query(Restaurant)\
                                .filter_by(id=restaurant_id)\
                                .one()

            FORM_HTML = ('<form '
                         'method="POST" '
                         'enctype="multipart/form-data">'
                           '<h1>{0}</h1>'
                           '<input name="new_name" type="text" placeholder="New Name">'
                           '<input type="submit" value="Rename">'
                         '</form>').format(restaurant.name)

            output = "<html><body>"
            output += FORM_HTML
            output += "</body></html>"

            # Send a message back to the client
            self.wfile.write(output)

        except NoResultFound:
            output = "WARNING: Restaurant with id {0} nor found".format(
                restaurant_id)

        # Print in the terminal what was sent to the client
        print output

    def answer_get_restaurants_delete(self):
        """
        Call this method in do_GET if the URL ends with "/restaurants/{number}/delete".

        This page will have a confirmation page for the deletion.
        """
        self.send_response(200)
        self.send_header('Cotent-type', 'text-html')
        self.end_headers()

        # The URL in in the form 'something/id/edit'. Let's get the id part
        restaurant_id = self.path.split('/')[2]

        session = get_a_database_session()

        try:
            # Get the restaurant from the ID
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

            FORM_HTML = ('<form '
                         'method="POST" '
                         'enctype="multipart/form-data">'
                           '<h1>Are you sure you want to delete {0}?</h1>'
                           '<input type="submit" value="Delete">'
                           '<a href="/restaurants"> Go Back</a>'
                         '</form>').format(restaurant.name)

            output = "<html><body>"
            output += FORM_HTML
            output += "</body></html>"

            # Send a message back to the client
            self.wfile.write(output)

        except:
            output = "WARNING: Restaurant with id {0} nor found".format(
                restaurant_id)

        # Print in the terminal what was sent to the client
        print output

    def do_GET(self):
        """
        Handles all GET requests our server receives.
        """
        # In order to figure it out which resources we are trying to access,
        # we will use a simple pattern maching plan that only looks for the
        # ending of our URL.

        # The BaseHTTPRequestHandler provide us with a variable
        # called "path" that contains the URL sent by the client.
        if self.path.endswith("/hello") or self.path.endswith("/hello/"):
            self.answer_get_hello()
            return  # Exit the if statement

        if self.path.endswith("/hola") or self.path.endswith("/hola/"):
            self.answer_get_hola()

            return  # Exit the if statement

        if self.path.endswith("/restaurants") or self.path.endswith("/restaurants/"):
            self.answer_get_restaurants()

            return  # Exit the if statement

        if self.path.endswith("/restaurants/new") or self.path.endswith("/restaurants/new/"):
            self.answer_get_restaurants_new()

            return  # Exit the if statement
        if self.path.endswith("/edit") or self.path.endswith("/edit/"):
            self.answer_get_restaurants_edit()

            return  # Exit the if statement
        if self.path.endswith("/delete") or self.path.endswith("/delete/"):
            self.answer_get_restaurants_delete()

            return  # Exit the if statement
        else:
            self.send_error(404, "File not found {0}".format(self.path))

    def answer_post_restaurants_new(self):
        """
        Call this method in do_POST if the URL ends with "/restaurants/new".

        This page will handle the creation of a new restaurant submited
        from.
        """
        # Parse an HTTP form header, such as content-type, into a main
        # value and dictionary of parameters
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))

        # Check and see if this is a form data being received
        if ctype == "multipart/form-data":
            # The variable "fields" will collect all the fields in a form
            fields = cgi.parse_multipart(self.rfile, pdict)
            # Get the value of a specifying field or set of fields and
            # store them in an array. The name "restaurant_name" here
            # should be used in the HTTP form
            restaurant_name = fields.get("restaurant_name")[0]

            # xxxxx Create the new restaurant in the database here xxxxxxxx
            # TODO: Should we have to be careful with the form input (it
            # could be SQL injection of script injection)? Or SQLAlchemy
            # will take care of that for us?
            newRestaurant = Restaurant(name=restaurant_name)

            session = get_a_database_session()
            session.add(newRestaurant)
            session.commit()
            # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            # This header will redirect us to the /restaurants page
            self.send_header('Location', '/restaurants')
            self.end_headers()

            return

    def answer_post_restaurants_edit(self):
        """
        Call this method in do_POST if the URL ends with
        "/restaurants/{number}/edit".

        This page will handle the POST action to edit an existing
        restaurant.
        """
        # Parse an HTTP form header, such as content-type, into a main
        # value and dictionary of parameters
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))

        # Check and see if this is a form data being received
        if ctype == "multipart/form-data":
            # The variable "fields" will collect all the fields in a form
            fields = cgi.parse_multipart(self.rfile, pdict)
            # Get the value of a specifying field or set of fields and
            # store them in an array. The name "restaurant_name" here
            # should be used in the HTTP form
            new_name = fields.get("new_name")[0]

            # The URL in in the form 'something/id/edit'. Let's get the id part
            restaurant_id = self.path.split('/')[2]

            session = get_a_database_session()

            try:
                # Get the restaurant from the ID
                restaurant = session.query(Restaurant)\
                                    .filter_by(id=restaurant_id)\
                                    .one()

                # Update the restaurant name in the database
                restaurant.name = new_name
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                # This header will redirect us to the /restaurants page
                self.send_header('Location', '/restaurants')
                self.end_headers()

            except NoResultFound:
                output = "WARNING: Restaurant with id {0} nor found".format(
                    restaurant_id)
                print output

            return

    def answer_post_restaurants_delete(self):
        """
        Call this method in do_POST if the URL ends with
        "/restaurants/{number}/delete".

        This page will handle the POST action to delete an existing
        restaurant.
        """
        # # Parse an HTTP form header, such as content-type, into a main
        # # value and dictionary of parameters
        # ctype, pdict = cgi.parse_header(
        #     self.headers.getheader('content-type'))

        # # Check and see if this is a form data being received
        # if ctype == "multipart/form-data":

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # The URL in in the form 'something/id/delete'. Let's get the id part
        restaurant_id = self.path.split('/')[2]

        session = get_a_database_session()

        # Delete the restaurant with the provided id
        session.query(Restaurant).filter_by(id=restaurant_id).delete()
        session.commit()

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        # This header will redirect us to the /restaurants page
        self.send_header('Location', '/restaurants')
        self.end_headers()

        return

    def do_POST(self, ):
        """Handle post requests
        """
        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        try:
            # Answer the POST to create a new restaurant
            if self.path.endswith("/restaurants/new") or self.path.endswith("/restaurants/new/"):
                self.answer_post_restaurants_new()
                return

            if self.path.endswith("/edit") or self.path.endswith("/edit/"):
                self.answer_post_restaurants_edit()
                return

            if self.path.endswith("/delete") or self.path.endswith("/delete/"):
                self.answer_post_restaurants_delete()
                return

            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()

            # # Parse an HTTP form header, such as content-type, into a main
            # # value and dictionary of parameters
            # ctype, pdict = cgi.parse_header(
            #     self.headers.getheader('content-type'))

            # # Check and see if this is a form data being received
            # if ctype == "multipart/form-data":
            #     # The variable "fields" will collect all the fields in a form
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     # Get the value of a specifying field or set of fields and
            #     # store them in an array. The name "message" here should be
            #     # used in the HTTP form
            #     messagecontent = fields.get("message")

            # # After receiving the POST request, we can send some
            # # information to the client
            # output = ""
            # output += "<html><body>"
            # output += "<h2> Okay, how about this: </h2>"
            # output += "<h1> {0} </h1>".format(messagecontent[0])
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass


# xxxxxxxxxx Main function xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Instantiate our server and specify which port to listen on
def main():
    """Run our server. Exit if ^C is entered.
    """
    try:
        port = 8080
        host = ''  # empty string -> localhost
        server = HTTPServer((host, port), WebserverHandler)
        print "Web server running on port {0}".format(port)
        server.serve_forever()

    except KeyboardInterrupt:  # Thriggered by "Ctrl+c"
        print "^C entered, stopping web server ..."
        server.socket.close()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxx Main xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == '__main__':
    main()
