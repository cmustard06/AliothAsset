#!/usr/bin/env python
# __Author__:cmustard


import datetime
from flask import render_template, Blueprint,render_template_string,request,url_for


discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")



@discover.route("/detail/<int:info_id>",)
def display_detail(info_id):
	return render_template_string(str(info_id))

@discover.route("/")
def index():
	test = [{"first_time":datetime.datetime.ctime(datetime.datetime.now()),"update_time":datetime.datetime.ctime(datetime.datetime.now()),
			"local_ip":"192.168.199.2","local_port":"80,22", "global_ip":"8.8.8.8","global_port":"80",
			"service":"apache->80,tomcat->8080","status":"Online","id":1},]
	if request.method == 'GET':
		return render_template("list.html",items=test)
	elif request.method == "POST":
		return render_template("discover.html")
	else:
		return render_template("discover.html")
