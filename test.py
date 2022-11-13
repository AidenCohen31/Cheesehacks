import socketio

sio = socketio.Client()
sio.connect("https://cheesehacks-backend.herokuapp.com/")

print(sio.sid)
sio.disconnect()