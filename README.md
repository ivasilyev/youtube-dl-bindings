# youtube-dl-bindings

## Setup

```shell script
cd /opt
sudo git clone "https://github.com/ivasilyev/youtube-dl-bindings"
sudo chown -R "$(whoami)" "/opt/youtube-dl-bindings"
sudo chmod -R 755 "/opt/youtube-dl-bindings"
cd "/opt/youtube-dl-bindings"
python3 -m venv venv

chmod a+x venv/bin/activate
source venv/bin/activate

pip install -r requirements.txt

python3 updater.py
```

## Run web server

```shell script
python3 rest.py

# or bash run_web_server.sh
```

## Run standalone single video downloader

```shell script
python3 single_downloader.py \
    --url "https://www.youtube.com/watch?v=zqTwOoElxBA" \
    --dir "/tmp"
```

## Run standalone playlist video downloader

```shell script
python3 playlist_downloader.py \
    --url "https://www.youtube.com/playlist?list=PLmBK9jc1368IfTwX0Vf3G_6GROJYc2XrH" \
    --dir "/tmp"
```

## Create system service

```shell script
export TOOL_NAME=youtube-dl-bindings
export TOOL_SERVICE="/etc/systemd/system/${TOOL_NAME}.service"

echo Create ${TOOL_NAME} system service
cat <<EOF | sudo tee "${TOOL_SERVICE}"
[Unit]
Description=${TOOL_NAME}
Documentation=https://google.com
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=$(whoami)
ExecReload=/usr/bin/env kill -s SIGTERM \$MAINPID
ExecStart=/usr/bin/env bash /opt/${TOOL_NAME}/run_web_server.sh
SyslogIdentifier=${TOOL_NAME}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF


echo Activate ${TOOL_NAME} service
sudo systemctl daemon-reload
sudo systemctl enable "${TOOL_NAME}.service"
sudo systemctl restart "${TOOL_NAME}.service"
sleep 3
sudo systemctl status "${TOOL_NAME}.service"
```