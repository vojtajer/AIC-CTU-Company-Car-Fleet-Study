/*
Function count how many trips ended within 200 metres from charging station.
*/

ALTER TABLE chargeable
ADD COLUMN charge_pointid integer;

UPDATE chargeable
    SET charge_pointid = (
        SELECT n.pointid FROM charging_points AS n where n.geom::geography <-> end_geom::geography < 200
        ORDER BY n.geom <-> end_geom limit 1);
