from . import ModelMixin
from . import db


class Reaction(db.Model, ModelMixin):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    emoji_id = db.Column(db.Integer, db.ForeignKey('emojis.id'))


    def __init__(self, form):
        self.user = form.get('user', '')
        # self.channel = form.get('channel', '')
        self.chat = form.get('chat', '')
        self.emoji = form.get('emoji', '')

    def format_reaction(self):
        d = {
            'user_id': self.user_id,
            'chat_id': self.chat_id,
            'emoji_id': self.emoji_id,
        }
        return d

    @classmethod
    def toggle(cls, data):
        d = {
            'user_id': data['user'].id,
            'chat_id': data['chat'].id,
            'emoji_id': data['emoji'].id,
        }
        r = cls.query.filter_by(**d).first()
        if r is None:
            cls(data).save()
            return 'add'
        else:
            r.delete()
            return 'delete'
