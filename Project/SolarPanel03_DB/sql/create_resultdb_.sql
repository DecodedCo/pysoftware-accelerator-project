CREATE TABLE solar_results (
    resultid INTEGER PRIMARY KEY AUTOINCREMENT,
    arraytype TEXT,
    moduletype TEXT,
    lat FLOAT,
    lng FLOAT,
    area FLOAT,
    systemcapacity FLOAT,
    tiltangle FLOAT,
    azimuthangle FLOAT,
    systemlosses FLOAT
);

INSERT INTO solar_results VALUES
    (1, "A11", "M11", 55, 0, 1000, 51, 10.1, 10, 11),
    (2, "A12", "M12", 55, 0, 2000, 52, 10.2, 20, 12),
    (3, "A13", "M13", 55, 0, 3000, 53, 10.3, 30, 13),
    (4, "A14", "M14", 55, 0, 4000, 54, 10.4, 40, 14),
    (5, "A15", "M15", 55, 0, 5000, 55, 10.5, 50, 15),
    (6, "A16", "M16", 55, 0, 6000, 56, 10.6, 60, 16);