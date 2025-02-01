import fap
from .iptables import iptables_flush

def _exit():
    iptables_flush()
    fap.stop_processes()

    print('\nBye bye...')

    exit(0)

COMMANDS = {
    'start': fap.start,
    'exit': _exit
}

def process_user_input(user_input: str) -> None:
    if user_input in COMMANDS:
        COMMANDS[user_input]()
    else:
        print('No such command: %s\n', user_input)

def main():
    print('Fake Access Point')

    while True:
        try:
            user_input = input('fap> ')

            process_user_input(user_input)
        except EOFError as e:
            _exit()

if __name__ == '__main__':
    main()
