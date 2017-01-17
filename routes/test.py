from . import *
from models.user import User
from models.channel import Channel
from models.emoji import Emoji
from models.chat import Chat
from models.reaction import Reaction


main = Blueprint('test', __name__)


@main.route('/user/create')
def user_create():
    args = request.args
    User(args).save()
    return 'ok'


@main.route('/channel/create')
def channel_create():
    args = request.args
    Channel(args).save()
    return 'ok'


@main.route('/chat/create')
def chat_create():
    args = request.args
    uid = args.get('uid', 1)
    cid = args.get('cid', 1)
    content = args.get('content', '')
    u = User.query.get(uid)
    c = Channel.query.get(cid)
    chat = {
        'content': content,
        'user': u,
        'channel': c,
    }
    Chat(chat).save()
    return 'ok'


@main.route('/reaction/create')
def reaction_create():
    args = request.args
    uid = args.get('uid', 1)
    cid = args.get('cid', 1)
    eid = args.get('eid', 1)
    u = User.query.get(uid)
    c = Chat.query.get(cid)
    e = Emoji.query.get(eid)
    d = {
        'emoji': e,
        'user': u,
        'chat': c,
    }
    Reaction(d).save()
    return 'ok'


@main.route('/reaction/get')
def reaction_get():
    args = request.args
    cid = args.get('cid')
    l = [r.format_reaction() for r in Chat.query.get(cid).reactions]
    return jsonify(l)
