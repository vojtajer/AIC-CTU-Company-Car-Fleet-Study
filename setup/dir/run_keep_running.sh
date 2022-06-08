#!/bin/bash

#stat /var/lib/postgresql/
#stat /var/lib/postgresql/9.6/

# set ownership of db folder, so db runs properly
chown -R ${POSTGRES_USER} /var/lib/postgresql

#stat /var/lib/postgresql/
#stat /var/lib/postgresql/9.6/

# start db server
bash /docker-entrypoint.sh &

echo "going to sleep..."
# wait for db to spin-up
sleep 30
echo "wake up"

# change user so db connection gets authenticated (local auth)
# EVERY CODE WITH DB CONNECTION HAS TO BE RUN LIKE THIS
# and run desired python code for experiments
su -p ${POSTGRES_USER}

tail -f /dev/null
