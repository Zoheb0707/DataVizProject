The original file taken from an external source is `earthquake_risk_lat_lon.csv`. 
We used the `earthquake_lat_lon_to_zip.sql` file to transform the latitude and longitude of the
data to zipcodes.

We used Postgis to map latitude and longitude to the closest centroid of a zipcode.