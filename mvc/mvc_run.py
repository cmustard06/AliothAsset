#!/usr/bin/env python
# __Author__:cmustard


from random import sample
from string import  digits,ascii_lowercase

from flask import render_template,redirect,url_for

from .views.asset_manage import manage,index
from .views.discover import discover
from mvc import app

# app = Flask(__name__,template_folder="templates",static_folder="static")
app.config['template_folder'] = "templates"
app.config['static_folder'] = "static"
app.config['static_url_path'] = "static"
app.config['SECRET_KEY'] = ''.join(sample(digits + ascii_lowercase, 10))

app.register_blueprint(manage)
app.register_blueprint(discover)

@app.errorhandler(404)
def not_found(error):
	return render_template("404.html"),404

@app.errorhandler(500)
def server_error(error):
	return render_template("404.html"),500

@app.route("/")
def main_page():
	return redirect("/list")

def start():
	app.run("0.0.0.0",port=8080,debug=True)
	
if __name__ == '__main__':
    start()