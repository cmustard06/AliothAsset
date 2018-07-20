#!/usr/bin/env python
# __Author__:cmustard


from random import sample
from string import  digits,ascii_lowercase
from flask import Flask
from .views.asset_manage import manage
from .views.discover import discover

app = Flask(__name__,template_folder="templates",static_folder="static")

app.config['SECRET_KEY'] = ''.join(sample(digits + ascii_lowercase, 10))

app.register_blueprint(manage)
app.register_blueprint(discover)

def start():
	app.run("0.0.0.0",port=8080,debug=True)
	
if __name__ == '__main__':
    start()