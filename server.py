# parse incoming HTTP request; esp, handle GET with do_GET(but we overrider it)
from http.server import BaseHTTPRequestHandler, HTTPServer


# inherite from BaseHTTPRequestHandler
# handle HTTP requests by returning a fixed page
class RequestHandler(BaseHTTPRequestHandler):

    Page = '''\
<html>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
'''
    # override do_GET function with our own personality;
    # seperate create_page and send_page from do_GET;
    def do_GET(self):
        page = self.create_page();
        self.send_page(page);

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path,
        }
        page = self.Page.format(**values)
        return page

    def send_page(self, page):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(page) ) )
        self.end_headers() # insert the blank line separating headers from the page;
        self.wfile.write(bytes(page, 'utf-8'))

if __name__ == '__main__':
    # the empty string means "run on the current machine"
    serverAddress = ('', 8080) # a tuple;
    # create an instance of HTTPServer with our own handler class and serverAddress;
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
