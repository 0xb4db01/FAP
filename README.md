# Fake Access Point (FAP)

This is a dirty, really dirty PoC I wrote for a fake access point live demo. The goal is to create a Wi-Fi access point that actually provides internet to devices that connect, first provinding a landing page that asks for credentials that you will grab because j00 r 1337 h4x0r.

I tested it on a Linux laptop and on a Raspberry Pi model 3b with 1 gb ram and Kali Linux with X removed. I was able to have 8 devices connected simultaneously and browsing without problems.

Code is awful and the prompt is nonesense, but I may one day fix it and make it better.

# Requisites

- python3
- dnsmask
- hostapd
- wifi interface

# Install

FAP at the moment is meant to run from root, without any fancy configuration.

Git clone this repo in /root, edit the `fapcfg.json` file to suite your needs with networking and log paths, possibly create a virtualenv to pip the requirements and setup install.

**IMPORTANT**: create `/root/log` and `/root/run` directories before running.

# Configuration

The only configuration file you need to touch is `fapcfg.json`. 

```
{
     "iptables": {
        "cmd": "iptables-legacy"
     },
     "dnsmasq": {
        "config_file_tplt": "/root/fap/3rdparty/config/templates/dnsmasq.tplt",
        "log_facility": "/root/log/dnsmasq.log",
        "dhcp_range": "192.168.50.10,192.168.50.100,8h",
        "server": "8.8.8.8",
        "listen_address": "192.168.50.1",
        "pid_file": "/root/run/dnsmasq.pid"
     },
     "hostapd": {
        "config_file_tplt": "/root/fap/3rdparty/config/templates/hostapd.tplt",
        "log_facility": "/root/log/hostapd.log",
        "ssid": "FAP-WIFI",
        "channel": "11",
        "pid_file": "/root/run/hostapd.pid"
     },
    "fap": {
        "dnsmasq_cfg": "/root/fap/3rdparty/config/dnsmasq.conf",
        "hostapd_cfg": "/root/fap/3rdparty/config/hostapd.conf",
        "ip": "192.168.50.1",
        "netmask": "255.255.255.0",
        "network": "192.168.50.0/24",
        "i_interface": "wlan0",
        "o_interface": "eth0",
        "log": "/root/log"
    },
    "flaskaptive": {
        "port": 80,
        "template_folder": "/root/fap/flaskaptive/templates/FREEWIFIZ",
        "static_folder": "/root/fap/flaskaptive/static/FREEWIFIZ"
    }
}
```

As you can see, the configuration file is pretty much compiled, and if you have installed fap on `/root` you should be good to go, unless the default network is not ok for you.

The main things you wanna touch in the configuration for a quick run is the `ssid`, `i_interface`, network stuff and `server` which has a non intuitive name, but it's the external DNS to use.

**IMPORTANT**: note that FAP uses `iptables-legacy` for all the iptables rules and chains. If you want to monitor fw stuff, use the `iptables-legacy` command, if you're unhappy with this, switch to `iptables` in the configuration file.

# Running

Provided you edited correctly the `fapcfg.json` file, you should just run 

```
fap -c fapcfg.json
```

and when prompted type `start` if no errors occured.

**IMPORTANT**: you must run fap from the /root/fap directory you git cloned from. Because templates and static Flask folders are there.

# Customizing FAP landing page

FAP uses Flask for the landing page, and all the web stuff is in `/root/fap/flaskaptive/`, meanwhile the python code is in `/root/fap/fap/flaskaptive/__init__.py`.

You can choose to modify the code there to fit your needs, or to create a new captive portal.

At the moment I'm not gonna document the way to do this, look at `flaskaptive/__init__.py` and good luck. Take also a look at the HTML and JS stuff if you just want to add other login platforms or just modify the default landing page, which is stupid on purpose.

My suggestion for this release is to modify the actual code, as it's in an `__init__.py` file. So use what's provided if you want to add routes and also for the web part, if you want to change the landing page look use the FREEWIFIZ templates and static folders.
