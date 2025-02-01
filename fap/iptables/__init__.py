import subprocess

from fap import config

iptables_cmd = config['iptables']['cmd']

def iptables_flush() -> None:
    print('Flushing iptables...')

    subprocess.run([iptables_cmd, '-F'])
    subprocess.run([iptables_cmd, '-t', 'nat', '-F'])

def iptables_start() -> None:
    print('Setting PREROUTING...')

    subprocess.run([iptables_cmd,
            '-t',
            'nat',
            '-A',
            'PREROUTING',
            '-d',
            '0/0',
            '-p',
            'tcp',
            '--dport',
            '80',
            '-j',
            'DNAT',
            '--to-destination',
            config['fap']['ip']])
    
    print('Setting POSTROUTING...')

    subprocess.run([iptables_cmd,
            '-t',
            'nat',
            '-A',
            'POSTROUTING',
            '-o',
            config['fap']['o_interface'],
            '-j',
            'MASQUERADE'])

    print('Setting FORWARD...')

    subprocess.run([iptables_cmd,
            '-A',
            'FORWARD',
            '-i',
            'wlp3s0',
            '-o',
            config['fap']['i_interface'],
            '-m',
            'state',
            '--state',
            'RELATED,ESTABLISHED',
            '-j',
            'ACCEPT'])

    print('Setting FORWARD...')

    subprocess.run([iptables_cmd,
            '-A',
            'FORWARD',
            '-i',
            config['fap']['i_interface'],
            '-o',
            config['fap']['o_interface'],
            '-j',
            'ACCEPT'])

    print('Setting DROP...')
    
    subprocess.run([iptables_cmd,
            '-I',
            'FORWARD',
            '-s',
            config['fap']['network'],
            '-j',
            'DROP'])

    print('Setting FORWARD http to GW...')
    subprocess.run([iptables_cmd,
            '-I',
            'FORWARD',
            '-s',
            config['fap']['network'],
            '-d',
            config['fap']['ip'],
            '-j'
            'ACCEPT'])

def iptables_allow_IP(ip: str) -> None:
    print('Allowing traffic to:', ip)

    subprocess.run([iptables_cmd,
            '-I',
            'FORWARD',
            '-s',
            ip,
            '-j',
            'ACCEPT'])

def iptables_remove_IP_rule(ip: str) -> None:
    print('Removing FORWARD rule for:', ip)

    subprocess.run([iptables_cmd,
            '-D',
            'FORWARD',
            '-s',
            ip,
            '-j',
            'ACCEPT'])
