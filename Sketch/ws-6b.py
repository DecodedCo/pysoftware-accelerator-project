"""
PROMPT:

* write a quick webserver in python, which outputs the json code above as a http response from a get url, the url should be http://localhost/api/request-data

* rather than use flask, just use the inbuilt python http.server module

* revise teh above to send a CORS header to allow CORS reuqests

"""

import http.server
import socketserver
import json

# Define the JSON data you want to return
fakePVWattsResponse = {
    "station_info": {
        "city": "Sample City",
        "state": "CA",
        "latitude": 34.0522,
        "longitude": -118.2437
    },
    "inputs": {
        "system_capacity": 5,  # kW
        "module_type": 0,
        "losses": 14.08  # %
    },
    "errors": [],
    "warnings": [],
    "outputs": {
        "ac_monthly": [
            600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150  # Monthly AC energy production (kWh)
        ],
        "dc_monthly": [
            625, 675, 725, 775, 825, 875, 925, 975, 1025, 1075, 1125, 1175  # Monthly DC energy production (kWh)
        ],
        "ac_annual": 9000,  # Annual AC energy production (kWh)
        "solrad_annual": 5.0,  # Annual solar radiation (kWh/m^2/day)
        "capacity_factor": 18.5,  # Capacity factor (%)
        "annual_degradation": 0.5  # Annual degradation (%)
    }
}

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/request-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept')
            
            self.end_headers()
            self.wfile.write(json.dumps(fakePVWattsResponse).encode())
        else:
            super().do_GET()

# Create an HTTP server
with socketserver.TCPServer(("", 5321), CustomHandler) as httpd:
    print("Server started at http://localhost:5321")
    httpd.serve_forever()
