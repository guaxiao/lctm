from . import ModelMixin
from . import db
import zipfile
import os


class Emoji(db.Model, ModelMixin):
    __tablename__ = 'emojis'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128))

    reactions = db.relationship('Reaction', backref='emoji', lazy='dynamic')

    def __init__(self, form):
        self.value = form.get('value', '')

    @classmethod
    def all(cls):
        return [e.format_emoji() for e in cls.query.all()]

    def format_emoji(self):
        d = {
            'key': ':{}:'.format(self.id),
            'value': self.value,
        }
        return d

    @classmethod
    def save_zip_file(cls, file):
        zip = zipfile.ZipFile(file)
        base_path = os.getcwd()
        emoji_file_path = os.path.join(base_path, 'static', 'emoji')
        for name in zip.namelist():
            d = zip.read(name)
            p = os.path.join(emoji_file_path, name)
            if (name.endswith('/')):
                if (not os.path.exists(p)):
                    os.makedirs(p)
            else:
                with open(p, 'wb') as f:
                    f.write(d)
                    cls({
                        'value': '/static/emoji/' + name
                    }).save()
