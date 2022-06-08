/*
Creates table with start point and endpoint of every trajectory.
*/
INSERT INTO start_points(tripid, carid, geom)
(SELECT traj.tripid, traj.carid, ST_StartPoint(traj.geom)
	FROM trajectories As traj
	GROUP BY traj.tripid, traj.carid, traj.geom);



INSERT INTO end_points(tripid, carid, geom)
(SELECT traj.tripid, traj.carid, ST_EndPoint(traj.geom)
	FROM trajectories As traj
	GROUP BY traj.tripid, traj.carid, traj.geom);
