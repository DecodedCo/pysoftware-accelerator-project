from time import sleep

# our two end points, faking some calc time
def run_estimators_api():
    sleep(1)
    with open('request-data-fake.json', 'rb') as f:
        return f.read()

def run_submit_api():
    sleep(1)
    with open('submit-data-fake.json', 'rb') as f:
        return f.read()





# a quick http server to make them work
from http.server import HTTPServer, BaseHTTPRequestHandler
def http_get_request(server):
    server.send_response(200)
    server.send_header('Access-Control-Allow-Origin', '*')
    server.send_header('Content-type', 'application/json')
    server.end_headers()
    server.wfile.write(run_submit_api() if 'submit' in server.path else run_estimators_api())

print("Starting http://127.0.0.1:8000 ...")
svr = HTTPServer(('127.0.0.1', 8000), type('Fake', (BaseHTTPRequestHandler,), {"do_GET": http_get_request}))
svr.serve_forever()
        


