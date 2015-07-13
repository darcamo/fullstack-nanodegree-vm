#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# TIP for BaseHTTPRequestHandler

# self.rfile: Contains an input stream, positioned at the start of the
# optional input data.
#
# self.wfile: Contains the output stream for writing a response back to the
# client. Proper adherence to the HTTP protocol must be used when writing
# to this stream.




# xxxxxxxxxx Handler class xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Will indicate what code to run based on the type of HTTP request
class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self, ):
        """
        Handles all GET requests our server receives.
        """
        # In order to figure it out which resources we are trying to access,
        # we will use a simple pattern maching plan that only looks for the
        # ending of our URL.

        # The BaseHTTPRequestHandler provide us with a variable
        # called "path" that contains the URL sent by the client.
        if self.path.endswith("/hello"):
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

            return  # Exit the if statement

        if self.path.endswith("/hola"):
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

            return  # Exit the if statement

        else:
            self.send_error(404, "File not found {0}".format(self.path))

    def do_POST(self, ):
        """Handle post requests
        """
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Parse an HTTP form header, such as content-type, into a main
            # value and dictionary of parameters
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))

            # Check and see if this is a form data being received
            if ctype == "multipart/form-data":
                # The variable "fields" will collect all the fields in a form
                fields = cgi.parse_multipart(self.rfile, pdict)
                # Get the value of a specifying field or set of fields and
                # store them in an array. The name "message" here should be
                # used in the HTTP form
                messagecontent = fields.get("message")

            # After receiving the POST request, we can send some
            # information to the client
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> {0} </h1>".format(messagecontent[0])
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
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
