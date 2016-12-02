from flask_socketio import SocketIO
from flask import session
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room

socketio = SocketIO()


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message.get('channel')
    print(message)
    emit('message', message, broadcast=True)
    print("fdsfdsfdsfd")
