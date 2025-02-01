from threading import Thread, Lock
from os import SEEK_END
from time import sleep
import re
from fap.iptables import iptables_remove_IP_rule

clients_connected = []
lock = Lock()

connect_pattern = re.compile(
        r'.*DHCPACK\(([\w\d]+)\)\s+([\d+\.]+)\s+([\w\d\:]+)\s+(.*)')
disconnect_pattern = re.compile(r'.*AP-STA-DISCONNECTED\s+([\w\d\:]+)')

def tail(filename: str) -> str:
    filehandler = open(filename, 'r')

    filehandler.seek(0, SEEK_END)
    
    while True:
        line = filehandler.readline()
        if not line:
            sleep(0.1)
            continue

        yield line

def login_client(ip: str) -> None:
    lock.acquire()

    for i in range(0, len(clients_connected)):
        if clients_connected[i][0] == ip:
            clients_connected[i][3] = True
    
    lock.release()

def match_disconnect(log_line: str) -> None:
    m = disconnect_pattern.match(log_line)

    if m is not None:
        lock.acquire()

        try:
            for i in range(0, len(clients_connected)):
                if clients_connected[i][1] == m.group(1):
                    iptables_remove_IP_rule(clients_connected[i][0])

                    del clients_connected[i]
        except IndexError as e:
            print('Error in LogMon:43!')
            print('DEBUG:', clients_connected)

        lock.release()

def match_connect(log_line: str) -> None:
    m = connect_pattern.match(log_line)

    if m is not None:
        lock.acquire()

        clients_connected.append([m.group(2), m.group(3), m.group(4), False])

        lock.release()

class LogMon(Thread):
    def __init__(self, logfile, matchfunc):
        Thread.__init__(self)
        self.logfile = logfile
        self.matchfunc = matchfunc
        self.isrun = True

    def run(self):
        while self.isrun:
            for line in tail(self.logfile):
                print(line, end='')

                self.matchfunc(line)
