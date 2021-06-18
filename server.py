from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_cors import CORS
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'my-very-secret-code-that-noone-knows'
socketio = SocketIO(app, cors_allowed_origins="*",
                    path="socket.io", engineio_logger=True, logger=True)


def log(message):
    print('\n\n\n\n' + message + '\n\n\n\n')


@app.route("/")
def show_stat():
    return "<p>Geekhub Chat API</p>"


# connection
@socketio.on('connect')
def on_client_connect(auth):
    log('client connected: ' + str(request.sid))


@socketio.on('disconnect')
def on_client_disconnect():
    log('client disconnected')


# room
@socketio.on('client/join')
def on_join(data):
    log('user joined: ' + str(data))
    sid = request.sid
    username = data['username']
    room = data['room']
    join_room(room)
    to_send = {
        'message': username + ' has entered the room: ' + room,
        'username': 'bot',
        'room': room,
        'sid': 0
    }
    emit('server/join', room, to=sid)
    emit('server/message', to_send, to=room)


@ socketio.on('client/leave')
def on_leave(data):
    log('user left: ' + str(data))
    sid = request.sid
    username = data['username']
    room = data['room']
    leave_room(room)
    to_send = {
        'message': username + ' has left the room: ' + room,
        'username': 'bot',
        'room': room,
        'sid': 0
    }
    emit('server/leave', room, to=sid)
    emit('server/message', to_send, to=room)


@ socketio.on('client/rooms')
def get_client_rooms(data):
    sid = request.sid
    client_rooms = rooms(sid=sid)
    to_send = {'sid': sid, 'rooms': client_rooms}
    emit('server/rooms', to_send, to=sid)


# message
@ socketio.on('client/message')
def on_receive_message(data):
    log('received message: ' + str(data))
    sid = request.sid
    username = data['username']
    room = data['room']
    message = data['message']
    to_send = {
        'message': message,
        'username': username,
        'room': room,
        'sid': sid
    }
    emit('server/message', to_send, to=room)


# runner
if __name__ == '__main__':
    socketio.run(app, debug=True)
