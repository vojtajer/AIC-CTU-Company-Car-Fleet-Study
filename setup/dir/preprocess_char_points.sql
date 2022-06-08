/*
From latitude and longitude of charigng points are created coordinates.
*/
ALTER TABLE charging_points
   ADD COLUMN geog geography, /* geog */
   ADD COLUMN geom geometry;  /* geom */

UPDATE charging_points
SET geog = ST_SetSRID(ST_MakePoint(charging_points.tmpLongitude, charging_points.tmpLatitude), 4326)::geography,
    geom = ST_MakePoint(charging_points.tmpLongitude, charging_points.tmpLatitude);

ALTER TABLE charging_points
DROP COLUMN tmp1,
DROP COLUMN tmp2,
DROP COLUMN tmp3,
DROP COLUMN tmpLongitude,
DROP COLUMN tmpLatitude;

CREATE INDEX ch_pts_sp_index ON charging_points USING GIST (geog, geom); /* geog, geom */
VACUUM ANALYZE charging_points;
