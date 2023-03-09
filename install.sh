#!/usr/bin/env bash

[[ ! "$EUID" == "0" ]] && echo "Be root or use sudo" && exit 1

[ ! -x "$(command -v pip3)" ] && echo "No pip3" && exit 1
[ ! -x "$(command -v python3)" ] && echo "No python" && exit 1
[ ! -x "$(command -v sed)" ] && echo "No sed" && exit 1
[ ! -x "$(command -v systemctl)" ] && echo "No systemctl. Are you not using SystemD?" && exit 1

pip3 install -r requirements.txt

cp main.py new.py

printf "Webhook URL: "
read URL

sed -i "s/DEFAULT_URL_CHANGEME/$URL/g" new.py

chmod +x new.py

mv new.py /usr/bin/shushmonitor

echo "Now add /usr/bin/shushmonitor to your crontab (as root) at whatever interval you choose."