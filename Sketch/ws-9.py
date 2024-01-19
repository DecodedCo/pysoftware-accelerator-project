import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import PySAM.Pvwattsv7 as PVWatts

# Define a function to predict PVWatts response based on input parameters using PySAM
def predict_pysam(latitude, longitude, system_capacity, module_type, losses):
    pvwatts = PVWatts.default("PVWattsSingleOwner")
    
    # Set location parameters (latitude and longitude)
    pvwatts.SolarResource.solar_resource_data = [(0, latitude, longitude, 0)]

    # Set system size (in kW)
    pvwatts.SystemDesign.system_capacity = system_capacity

    # Set module type (0 for standard)
    pvwatts.SystemDesign.module_type = module_type

    # Set system losses (in percent)
    pvwatts.SystemDesign.losses = losses

    try:
        # Run the PVWatts model
        pvwatts.execute()

        # Retrieve results
        ac_monthly = pvwatts.Outputs.ac_monthly  # Monthly AC energy production (kWh)
        dc_monthly = pvwatts.Outputs.dc_monthly  # Monthly DC energy production (kWh)
        ac_annual = pvwatts.Outputs.ac_annual  # Annual AC energy production (kWh)
        solrad_annual = pvwatts.Outputs.solrad_annual  # Annual solar radiation (kWh/m^2/day)
        capacity_factor = pvwatts.Outputs.capacity_factor  # Capacity factor (%)
        annual_degradation = pvwatts.Outputs.annual_degradation  # Annual degradation (%)

        response_data = {
            "station_info": {
                "city": "Sample City",
                "state": "CA",
                "latitude": latitude,
                "longitude": longitude
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

    except Exception as e:
        # Handle any exceptions that may occur during model execution
        error_message = str(e)
        return {"error": error_message}

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/request-data'):
            # Parse query parameters
            query_params = parse_qs(urlparse(self.path).query)
            
            # Extract parameters or use default values
            latitude = float(query_params.get('latitude', [34.0522])[0])
            longitude = float(query_params.get('longitude', [-118.2437])[0])
            system_capacity = float(query_params.get('system_capacity', [5])[0])
            module_type = int(query_params.get('module_type', [0])[0])
            losses = float(query_params.get('losses', [14.08])[0])

            response_data = predict_pysam(latitude, longitude, system_capacity, module_type, losses)

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
