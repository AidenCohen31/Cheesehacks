import socketio

sio = socketio.Client()
sio.connect("http://localhost:5000/")

print(sio.sid)
sio.disconnect()