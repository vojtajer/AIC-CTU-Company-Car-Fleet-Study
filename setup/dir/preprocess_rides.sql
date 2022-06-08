/*
From latitude and logitude is created point in geogprahy and geometry format.
*/
DELETE FROM points
WHERE points.tmpLatitude = 0 OR points.tmpLongitude = 0;

ALTER TABLE points
   ADD COLUMN dateTime timestamp,
   ADD COLUMN geog geography, /* geog */
   ADD COLUMN geom geometry; /* geom */

UPDATE points
SET dateTime = TO_TIMESTAMP(points.tmpDateTime, 'YYYY-MM-DD HH24:MI:SS.MS'),
    geog = ST_SetSRID(ST_MakePoint(points.tmpLongitude, points.tmpLatitude), 4326)::geography,
    geom = ST_MakePoint(points.tmpLongitude, points.tmpLatitude);

/*DELETE FROM points
WHERE datetime
NOT BETWEEN '2019-05-13'  AND '2019-05-19';*/

ALTER TABLE points
DROP COLUMN tmpDateTime,
DROP COLUMN tmpLongitude,
DROP COLUMN tmpLatitude;

CREATE INDEX points_spatial_index ON points USING GIST (geog, geom); /* geog, geom*/
VACUUM ANALYZE points;
