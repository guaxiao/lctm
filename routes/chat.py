from models.chat import Chat
from models.user import User
from models.channel import Channel
from routes import *
import redis
import json
from functools import wraps


def current_user():
    uid = int(session.get('uid', -1))
    u = User.query.get(uid)
    return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            # r = {
            #     'success': False,
            #     'message': '未登录',
            # }
            # return jsonify(r)
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)
    return function


main = Blueprint('chat', __name__)

Model = Chat

red = redis.Redis(host='localhost', port=6379, db=0)
chat_channel = 'water'


def stream():
    pubsub = red.pubsub()
    pubsub.subscribe(chat_channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            yield 'data: {}\n\n'.format(data)


@main.route('/')
@login_required
def index():
    cs = Channel.query.all()
    # return render_template('chat_index.html', chat_list=ms)
    return render_template('chat_room.html', channel_list=cs)


@main.route('/test')
def test():
    cs = Channel.query.all()
    print(cs)
    return render_template('chats.html', channel_list=cs)


@main.route('/add', methods=['POST'])
@login_required
def add():
    u = current_user()
    msg = request.get_json()
    content = msg.get('content', '')
    channel = msg.get('channel', '')
    r = {
        'content': content,
        'channel': channel,
        'created_time': current_time(),
        'username': u.username,
    }
    m = Model(r)
    m.user_id = u.id
    m.save()
    print('add chat', m)
    message = json.dumps(r, ensure_ascii=False)
    red.publish(chat_channel, message)
    return 'OK'


@main.route('/subscribe')
@login_required
def subscribe():
    s = stream()
    mime = 'text/event-stream'
    return Response(s, mimetype=mime)
