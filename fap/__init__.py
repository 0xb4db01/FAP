from sys import argv
from getopt import getopt
from json import loads
from time import sleep
import os
import psutil

opts, args = getopt(argv[1:], 'c:')

config_file = None

for opt in opts:
    if opt[0] == '-c':
        config_file = opt[1]

if config_file is None:
    print('args: -c <config file>')

    exit(-1)

config = None

with open(config_file, 'r') as f:
    config = loads(f.read())

import subprocess

from .iptables import *
from .flaskaptive import app
from .logmon import LogMon, clients_connected, match_connect, match_disconnect

# Check for dependencies
hostapd = subprocess.run(['which', 'hostapd'], capture_output=True)
dnsmasq = subprocess.run(['which', 'dnsmasq'], capture_output=True)

if hostapd.stdout == b'':
    print('Missing dependency: hostapd')

    exit(-1)

if dnsmasq.stdout == b'':
    print('Missing dependency: dnsmasq')

    exit(-1)

# Configure network interface
print('Configuring network interface:', config['fap']['i_interface'])
subprocess.run(['ifconfig', 
        config['fap']['i_interface'],
        'down'])

sleep(0.5)

subprocess.run(['ifconfig', 
        config['fap']['i_interface'],
        config['fap']['ip'],
        'netmask',
        config['fap']['netmask'],
        'up'])

# Configure dnsmasq
with open(config['dnsmasq']['config_file_tplt'], 'r') as ftplt:
    print('Configuring dnsmasq...')

    tplt = ftplt.read()

    tplt = tplt.replace('{{interface}}', config['fap']['i_interface'])
    tplt = tplt.replace('{{dhcp_range}}', config['dnsmasq']['dhcp_range'])
    tplt = tplt.replace('{{listen_address}}',
            config['dnsmasq']['listen_address'])
    tplt = tplt.replace('{{server}}', config['dnsmasq']['server'])
    tplt = tplt.replace('{{log_facility}}', config['dnsmasq']['log_facility'])

    fcfg = open(config['fap']['dnsmasq_cfg'], 'w')
    fcfg.write(tplt)
    fcfg.close()

# Configure hostapd
with open(config['hostapd']['config_file_tplt'], 'r') as ftplt:
    print('Configuring hostapd...')

    tplt = ftplt.read()

    tplt = tplt.replace('{{interface}}', config['fap']['i_interface'])
    tplt = tplt.replace('{{ssid}}', config['hostapd']['ssid'])

    fcfg = open(config['fap']['hostapd_cfg'], 'w')
    fcfg.write(tplt)
    fcfg.close()

STATE = {
    'dnsmasq_pid': None,
    'hostapd_pid': None,
}

def stop_processes() -> None:
    print('Stopping hostapd...')

    subprocess.run(['kill', '-9', str(STATE['hostapd_pid'])])

    print('Stopping dnsmasq...')

    subprocess.run(['kill', '-9', str(STATE['dnsmasq_pid'])])

    # Because threads are gonna be hanging...
    psutil.Process(os.getpid()).terminate()

def iptables_init() -> None:
    iptables_flush()
    iptables_start()

def start() -> None:
    # Set ip forwarding...
    print('Setting ip forwarding...')

    subprocess.run(['sysctl', 'net.ipv4.ip_forward=1'])

    iptables_init()

    _dnsmasq = subprocess.Popen([dnsmasq.stdout.decode().strip(), 
            '-C', 
            config['fap']['dnsmasq_cfg'],
            '-x',
            config['dnsmasq']['pid_file']], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            start_new_session=True)

    sleep(0.5)

    dnsmasqlog = LogMon(config['dnsmasq']['log_facility'], match_connect)
    dnsmasqlog.start()

    dnsmasq_pid = None

    with open(config['dnsmasq']['pid_file'], 'r') as f:
        dnsmasq_pid = int(f.read())

    STATE['dnsmasq_pid'] = dnsmasq_pid

    print('dnsmasq running with pid:', STATE['dnsmasq_pid'])

    _hostapd = subprocess.Popen([hostapd.stdout.decode().strip(),
            config['fap']['hostapd_cfg'],
            '-B',
            '-t',
            '-f',
            config['hostapd']['log_facility'],
            '-P',
            config['hostapd']['pid_file']], 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            start_new_session=True)

    sleep(0.5)

    hostapdlog = LogMon(config['hostapd']['log_facility'], match_disconnect)
    hostapdlog.start()

    hostapd_pid = None

    sleep(0.5)

    with open(config['hostapd']['pid_file'], 'r') as f:
        hostapd_pid = int(f.read())

    STATE['hostapd_pid'] = hostapd_pid

    print('hostapd running with pid:', STATE['hostapd_pid'])

    print('Starting flaskaptive...')

    app.run(host=config['fap']['ip'],
            port=config['flaskaptive']['port'], 
            debug=False)
