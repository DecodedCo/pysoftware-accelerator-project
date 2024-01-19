import os
import sqlite3 
from solardb_resultmodel_ import *

DATABASE_FILE = 'solar.db'


def solardb_create(createsql='sql/create_resultdb_.sql'):
    if os.path.exists(DATABASE_FILE):
        raise Exception('The solar db has been created (delete to recreate)!')

    db = sqlite3.connect(DATABASE_FILE)

    with open(createsql) as sql:
        db.executescript(sql.read())

    db.commit()
    return db 


def solardb_destroy():
    if os.path.exists(DATABASE_FILE):
        return os.remove(DATABASE_FILE)

    return True

def solardb_select_all(db):
    return list(db.execut("SELECT * FROM solar_results").fetchall())



# def solardb_insert(db, r: SolarResult):
#     db.cursor().execute("""
#     INSERT INTO solar_results(
#             arraytype, moduletype, 
#             lat, lng, area, 
#             systemcapacity, 
#             tiltangle, azimuthangle, systemlosses
#     ) 
#     VALUES (
#         :arraytype, :moduletype,
#         :lat, :lng, :area,
#         :systemcapacity,
#         :tiltangle, :azimuthangle, :systemlosses
#     )""", asdict(r))

# solardb_insert(db, SolarResult(
#     moduletype = "A",
#     arraytype = "B",
#     lat = 10,
#     lng = 20,
#     area = 30,
#     systemcapacity = 40,
#     tiltangle = 50,
#     azimuthangle = 60,
#     systemlosses = 70,
# ))






    