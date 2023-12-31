## DB preparing:

Build PostgreSQL image:

    $ docker build "$PWD"/postgers/Dockerfile -t test-postgres

Run locally:  

    $ mkdir "$PWD"/postgres/logs/ && chmod 777 "$PWD"/postgres/logs/

    $ docker run -d -p 5432:5432 --cpus=0.5 -m=2g --network host \
      --name postgres-test \
      --user 0 \
      -v "$PWD"/postgres/postgresql.conf:/etc/postgresql/postgresql.conf \
      -v "$PWD"/postgres/logs:/etc/postgresql/pg_log \
      postgres-test -c 'config_file=/etc/postgresql/postgresql.conf'

Uploading data:
20 000 000 строк

    $ python3 "$PWD"/inserter/main.py

## Performance testing PostgreSQL indexes

#### Creating results table:

    CREATE TABLE testdb.public.measured_time (
        IndexType    VARCHAR,
        DataType     VARCHAR,
        IndexWeight  FLOAT,
        CreationTime FLOAT,
        "="          FLOAT,
        ">"          FLOAT,
        "like"       FLOAT,
        "in"         FLOAT
    )

#### Tests
    $ export PYTHONPATH=$PYTHONPATH:$PWD/inserter
    $ python "$PWD"/index_performance_test/main.py

#### Result
| IndexType  | DataType  |  IndexSize | CreationDuration |   =   |   >   | like |   in   |
|------------|-----------|------------|------------------|-------|-------|------|--------|
|   brin     | varchar   |	 64 kB	  |      45.01	     | 26.49 |       | 22.7 |  24.8  | 
|   brin	 | integer   |	 64 kB    |      30.9	     | 22.5	 | 19.1	 |	    |  23.5  |
|   brin	 | date	     |   64 kB    |      33.79	     | 25.09 | 16.1	 |	    |  24.5  |
|   hash	 | varchar	 |   841 MB   |      396.39	     |  0.2	 |       | 28.8	|   0.1  |
|   hash	 | integer	 |   535 MB   |      318.2	     |  0.0	 | 28.1	 |      |   0.0  |    
|   hash	 | date	     |   895 MB   |      2518.3	     |  4.0	 | 19.4	 |	    |   1.9  |
|   btree	 | varchar	 |   139 MB   |      489.71	     |  0.0	 |       | 24.3 |   0.0  |
|   btree	 | integer	 |   177 MB   |      149.9	     |  0.0	 | 18.9	 |      |   0.09 |   
|   btree	 | date	     |   132 MB   |      176.11	     |  0.1	 |  8.8	 |      |   0.3  |

### Cleaning out container and image:

    docker stop test-postgres && docker rmi test-postgres

## Monitoring

Start prometheus:

    docker run \
      -p 9090:9090 \
      -d \
      --network host \
      -v "$PWD"/postgres/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
      --name prometheus \
      prom/prometheus

Start postgres exporter:

    docker run \
      --net=host \
      -d \
      -e DATA_SOURCE_NAME="postgresql://postgres:postgres@127.0.0.1:5432/testdb?sslmode=disable" \
      --name postgres-exporter \
      quay.io/prometheuscommunity/postgres-exporter


Start cadvisor:

    docker run \
      --volume=/:/rootfs:ro \
      --volume=/var/run:/var/run:ro \
      --volume=/sys:/sys:ro \
      --volume=/var/lib/docker/:/var/lib/docker:ro \
      --volume=/dev/disk/:/dev/disk:ro \
      --publish=8080:8080 \
      --detach=true \
      --name=cadvisor \
      --privileged \
      --device=/dev/kmsg \
      --network host \
      --name cadvisor \
      gcr.io/cadvisor/cadvisor

Start grafana container:

    docker run -d -p 3000:3000 --network host --name=grafana \
      --user "$(id -u)" \
      -e "GF_INSTALL_PLUGINS=grafana-clock-panel" \
      grafana/grafana-enterprise

Optional add to grafana:
    
    sudo chmod 777 
    
    --volume "$PWD/data:/var/lib/grafana" \

Start node exporter:

    sudo groupadd -f node_exporter && \
    useradd -g $(getent group node_exporter | cut -d: -f3) -M -s /bin/false node_exporter && \
    mkdir /etc/node_exporter && \
    chown node_exporter:node_exporter /etc/node_exporter && \
    wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz && \
    tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz && \
    cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/bin/
    chown node_exporter:node_exporter /usr/bin/node_exporter && \
    chmod 664 /usr/lib/systemd/system/node_exporter.service && \
    systemctl daemon-reload && \
    systemctl start node_exporter && \
    rm -rf node_exporter-1.6.1.linux-amd64.tar.gz node_exporter-1.6.1.linux-amd64

Clean up node_exporter:

    sudo systemctl stop node_exporter && \
    systemctl disable node_exporter && \
    rm /usr/bin/node_exporter -f && \
    rm /usr/lib/systemd/system/node_exporter.service -f && \
    systemctl daemon-reload && \
    systemctl reset-failed
