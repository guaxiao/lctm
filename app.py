from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import logging


from models import db
from models.user import User
from models.channel import Channel
from models.chat import Chat


from websocket import socketio

app = Flask(__name__)
manager = Manager(app)


def register_routes(app):
    from routes.channel import main as routes_channel
    from routes.chat import main as routes_chat
    from routes.user import main as routes_user
    app.register_blueprint(routes_channel, url_prefix='/channel')
    app.register_blueprint(routes_chat, url_prefix='/chat')
    app.register_blueprint(routes_user, url_prefix='/user')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # secret_key 和 数据库配置都放在 config.py 文件中, 例子如下
    # db_uri = 'sqlite:///{}'.format('demo.sqlite')
    # 自行添加
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    app.config['USER_AVATARS_DIR'] = config.user_avatar_dir
    db.init_app(app)
    register_routes(app)
    import os
    if os.path.isfile(config._db_path) is False:
        init_db()
    # init socket app
    socketio.init_app(app)
    # 设置 log, 否则输出会被 gunicorn 吃掉
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configured_app():
    configure_app()
    return app


def init_db():
    with app.app_context():
        db.create_all()
        default_channel = {
            'name': '大厅',
            'description': '没有描述',
        }
        Channel(default_channel).save()


@manager.command
def server():
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

# (gunicorn wsgi --worker-class=gevent -t 4 -b 0.0.0.0:8000 &)
