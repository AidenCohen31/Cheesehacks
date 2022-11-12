import socketio

sio = socketio.Client()
sio.connect("http://cheesehacks-backend.herokuapp.com/")

print(sio.sid)
sio.disconnect()