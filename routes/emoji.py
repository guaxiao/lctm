from . import *
from models.emoji import Emoji
import random


main = Blueprint('emoji', __name__)


@main.route('/')
def index():
    return jsonify(Emoji.all())

@main.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        file = request.files['file']
        Emoji.save_zip_file(file)
        return 'ok'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/emoji/add" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
