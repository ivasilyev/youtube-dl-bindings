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
