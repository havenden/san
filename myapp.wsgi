#!/usr/bin/python
import sys
import logging
activate_this = '/data/htdocs/test.cpnkyy.com/myapp/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/data/htdocs/test.cpnkyy.com/")

from myapp import app as application
application.secret_key = 'dskfl3sklf03sldfa'
