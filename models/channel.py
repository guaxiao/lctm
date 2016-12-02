from . import ModelMixin
from . import db
from . import timestamp


class Channel(db.Model, ModelMixin):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    created_time = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # chats = db.relationship('Chat', backref='channel', lazy='dynamic')

    def __init__(self, form):
        self.name = form.get('name', '')
        self.description = form.get('description', '')
        self.created_time = timestamp()

    def update(self, form):
        self.name = form.get('name', '')
        self.description = form.get('description', '')
