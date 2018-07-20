#!/usr/bin/env python
# __Author__:cmustard


import datetime
from flask import render_template, Blueprint,render_template_string,request,url_for


discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")



@discover.route("/detail/<int:info_id>",)
def display_detail(info_id):
	return render_template_string(str(info_id))

@discover.route("/")
@discover.route("/discover")
def _discover():
	return "test"
