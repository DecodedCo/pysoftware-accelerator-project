"""

*  describe a series of steps for implementing the actual pysam model in this program

* the above is to create a model, i just want to use the std nrel pysam model

* given all the steps above write two pythons: setup_pysam() which sets up pysam for use; and predict_pysam() which takes in the relevant http form data and produces a prediction 

* rather than using the functions directly, integrate them into the webserver code below, 


* revise the above, rather than using constant/fake input data, provide a POST endpoint where a form could be submitted


*** THE BELOW DOESNT WORK BECAUSE PySAM is the wrong python module (it's another library for biological data), so manual iteration is required to get the libraries correct. ***

"""
# pip install PySAM


import PySAM.Pvwattsv7 as PVWatts

def setup_pysam():
    # Create a PVWatts model
    pvwatts = PVWatts.default("PVWattsSingleOwner")
    return pvwatts


def predict_pysam(latitude, longitude, system_capacity, module_type, losses):
    # Initialize the PVWatts model
    pvwatts = setup_pysam()

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
        annual_energy = pvwatts.Outputs.ac_annual  # Annual AC energy production (kWh)
        monthly_energy = pvwatts.Outputs.ac_monthly  # Monthly AC energy production (kWh)
        capacity_factor = pvwatts.Outputs.capacity_factor  # Capacity factor (%)

        # Create a prediction response
        prediction = {
            "annual_energy": annual_energy,
            "monthly_energy": monthly_energy,
            "capacity_factor": capacity_factor
        }

        return prediction

    except Exception as e:
        # Handle any exceptions that may occur during model execution
        error_message = str(e)
        return {"error": error_message}

