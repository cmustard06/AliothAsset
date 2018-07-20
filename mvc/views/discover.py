#!/usr/bin/env python
# __Author__:cmustard

from flask import render_template, Blueprint,render_template_string,request


discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")


@discover.route("/")
def index():
	if request.method == 'GET':
		return render_template("discover.html")
	elif request.method == "POST":
		return render_template("discover.html")
	else:
		return render_template("discover.html")