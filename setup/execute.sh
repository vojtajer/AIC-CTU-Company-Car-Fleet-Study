#!/usr/bin/env bash

./build.sh

ARG=$1
echo ${ARG}


if [[ ${ARG} == "populate" ]]; then
    echo "Populate option selected"
    docker run --rm \
           -i \
           -p 35432:5432 \
           -e ALLOW_IP_RANGE='0.0.0.0/0' \
           -e POSTGRES_USER='root' \
           -e POSTGRES_PASS=sumpr0ject \
           -e POSTGRES_DBNAME=skoda-postgres \
           --volume "$PWD/db_persistence":/var/lib/postgresql \
           --name proj-skoda \
           --entrypoint "/home/populate_database.sh" \
           proj-skoda
elif [[ ${ARG} == "alive" ]]; then
    echo "Alive option selected"
    docker run --rm \
           -i \
           -p 35432:5432 \
           -e ALLOW_IP_RANGE='0.0.0.0/0' \
           -e POSTGRES_USER='root' \
           -e POSTGRES_PASS=sumpr0ject \
           -e POSTGRES_DBNAME=skoda-postgres \
           --volume "$PWD/db_persistence":/var/lib/postgresql \
           --name proj-skoda \
           --entrypoint "/home/run_keep_running.sh" \
           proj-skoda
else
   echo "Default"
   docker run --rm \
   -e POSTGRES_USER='root' \
   -e POSTGRES_PASS=sumpr0ject \
   -e POSTGRES_DBNAME=skoda--postgres \
   --volume "$PWD/db_persistence":/var/lib/postgresql \
   --name proj-skoda \
   proj-skoda
fi
