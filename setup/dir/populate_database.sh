#!/bin/bash

#stat /var/lib/postgresql/
#stat /var/lib/postgresql/9.6/

# set ownership of db folder, so db runs properly
chown -R ${POSTGRES_USER} /var/lib/postgresql

#stat /var/lib/postgresql/
#stat /var/lib/postgresql/9.6/

# start db server with user that owns data dirs
#su -p $(stat -c '%U' /var/lib/postgresql/) -c
bash /docker-entrypoint.sh &

# wait for db to spin-up
echo "Going to sleep"
sleep 30

# change user so db connection gets authenticated (local auth)
# EVERY CODE WITH DB CONNECTION HAS TO BE RUN LIKE THIS
# and run desired python code for experiments
echo "woke up..."
su -p ${POSTGRES_USER} <<EOF

python replace.py
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS carsharing;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS points;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS trajectories;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS end_points;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS start_points;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS charging_points;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS trips_points;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "DROP TABLE IF EXISTS chargeable;"



#echo "Creating table carsharing..."
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS carsharing (UserID text,Name text,tmpDateFrom text,tmpDateTo text,DepartureParking text,ArrivalParking text);"
echo "Creating tables..."
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS points (CarID integer,tmpDateTime text, tmpLatitude numeric, tmpLongitude numeric);"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS trajectories (TripID integer, CarID integer, geom geometry);"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS trips_points (TripID integer, CarID integer, dateTime timestamp, geom geometry);"

# Start and end points table does not have implemented timestamp columns yet
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS start_points (TripID integer, CarID integer, start_point geometry, start_time timestamp);"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS start_points (TripID integer, CarID integer, geom geometry);"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS end_points (TripID integer, CarID integer, end_point geometry, end_time timestamp);"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS end_points (TripID integer, CarID integer, geom geometry);"

psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS charging_points (tmp1 text, tmp2 text, tmp3 text, PointID integer PRIMARY KEY, NumAC_smart integer, NumAC_DC integer, location text, tmpLongitude numeric, tmpLatitude numeric);"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "CREATE TABLE IF NOT EXISTS chargeable (TripID integer, CarID integer, end_geom geometry, start_geom geometry, end_time timestamp, start_time timestamp);"


#echo "Raw trip data..."
#ls -la ./import_data


echo "Importing raw data into database..."
# IMPORT DATA
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY carsharing FROM '$(pwd)/import_data/ExportRezervaci_Kveten2019.csv' DELIMITER ',' CSV HEADER;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_1.csv' DELIMITER ';' CSV HEADER;"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY charging_points FROM '$(pwd)/import_data/charging_points_2019.csv' DELIMITER ',' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_2.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_3.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_4.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_5.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_6.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_7.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_8.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_9.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_10.csv' DELIMITER ';' CSV HEADER;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "COPY points FROM '$(pwd)/import_data/_Skoda_Export_11.csv' DELIMITER ';' CSV HEADER;"
echo "Imported"


# UNCOMMENT LINE BELOW AND COMMENT EVERYTHING UNDER IT IF YOU WANT TO EXPORT DATA DIVIDED BY MONTH
# psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/sort_csv_by_date.sql


#echo "Preprocessing carsharing table"
#psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/preprocess_carsharing.sql


echo "Preprocessing points table"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/preprocess_rides.sql

echo "Preprocessing charging points table"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/preprocess_char_points.sql

echo "Divide into trips"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/create_trips.sql

# HERE ENTER TIME AND DISTANCE LIMIT FOR TRIP SEPARATION (seconds, meters)
psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT createTrips(300, 5);"

echo "Creating trajectories"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/trajectories.sql
echo "Extracting start and end points"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/start_end.sql #EDIT THIS SCRIPT

echo "Add spatial indexes"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/add_spatial_index.sql

echo "Assign chargers"
psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/nn_charger.sql

# EXPORT OF TRAFFIC DATA FOR PURPOSES OF MY BACHELOR THESIS
#psql -U ${POSTGRES_USER} -d skoda-postgres -f $(pwd)/get_data.sql

# USE FOR EXTRACTION OF DATA TO OVERFLOW BLUE FORMAT
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "Copy (select (tripid+1)*-1, (tripid+1)*-1, st_y(end_geom), st_x(end_geom) from startend) To '/var/lib/postgresql/end.csv' With CSV DELIMITER ',';"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "Copy (select (tripid+1), (tripid+1),  st_y(start_geom), st_x(start_geom) from startend) To '/var/lib/postgresql/start.csv' With CSV DELIMITER ',';"


#echo "Test prints from carsharing:"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT COUNT(*) FROM start_points;"
#psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT * FROM carsharing LIMIT 3;"

echo "test print potential charging trips"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "select carid, charge_pointid, end_time, start_time from chargeable where charge_pointid is not null order by end_time ASC limit 10;"
echo "Test prints from points:"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT COUNT(*) FROM points;"
echo "Descending order"
psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT * FROM points ORDER BY dateTime DESC LIMIT 10;"
echo "Ascending order" */
psql -U ${POSTGRES_USER} -d skoda-postgres -c "SELECT * FROM points ORDER BY dateTime ASC LIMIT 10;"
