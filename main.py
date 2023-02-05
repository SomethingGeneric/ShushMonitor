# System
import sys,os

# Pip
import toml

if not os.path.exists("hosts.toml"):
    print("Please copy 'ex_hosts.toml' to 'hosts.toml' and edit.")
    sys.exit(1)

rdata = open("hosts.toml").read().strip()

data = toml.loads(rdata)

for host in data:
    name = host
    info = data[host]

    silent = ""
    command = ""

    if info['os'] == 'debian':
        silent = "apt update"
        command = "apt list --upgradable"

    if command == "":
        print(f"Don't know how to check OS: {info['os']}")

    print(f"Going to run: \"ssh {info['user']}@{info['ip']} '{silent};{command}'\"")