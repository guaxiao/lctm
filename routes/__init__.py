from flask import request
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for
from flask import Response
from flask import session

import time


def current_time():
    return int(time.time())
