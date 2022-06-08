FROM kartoza/postgis:9.6-2.4

RUN rm -rf /var/lib/apt/lists/* \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
  "g++" \
  "make" \
  "python-dev" \
  "python-numpy" \
  "python2.7" \
  "python-setuptools" \
  "python-pip" \
  "libspatialindex-dev" \
  "python-tk" \
  "libpq-dev" \
  && rm -rf /var/lib/apt/lists/*

# add pip requirements alone, so caching is used effectively
ADD dir/requirements.txt /home
WORKDIR /home
RUN pip install -r requirements.txt

# copy whole directory structure for experiment
COPY dir/ /home/

# # setup dbs authentication et al.
# RUN export POSTGRES_USER=root
# RUN export POSTGRES_PASS=sumpr0ject
# RUN export POSTGRES_DBNAME=skoda-postgres

# prepare mounting volume for db persistence
# RUN chown -R $POSTGRES_USER /var/lib/postgresql/..
VOLUME /var/lib/postgresql/

RUN chmod +x /home/run.sh

ENTRYPOINT ["/home/run.sh"]
