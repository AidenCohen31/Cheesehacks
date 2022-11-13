from flask import Flask,request
import mysql.connector
from flask_socketio import SocketIO,send,emit
from uuid import uuid4
import subprocess
import base64
from flask import send_file
import wave
import numpy as np
from sklearn.decomposition import KernelPCA, TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
import tensorflow as tf
from keras import Model, Sequential
from keras.layers import Input, LSTM, Dense, RepeatVector, TimeDistributed
import librosa
import os
import scipy

url = "mysql://ktnbpq3gxt22k2fv:s1wkukxdv5xmxysj@qvti2nukhfiig51b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/dq7hba5u9dvqimjc"
app = Flask(__name__)
clients = {}
resp = {}
socketio = SocketIO(app,cors_allowed_origins="*" )
file = 0
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@socketio.on('message')
def handle_message(data):
    clients[request.sid] = data["data"]
    if(len(data["data"]) > 0):
        train(request.sid,format(request.sid))
@socketio.on('connect')
def connect():
    clients[request.sid] = ""
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

def train(id, compare_audio):
    f = {0: ["0.wav", "1.wav", "2.wav"], 1 : ["3.wav", "4.wav", "5.wav"], 2 :["9.wav","10.wav", "11.wav", "12.wav", "13.wav"],
        3: ["14.wav", "15.wav"], 5 : ["6.wav"], 6: ["7.wav", "8.wav"]}
    d = {0 : ["Rain Check", "https://www.youtube.com/watch?v=cYBCrCGw2b0"] , 
            1 : ["Kreepa Oh No", "https://www.youtube.com/watch?v=cYBCrCGw2b0"] , 
            3 : ["The Astronaut" , "https://www.youtube.com/watch?v=c6ASQOwKkhk"] , 2 : 
            ["Blinding Lights", "https://www.youtube.com/watch?v=4NRXx6U8ABQ"],
            5: ["Random Short", "np"], 6: ["Without Me" , "https://www.youtube.com/watch?v=tqxRidAWER8&ab_channel=Eminem-Topic"]}
    x = []
    labels=[]
    for i in os.listdir("tests"):
        if(i.endswith(".wav")):
            data, rate = librosa.load(f"tests/{i}")
            ms = librosa.feature.melspectrogram(data, rate)
            a = TruncatedSVD(7)
            sig = a.fit_transform(ms)
            x.append(sig.flatten())
            labels.append([j for j in f if i in f[j]][0])
    labels = np.array(labels)
    k = KMeans(init ='k-means++', n_clusters= len(d))
    k.fit(x)
    c,rate = librosa.load(compare_audio)

    ms = librosa.feature.melspectrogram(c)

    a = TruncatedSVD(7)
    sig = a.fit_transform(ms)
    x= np.array(x).astype('float64')
    print(x.shape)
    pred_classes = k.predict(x)
    print(sig.flatten().reshape(1,-1).shape)
    p = k.predict(sig.flatten().reshape(1,-1).astype('float64'))

    resp[id] = { "ans" : d[scipy.stats.mode(labels[np.where(pred_classes == p)]).mode[0]], "score" : 1-k.score(sig.flatten().reshape(1,-1).astype('float64'))}


def format(id):
    a = clients[id]
    a = base64.b64decode(a.split(",")[1][:-1])
    with open(f"tests/{file}.webm" , "wb+") as f:
        f.write(a)
    subprocess.run(["ffmpeg" ,"-i", f"tests/{file}.webm", "-vn", f"tests/{file}.wav"])
    temp = file
    file += 1
    return f"{temp}.wav"



if __name__ == '__main__':
    socketio.run(app)
