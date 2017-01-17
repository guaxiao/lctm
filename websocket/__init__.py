from flask_socketio import SocketIO
from flask import session
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from models.channel import Channel
from models.chat import Chat
from models.reaction import Reaction
from models.emoji import Emoji
import html


socketio = SocketIO()


def default_channel():
    from models.channel import Channel
    return Channel.query.first()


def save_chat(channel_id):
     from models.channel import Channel
     c = Channel.query.get(channel_id)


def current_user():
    from models.user import User
    uid = int(session.get('uid', -1))
    u = User.query.get(uid)
    return u


@socketio.on('connect')
def connect():
    message = {
        'type': 'join',
        'channel': Channel.default_channel().name,
        'username': current_user().username,
        'avatar': current_user().avatar,
        'content': '{} 加入聊天'.format(current_user().username)
    }
    emit('message', message, broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', current_user().id)


@socketio.on('join_channel')
def join(channel):
    message = {
        'type': 'join',
        'channel': channel,
        'username': current_user().username,
        'avatar': current_user().avatar,
    }
    join_room(channel)
    emit('message', message, broadcast=True)


@socketio.on('leave_channel')
def leave(channel):
    message = {
        'type': 'left',
        'channel': channel,
        'username': current_user().username,
        'avatar': current_user().avatar,
    }
    leave_room(channel)
    emit('message', message, broadcast=True)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    room = message.get('channel', Channel.default_channel().name)
    message['content'] = html.escape(message['content'])
    c = {
        'content': message.get('content', ''),
        'user': current_user(),
        'channel': Channel.find_by_name(room),
    }
    chat = Chat(c).save()
    message['id'] = chat.id
    message['type'] = 'message'
    message['username'] = current_user().username
    message['avatar'] = current_user().avatar

    join_room(room)
    emit('message', message, broadcast=True)

@socketio.on('toggle_reaction')
def toggle_reaction(message):
    room = message.get('channel', Channel.default_channel().name)
    join_room(room)
    chat_id = message.get('chat_id', 1)
    emoji_id = message.get('emoji_id', 1)
    d = {
        'emoji': Emoji.find_by_id(emoji_id),
        'user': current_user(),
        'chat': Chat.find_by_id(chat_id),
    }
    status = Reaction.toggle(d)
    message['status'] = status
    emit('response_toggle_reaction', message, broadcast=True)
