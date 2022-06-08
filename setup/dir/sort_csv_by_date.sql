/*
Function exports data ordered by months.
*/

ALTER TABLE points
   ADD COLUMN dateTime timestamp;

UPDATE points
   SET dateTime = TO_TIMESTAMP(points.tmpDateTime, 'YYYY-MM-DD HH24:MI:SS.MS');


Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-03-01' and '2019-04-01' order by datetime)
To '/var/lib/postgresql/export_month_march.csv' With CSV DELIMITER ';';


Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-04-01' and '2019-05-01' order by datetime)
To '/var/lib/postgresql/export_month_april.csv' With CSV DELIMITER ';';


Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-05-01' and '2019-06-01' order by datetime)
To '/var/lib/postgresql/export_month_may.csv' With CSV DELIMITER ';';

Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-06-01' and '2019-07-01' order by datetime)
To '/var/lib/postgresql/export_month_june.csv' With CSV DELIMITER ';';

Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-07-01' and '2019-08-01' order by datetime)
To '/var/lib/postgresql/export_month_july.csv' With CSV DELIMITER ';';

Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-08-01' and '2019-09-01' order by datetime)
To '/var/lib/postgresql/export_month_august.csv' With CSV DELIMITER ';';

Copy (select carid, datetime, tmpLatitude, tmpLongitude
from points where datetime between '2019-09-01' and '2019-09-30' order by datetime)
To '/var/lib/postgresql/export_month_september.csv' With CSV DELIMITER ';';
