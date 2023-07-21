## DB preparing:

Build PostgreSQL image:

    docker build . -t test-postgres

Run locally:  

    $ chmod 777 "$PWD"/logs/

    $ docker run -d -p 5432:5432 --cpus=0.5 -m=2g --network host \
      --name postgres-test --user 0 \
      -v "$PWD"/postgresql.conf:/etc/postgresql/postgresql.conf \
      -v "$PWD"/logs:/etc/postgresql/pg_log \
      postgres-test -c 'config_file=/etc/postgresql/postgresql.conf'