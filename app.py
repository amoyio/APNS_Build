# coding: utf-8

from datetime import datetime

from flask import Flask,request
from flask import render_template
from flask_sockets import Sockets

from views.todos import todos_view

# --------
import time
from apns import APNs, Frame, Payload

app = Flask(__name__)
sockets = Sockets(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Hello POST'
    else:
        apns = APNs(use_sandbox=True, cert_file='apns_dev_noti_cert.pem', key_file='apns_dev_noti_key_nopass.pem')

        token_hex = 'd2dc5040b1db1e10c2ee208d68d4b2c426d490dac5a30b56d9c34763a1db13de'
        payload = Payload(alert="Hello World!", sound="default", badge=1)
        apns.gateway_server.send_notification(token_hex, payload)

        return 'Hello GET'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9000')