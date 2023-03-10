#!/usr/bin/env bash

[[ ! "$EUID" == "0" ]] && echo "Be root or use sudo" && exit 1

[ ! -x "$(command -v pip3)" ] && echo "No pip3" && exit 1
[ ! -x "$(command -v python3)" ] && echo "No python" && exit 1
[ ! -x "$(command -v sed)" ] && echo "No sed" && exit 1
[ ! -x "$(command -v systemctl)" ] && echo "No systemctl. Are you not using SystemD?" && exit 1

pip3 install -r requirements.txt

printf "Webhook URL: "
read URL

[[ ! -d /etc/shushmonitor ]] && mkdir -p /etc/shushmonitor

echo "$URL" > /etc/shushmonitor/webhook

chmod +x main.py

mv main.py /usr/bin/shushmonitor

echo "Now add /usr/bin/shushmonitor to your crontab (as root) at whatever interval you choose."