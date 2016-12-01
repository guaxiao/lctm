from models.user import User
from routes import *


main = Blueprint('user', __name__)

Model = User

chat_channel = 'water'


@main.route('/login')
def index():
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form.get('username', '')
    u = User.query.filter_by(username=username).first()
    if u is not None and u.validate_login(form):
        session['uid'] = u.id
        return redirect(url_for('chat.index'))
    else:
        return redirect(url_for('.index'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
        session['uid'] = u.id
        return redirect(url_for('chat.index'))
    else:
        return redirect(url_for('.index'))
