#!/usr/bin/env python3

# System
import sys,os,subprocess,shutil

# PyPi
from discord_webhook import DiscordWebhook

if not os.path.exists("/etc/shushmonitor/webhook"):
    print("Set webhook in /etc/shushmonitor/webhook")
    sys.exit(1)

webhook_url = open("/etc/shushmonitor/webhook").read().strip()

if not os.path.exists("/etc/issue"):
    # fail code
    print("No /etc/issue")
    sys.exit(1)

if not os.path.exists("/etc/hostname"):
    # fail code
    print("No /etc/hostname")
    sys.exit(1)

issue = open("/etc/issue").read().lower()
host = open("/etc/hostname").read().strip()

if "debian" in issue or "ubuntu" in issue:
    # apt time
    os.system("apt update")
    res = subprocess.check_output(['apt','list','--upgradable']).decode()
elif "arch" in issue or "crystal" in issue:
    # pacman time
    if shutil.which("checkupdates") is None:
        res = "You've not installed the package 'pacman-contrib'."
    else:
        res = subprocess.check_output(["checkupdates","--nocolor"]).decode()

msg = f"Update check for {host}:\n```\n{res}\n```"

if len(msg) < 1024:
    webhook = DiscordWebhook(url=webhook_url, content=msg)
    webhook.execute()
else:
    sent = False
    for exec in ["nc", "netcat"]:
        if shutil.which(exec) is not None:
            with open("temp.out", "w") as f:
                f.write(res)
            url = subprocess.check_output([f"cat temp.out | {exec} termbin.com 9999"])
            webhook = DiscordWebhook(url=webhook_url, content=f"Output was too long, please view: {url}")
            webhook.execute()
            os.remove("temp.out")
            sent = True
    if not sent:
        print("Uhoh can't paste long output. Failing.")
        sys.exit(1)
