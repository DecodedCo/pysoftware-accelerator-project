from dataclasses import dataclass

@dataclass 
class PvwattsParameters:
    module_type: int = 0
    array_type: int = 1
    latitude: float = 2
    longitude: float = 3
    system_capacity: float = 4
    tilt: float = 5
    azimuth: float  = 6
    losses: float  = 7

@dataclass
class PvwattsReport:
    energy_per_month : list[float]
    radiation_per_month : list[float]
    annual_radiation: float 
    annual_energy: float 

@dataclass
class EnergyPriceParameters:
    months: list[str] 
    # energy_per_month: list[float]

@dataclass
class EnergyPriceReport:
    months: list[str]               
    profit_per_month: list[float]   

@dataclass 
class SolarPanelEstimationReport:
    pvParams: PvwattsParameters
    pvResult: PvwattsReport
    enParams: EnergyPriceParameters
    enResult: EnergyPriceReport


def run_estimators(enp: EnergyPriceParameters, pvp: PvwattsParameters) -> SolarPanelEstimationReport:
    pvr = pvwatts_predict_energy(pvp)
    enr = mlmodel_predict_energyprice(pvr, enp)

    return SolarPanelEstimationReport(
        pvParams=pvp, 
        pvResult=pvr,
        enParams=enp,
        enResult=enr
    )

def mlmodel_predict_energyprice(pvwatts: PvwattsReport, params: EnergyPriceParameters):
    return EnergyPriceReport(
        months=[f"2023/{m}/01" for m in range(1, 12)],
        profit_per_month=[0.15 * kwh for kwh in pvwatts.energy_per_month]
    )

def pvwatts_predict_energy(params):
    # for param, value in asdict(params).items():
    #     print(f"{param}={value}")
    return PvwattsReport(
        energy_per_month=list(range(12)),
        radiation_per_month=list(range(12, 25)),
        annual_energy=sum(range(12)),
        annual_radiation=sum(range(12, 25))
    )

if __name__ == "__main__":
    print(run_estimators(
        PvwattsParameters(),
        EnergyPriceParameters([f"2024/{m}/01" for m in range(1, 12)]))
    )