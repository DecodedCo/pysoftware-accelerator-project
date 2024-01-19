"""

* below is a webserver for serving a fake pvwatts api response which reports solar panel modelling data based on http parameters. write a function which accepts relevant parameters and returns a realistic response based on some basic formula 

{{python code}}

"""

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

# Define a function to generate a PVWatts response based on input parameters
def generatePVWattsResponse(system_capacity, module_type, losses):
    # Calculate AC and DC monthly and annual energy production based on basic formulas
    ac_monthly = [system_capacity * 1000 * (1 - losses / 100) * 30 * (1.02 ** i) for i in range(12)]
    dc_monthly = [ac / 0.95 for ac in ac_monthly]  # Assuming 95% inverter efficiency
    ac_annual = sum(ac_monthly)
    solrad_annual = 5.0  # A constant value for solar radiation
    capacity_factor = (ac_annual / (system_capacity * 1000)) / 8760 * 100  # Capacity factor
    annual_degradation = 0.5  # A constant value for annual degradation

    response_data = {
        "station_info": {
            "city": "Sample City",
            "state": "CA",
            "latitude": 34.0522,
            "longitude": -118.2437
        },
        "inputs": {
            "system_capacity": system_capacity,
            "module_type": module_type,
            "losses": losses
        },
        "errors": [],
        "warnings": [],
        "outputs": {
            "ac_monthly": ac_monthly,
            "dc_monthly": dc_monthly,
            "ac_annual": ac_annual,
            "solrad_annual": solrad_annual,
            "capacity_factor": capacity_factor,
            "annual_degradation": annual_degradation
        }
    }

    return response_data

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/request-data'):
            # Parse query parameters
            query_params = parse_qs(urlparse(self.path).query)
            
            # Extract parameters or use default values
            system_capacity = float(query_params.get('system_capacity', [5])[0])
            module_type = int(query_params.get('module_type', [0])[0])
            losses = float(query_params.get('losses', [14.08])[0])

            response_data = generatePVWattsResponse(system_capacity, module_type, losses)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept')
            
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            super().do_GET()

# Create an HTTP server
with socketserver.TCPServer(("", 5321), CustomHandler) as httpd:
    print("Server started at http://localhost:5321")
    httpd.serve_forever()
