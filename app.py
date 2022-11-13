from flask import Flask,request
import mysql.connector
from flask_socketio import SocketIO,send,emit
from uuid import uuid4
import subprocess
import base64
from flask import send_file
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
    print(clients)
    send(request.sid)
@socketio.on('connect')
def connect():
    clients[request.sid] = []
    resp[request.sid] = {}
    emit("session", {"sessionID" : request.sid})
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

@app.route("/format", methods=["GET"])
def format():
    a = clients[request.args.get('id')]
    a = base64.b64decode(a.split(",")[1][-1:])
    with open("file.webm" , "wb+") as f:
        f.write(a)
    subprocess.run(["ffmpeg" ,"-i", "file.webm", "-vn", "file.wav"])

    # generate_wav_file should take a file as parameter and write a wav in it


    return send_file("file.wav", as_attachment=True)
     


if __name__ == '__main__':
    socketio.run(app)
