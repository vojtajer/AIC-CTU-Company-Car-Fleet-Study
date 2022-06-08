/*
Add spatial indexes to improve performance of database.
*/

CREATE INDEX traj_sp_index ON trajectories USING GIST (geom);
VACUUM ANALYZE trajectories;

CREATE INDEX start_sp_index ON start_points USING GIST (geom);
VACUUM ANALYZE start_points;

CREATE INDEX end_sp_index ON end_points USING GIST (geom);
VACUUM ANALYZE end_points;

CREATE INDEX trips_sp_index ON trips_points USING GIST (geom);
VACUUM ANALYZE trips_points;

CREATE INDEX chargeable_sp_index ON chargeable USING GIST (start_geom, end_geom);
VACUUM ANALYZE chargeable;
