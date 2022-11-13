from flask import Flask,request
import mysql.connector
from flask_socketio import SocketIO,send
from uuid import uuid4
import subprocess
url = "mysql://ktnbpq3gxt22k2fv:s1wkukxdv5xmxysj@qvti2nukhfiig51b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/dq7hba5u9dvqimjc"
app = Flask(__name__)
clients = {}
resp = {}
socketio = SocketIO(app,cors_allowed_origins="*" )
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@socketio.on('message')
def handle_message(data):
    clients[request.sid] = data
    send(request.sid)
@socketio.on('connect')
def connect():
    clients[request.sid] = []
    resp[request.sid] = {}
    send(request.sid)
@socketio.on('disconnect')
def disconnect():
    clients.pop(request.sid)
    send('disconnected')

@app.route("/answer", methods=["GET"])
def answer():
    if(resp[request.args.get('id')] != {}):
        return resp[request.args.get('id')]
    else:
        return {}

@app.route("format", methods=["GET"])
def format():
    with open("file.webm" , "wb+") as f:
        f.write(clients[request.args.get("id")])
    subprocess.run(["ffmpeg" ,"-i", "file.webm", "-vn", "file.wav"])
if __name__ == '__main__':
    socketio.run(app)
