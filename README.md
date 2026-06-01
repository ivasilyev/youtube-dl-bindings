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

## Run single video downloader

* Standalone

```shell script
python3 single_downloader.py \
    --url "https://www.youtube.com/watch?v=zqTwOoElxBA" \
    --dir "/tmp"
```

* Web-based

```shell script
curl -X 'POST' \
  'http://127.0.0.1:8090/api/download/single-download' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://www.youtube.com/watch?v=zqTwOoElxBA",
  "directory": "/tmp"
}'
```

## Run playlist video downloader

* Standalone

```shell script
python3 playlist_downloader.py \
    --url "https://www.youtube.com/playlist?list=PLmBK9jc1368IfTwX0Vf3G_6GROJYc2XrH" \
    --dir "/tmp" \
    --prefix 'https://www.youtube.com/watch?v='
``` 

* Web-based

```shell script
curl -X 'POST' \
    'http://127.0.0.1:8090/api/download/playlist-download' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "url": "https://www.youtube.com/playlist?list=PLmBK9jc1368IfTwX0Vf3G_6GROJYc2XrH",
        "directory": "/tmp",
        "prefix": "https://www.youtube.com/watch?v="
    }'
```

### Advanced scripting example

```shell script
#!/usr/bin/env bash

yt_dl() {
    echo "Download: ${1} ${2}"
    curl -X 'POST' \
    'http://127.0.0.1:8090/api/download/playlist-download' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d @- <<EOF
{
    "url": "${1}",
    "directory": "${2}",
    "prefix": "https://www.youtube.com/watch?v="
}
EOF
}

bb_dl() {
    echo "Download: ${1} ${2}"
    curl -X 'POST' \
    'http://127.0.0.1:8090/api/download/playlist-download' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d @- <<EOF
{
    "url": "${1}",
    "directory": "${2}",
    "prefix": "https://www.bilibili.com/video/"
}
EOF
}

echo Update Youtube channel
yt_dl "https://www.youtube.com/@playlist/videos" '/tmp/yt-@playlist/'
echo Update Bilibili channel
bb_dl "https://space.bilibili.com/123456/upload/video" '/tmp/bb-123456/'
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