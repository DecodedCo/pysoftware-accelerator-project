from solar_lib import estimators as est 

def solarapi_est_response(r: est.SolarPanelEstimationReport):
    return {
        "error": False,
        "data": [
            dict(month=m, radiation=r, energy=e, profit=p) 
            for (m, r, e, p) in zip(r.enParams.months,
                r.pvResult.energy_per_month, 
                r.pvResult.radiation_per_month, 
                r.enResult.profit_per_month)
        ],

        "summary": {
            "estAnnualRadiation": r.pvResult.annual_radiation,
            "estEnergyPrices": r.enResult.profit_per_month,
            "estAnnualEnergy": r.pvResult.annual_energy,
            "estFinancialSavings": sum(r.enResult.profit_per_month),
            "downloadLink": "/download/someid"
        }
    }


