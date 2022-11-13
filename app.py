from flask import Flask,request
import mysql.connector
from flask_socketio import SocketIO,send
from uuid import uuid4
url = "mysql://ktnbpq3gxt22k2fv:s1wkukxdv5xmxysj@qvti2nukhfiig51b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/dq7hba5u9dvqimjc"
app = Flask(__name__)
clients = {}
socketio = SocketIO(app,cors_allowed_origins="*" )
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@socketio.on('message')
def handle_message(data):
    clients[request.sid].append(data)
    print(data)

@socketio.on('connect')
def connect():
    clients[request.sid] = []
    send(request.sid)
    print(request.sid)
    print("client connected")
@socketio.on('disconnect')
def disconnect():
    clients.pop(request.sid)
    send('disconnected')

if __name__ == '__main__':
    socketio.run(app)
