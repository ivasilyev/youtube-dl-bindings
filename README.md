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

python updater.py
```

## Run web server

```shell script
python3 rest.py
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
