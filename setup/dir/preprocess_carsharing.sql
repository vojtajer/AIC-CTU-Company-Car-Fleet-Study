/*
This code is not part of GPS data project.
*/

ALTER TABLE carsharing
   ADD COLUMN DateFrom timestamp,
   ADD COLUMN DateTo timestamp;

UPDATE carsharing
SET DateFrom = TO_TIMESTAMP(carsharing.tmpdatefrom, 'YYYY-MM-DD HH24:MI:SS.MS'),
    DateTo = TO_TIMESTAMP(carsharing.tmpdateto, 'YYYY-MM-DD HH24:MI:SS.MS');

ALTER TABLE carsharing
DROP COLUMN tmpDateTo,
DROP COLUMN tmpDateFrom;
