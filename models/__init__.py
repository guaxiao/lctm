from flask_sqlalchemy import SQLAlchemy
import time

from flask import current_app

app = current_app


db = SQLAlchemy()


def timestamp():
    return int(time.time())


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0}=({1})'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '  \n'.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)
