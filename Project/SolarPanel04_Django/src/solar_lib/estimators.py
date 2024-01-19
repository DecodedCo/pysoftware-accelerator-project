from .pysam_simulation  import ssc, SSC_FILES_ROOT


from dataclasses import dataclass

@dataclass
class PvwattsParameters:
    _grid_curtailment:                str   = f"{SSC_FILES_ROOT}/grid_curtailment.csv".encode()
    _solar_resource_file:             str   = f"{SSC_FILES_ROOT}/52_0_msg-iodc_60_2019.csv".encode()
    _latitude:                        float = 0
    _longitude:                       float = 0
    
    adjust :                          float = 0
    array_type :                      float = 1 
    module_type :                     float = 0 
    tilt :                            float = 20 
    azimuth :                         float = 180 
    losses :                          float = 14 
    use_wf_albedo :                   float = 1 
    dc_ac_ratio :                     float = 1.15 
    bifaciality :                     float = 0 
    gcr :                             float = 0.3
    en_snowloss :                     float = 0 
    inv_eff :                         float = 96 
    batt_simple_enable :              float = 0 
    enable_interconnection_limit :    float = 0 
    system_capacity :                 float = 1000 
    grid_interconnection_limit_kwac : float = 100000 
    albedo  :                         tuple[float] = (0.2,) * 12
    soiling :                         tuple[float] = (0.0,) * 12



@dataclass
class PvwattsReport:
    energy_per_month : list[float]
    radiation_per_month : list[float]
    annual_radiation: float 
    annual_energy: float 
    
    @staticmethod
    def monthly_averages(hourly):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_averages = []
        start_index = 0

        for days in days_in_month:
            end_index = start_index + days * 24
            month_data = hourly[start_index:end_index]
            month_averages.append(round(sum(month_data) / len(month_data), 2))
            start_index = end_index

        return month_averages

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


def run_estimators(pvp: PvwattsParameters, enp: EnergyPriceParameters,) -> SolarPanelEstimationReport:
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

def pvwatts_predict_energy(params: PvwattsParameters) -> PvwattsReport:
    modpv = ssc.module_create(b'pvwattsv8')    
    modgd = ssc.module_create(b'grid')    
    ssc.module_exec_set_print(0)

    data = _pvwatts_assign(ssc.data_create(), params)
    
    if (ssc.module_exec(modpv, data) == 0) or (ssc.module_exec(modgd, data) == 0):
        raise Exception('pvwattsv8 simulation error: ' + ssc.module_log(modpv, 0).decode())

    ssc.module_free(modpv)
    ssc.module_free(modgd)

    #todo: should this be `gen` ?
    energy_per_hour    = ssc.data_get_array(data, b'ac') 
    radiation_per_hour = ssc.data_get_array(data, b'poa')
    
    return PvwattsReport(
        energy_per_month=PvwattsReport.monthly_averages(energy_per_hour),
        radiation_per_month=PvwattsReport.monthly_averages(radiation_per_hour),
        annual_energy=sum(energy_per_hour),
        annual_radiation=sum(radiation_per_hour)
    )

    #todo: add back in
    # ssc.data_free(data)



def _pvwatts_assign(data, params):
    # this should be done in a simple loop, 
	# but for unknown reasons pvwatts doesnt like it

    ssc.data_set_array_from_csv(data, b'grid_curtailment', params._grid_curtailment)
    ssc.data_set_string(data, b'solar_resource_file', params._solar_resource_file)
    ssc.data_set_array( data, b'albedo',  params.albedo)
    ssc.data_set_array( data, b'soiling',  params.soiling)
    ssc.data_set_number( data, b'use_wf_albedo',  params.use_wf_albedo )
    ssc.data_set_number( data, b'system_capacity',  params.system_capacity )
    ssc.data_set_number( data, b'module_type',  params.module_type )
    ssc.data_set_number( data, b'losses',  params.losses )
    ssc.data_set_number( data, b'dc_ac_ratio',  params.dc_ac_ratio )
    ssc.data_set_number( data, b'bifaciality',  params.bifaciality )
    ssc.data_set_number( data, b'array_type',  params.array_type )
    ssc.data_set_number( data, b'tilt',  params.tilt )
    ssc.data_set_number( data, b'azimuth',  params.azimuth )
    ssc.data_set_number( data, b'gcr',  params.gcr )
    ssc.data_set_number( data, b'en_snowloss',  params.en_snowloss )
    ssc.data_set_number( data, b'inv_eff',  params.inv_eff )
    ssc.data_set_number( data, b'batt_simple_enable',  params.batt_simple_enable )
    ssc.data_set_number( data, b'adjust:constant',  params.adjust)
    ssc.data_set_number( data, b'enable_interconnection_limit',  params.enable_interconnection_limit )
    ssc.data_set_number( data, b'grid_interconnection_limit_kwac',  params.grid_interconnection_limit_kwac )
    return data

    
if __name__ == "__main__":
	print(run_estimators(
        PvwattsParameters(),
		EnergyPriceParameters([f"2024/{m}/01" for m in range(1, 12)]))
	)
