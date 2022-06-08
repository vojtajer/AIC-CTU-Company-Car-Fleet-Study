/*
Function separates points into trips based on difference between their timestamps.
Special case is when it is first and last timestamp, that is reason of many IFs.
*/

DROP FUNCTION createTrips();

CREATE OR REPLACE FUNCTION createTrips(time_lmt integer, dist_lmt integer)
RETURNS VOID
AS $$
DECLARE
   id integer;

   previous_datetime timestamp;
   is_first boolean;
   to_insert boolean;
   last_user integer;
   previous_point geometry;
   t_curs cursor for
      select * from points order by carid, datetime;
   t_row points%rowtype;
BEGIN
id := 0;
is_first := true;
to_insert := false;
FOR t_row in t_curs LOOP
   IF last_user != t_row.carid THEN
      is_first := true;
      id := id + 1;
   END IF;
   IF is_first = false THEN
      IF (SELECT EXTRACT(EPOCH FROM (t_row.datetime - previous_datetime))) > time_lmt THEN
         id := id + 1;
         to_insert := true;
         INSERT INTO chargeable(TripID, CarID, end_geom, start_geom, end_time, start_time) VALUES (id, t_row.carid, previous_point, t_row.geom, previous_datetime, t_row.datetime);
      END IF;
      INSERT INTO trips_points(TripID, CarID, dateTime, geom) VALUES (id, t_row.carid, t_row.dateTime, t_row.geom);

   ELSE
      INSERT INTO trips_points(TripID, CarID, dateTime, geom) VALUES (id, t_row.carid, t_row.dateTime, t_row.geom);
      is_first := false;
      to_insert := false;
   END IF;
   previous_datetime := t_row.dateTime;
   previous_point := t_row.geom;
   last_user := t_row.carid;
--where current of t_curs;
END LOOP;
DELETE FROM chargeable WHERE NOT ST_DWithin(end_geom::geography, start_geom::geography, dist_lmt);

END;
$$
LANGUAGE plpgsql;
