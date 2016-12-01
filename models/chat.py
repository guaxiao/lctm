from . import ModelMixin
from . import db
from . import timestamp


class Chat(db.Model, ModelMixin):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.channel = form.get('channel', '')
        # self.user_id = form.get('user_id', '')
        self.created_time = timestamp()
