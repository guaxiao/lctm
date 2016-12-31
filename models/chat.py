from . import ModelMixin
from . import db
from . import timestamp


class Chat(db.Model, ModelMixin):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))

    # channel = db.relationship('Chat', backref='channel', lazy='dynamic')
    # user = db.relationship('User', backref='user', lazy='dynamic')


    def __init__(self, form):
        self.content = form.get('content', '')
        # self.channel = form.get('channel', '')
        self.channel = form.get('channel', '')
        self.user = form.get('user', '')
        self.created_time = timestamp()
