/*
Create trajectories of trips from point that were previously marked with trip_id by function create_trips.sql
*/

INSERT INTO trajectories(tripid, carid, geom)
(SELECT tr.tripid, tr.carid, ST_MakeLine(tr.geom ORDER BY tr.datetime)t
	FROM trips_points As tr
	GROUP BY tr.tripid, tr.carid);
