# Minecraft Prometheus Exporter

Prometheus exporter for Minecraft Java Edition singleplayer statistics. This exporter periodically scrapes [game statistics](https://minecraft.fandom.com/wiki/Statistics) and exports metrics via HTTP for Prometheus consumption. 

## Installation

Since the exporter is a simple python script, the whole setup is to create a unit file for the systemd service. 

1. Clone this repository 

```shell
git clone git@github.com:BogdanPetrov/minecraft_exporter.git
```

2. Perform a test run

```shell
python3 minecraft_exporter/minecraft_exporter.py "MINECRAFT_HOME" SCRAPE_INTERVAL PORT
```

Here `MINECRAFT_HOME` is the path to the Minecraft's root directory, `SCRAPE_INTERVAL` defines the refresh rate in seconds, `PORT` is the HTTP port on which the metrics will be available.

For example, if you run the command with parameter values as below

```shell
python3 minecraft_exporter/minecraft_exporter.py "/home/username/.minecraft" 10 9817
```

then Minecraft metrics will be available on [http://localhost:9817/](http://localhost:9817/) and they will be updated approximately every 10 seconds. 

3. Create systemd service

If the test run was successful and you saw your metrics, then create a unit file with the command (note that you need to replace the values `USERNAME, MINECRAFT_HOME, SCRAPE_INTERVAL, PORT` before executing)

```shell
sudo tee /etc/systemd/system/minecraft_exporter.service<<EOF
[Unit]
Description=Minecraft Prometheus Exporter
 
[Service]
Type=simple
User=USERNAME
Group=USERNAME
WorkingDirectory=/home/USERNAME/
ExecStart=python3 minecraft_exporter/minecraft_exporter.py "MINECRAFT_HOME" SCRAPE_INTERVAL PORT
Restart=always
RestartSec=60
 
[Install]
WantedBy=multi-user.target
EOF
```

Next run the commands

```shell
sudo systemctl daemon-reload
sudo systemctl start minecraft_exporter
sudo systemctl enable minecraft_exporter
``` 

and now you should see your metrics on [http://localhost:PORT/](http://localhost:PORT/)

## Prometheus configuration

You should update the [Prometheus configuration file](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) to start collecting metrics. Just add 

```yaml
- job_name: minecraft
  scrape_interval: 30s
  static_configs:
  - targets: ['localhost:PORT']
```

to `/etc/prometheus/prometheus.yml` (specify the same port as in the unit file) and reload configuration.
