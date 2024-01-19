
from dataclasses import dataclass

@dataclass
class SolarResult:
    resultid: int 
    arraytype: str 
    moduletype: str 
    lat: float 
    lng: float 
    area: float 
    systemcapacity: float 
    tiltangle: float 
    azimuthangle: float 
    systemlosses: float 


