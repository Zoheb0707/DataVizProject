CREATE TABLE zip_codes (ZIP char(5), LATITUDE double precision, LONGITUDE double precision);

-- Update absolute path before running sql script
COPY zip_codes FROM '/Users/li/Documents/CS6242/zipcode_lat_lon.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- prefix 0s are lost in copy, so reappend 
UPDATE zip_codes SET ZIP = '0' || ZIP WHERE LENGTH(ZIP) = 4;
UPDATE zip_codes SET ZIP = '00' || ZIP WHERE LENGTH(ZIP) = 3;

CREATE TABLE earthquake_risk_lat_lon (
    ID SERIAL PRIMARY KEY,
    LONGITUDE real,
    LATITUDE real,
    MMI_50 real,
    MMI_10 real,
    MMI_2 real
);

-- Update absolute path before running sql script
COPY earthquake_risk_lat_lon(LONGITUDE, LATITUDE, MMI_50, MMI_10, MMI_2) FROM '/Users/li/Documents/CS6242/earthquake_risk_lat_lon_us.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

CREATE EXTENSION postgis;

CREATE TABLE geo_zipcode (geog geography, ZIP char(5));

CREATE INDEX ON geo_zipcode USING gist(geog);

INSERT INTO geo_zipcode
SELECT ST_MakePoint(LATITUDE, LONGITUDE), ZIP FROM zip_codes;


CREATE TABLE earthquake_risk_geo (
    ID INTEGER PRIMARY KEY,
    geog geography,
    MMI_50 real,
    MMI_10 real,
    MMI_2 real
);

CREATE INDEX ON earthquake_risk_geo USING gist(geog);

INSERT INTO earthquake_risk_geo
SELECT ID, ST_MakePoint(LATITUDE, LONGITUDE), MMI_50, MMI_10, MMI_2 FROM earthquake_risk_lat_lon;


-- looks up zip in geo_zipcode table and then groups by zip and get average risk values
COPY (
    SELECT ZIP,
    AVG(MMI_50) AS MMI_50,
    AVG(MMI_10) AS MMI_10,
    AVG(MMI_2) AS MMI_2 FROM (SELECT (SELECT ZIP FROM geo_zipcode ORDER BY geo_zipcode.geog <-> ST_MakePoint(LATITUDE,LONGITUDE)::geography limit 1) AS ZIP, MMI_50, MMI_10, MMI_2 FROM earthquake_risk_lat_lon) AS avg_zip GROUP BY ZIP) TO '/Users/li/Documents/CS6242/earthquake_risk_zipcode.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');


-- Update absolute path before running sql script
COPY
(SELECT ZIP, MMI_50, MMI_10, MMI_2
FROM (
         (SELECT (
                     SELECT id
                     FROM earthquake_risk_geo
                     ORDER BY earthquake_risk_geo.geog <-> ST_MakePoint(zip_codes.LATITUDE, zip_codes.LONGITUDE)::geography limit 1
         ) as id,
              ZIP
              FROM zip_codes
         ) as zipcodes_with_id
         LEFT JOIN earthquake_risk_geo
                   ON zipcodes_with_id.id = earthquake_risk_geo.id))
TO '/Users/li/Documents/CS6242/earthquake_risk_zipcode.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');
