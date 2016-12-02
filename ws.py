#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

sys.path.insert(0, abspath(dirname(__file__)))


import app
application = app.configured_app()

# gunicorn -k gevent -w 1 ws:application
