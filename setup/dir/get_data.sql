/*
Used for export of potential charging windows with duration of charging and charge point id.
*/

Copy (select carid, (charge_pointid - 1), end_time, start_time from chargeable where charge_pointid is not null order by end_time ASC)
To '/var/lib/postgresql/traffic_export.csv' With CSV DELIMITER ',';
