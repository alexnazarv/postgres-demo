Start prometheus:

    docker run \
      -p 9090:9090 \
      -d \
      --network host \
      -v "$PWD"/prometheus.yml:/etc/prometheus/prometheus.yml \
      --name prometheus \
      prom/prometheus

Start postgres exporter:

    docker run \
      --net=host \
      -d \
      -e DATA_SOURCE_NAME="postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable" \
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