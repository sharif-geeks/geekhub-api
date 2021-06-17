from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-very-secret-code-that-noone-knows'
socketio = SocketIO(app, cors_allowed_origins="*", path="socket.io")


@app.route("/")
def show_stat():
    return "<p>Geekhub Chat API</p>"


# connection
@socketio.on('connect')
def handle_client_connect(auth):
    print('client connected: ', str(auth))
    emit('server/connect', {'data': 'Connected'})


@socketio.on('disconnect')
def handle_client_disconnect():
    print('client disconnected')


# room
@socketio.on('client/join')
def on_join(data):
    print('user connected: ' + str(data))
    username = data['username']
    room = data['room']
    join_room(room)
    to_send = {
        'message': username + ' has entered the room.',
        'username': 'bot',
        'sid': 0
    }
    emit('server/message', to_send, to=room)


@socketio.on('client/leave')
def on_leave(data):
    print('user left: ' + str(data))
    username = data['username']
    room = data['room']
    leave_room(room)
    to_send = {
        'message': username + ' has left the room.',
        'username': 'bot',
        'sid': 0
    }
    emit('server/message', to_send, to=room)


@socketio.on('client/rooms')
def get_client_rooms(data):
    sid = request.sid
    client_rooms = rooms(sid=sid)
    to_send = {'sid': sid, 'rooms': client_rooms}
    emit('server/rooms', to_send, to=sid)


# message
@socketio.on('client/message')
def handle_receive_message(data):
    print('received message: ' + str(data))
    sid = request.sid
    username = data['username']
    room = data['room']
    message = data['message']
    to_send = {'message': message, 'username': username, 'sid': sid}
    emit('server/message', to_send, to=room)


# runner
if __name__ == '__main__':
    socketio.run(app, debug=True)
