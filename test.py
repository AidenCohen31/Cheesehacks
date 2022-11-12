import socketio

sio = socketio.Client()
sio.connect("http://cheesehacks-backend.herokuapp.com:5000/")

print(sio.sid)
sio.disconnect()