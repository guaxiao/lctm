import hashlib
import os

from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    channel = db.relationship('Channel', backref='user', lazy='dynamic')
    chats = db.relationship('Chat', backref='user', lazy='dynamic')

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self, form):
        password = form.get('password', '')
        return password == self.password

    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() is None
        print(self.username, self.password)
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password) >= 3
        # valid_captcha = self.captcha == '3'
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        if not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        if not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        # if not valid_captcha:
            # message = '验证码必须输入 3'
            # msgs.append(message)
        # status = valid_username and valid_username_len and valid_password_len and valid_captcha
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs
