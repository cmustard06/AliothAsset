#!/usr/bin/env python
# __Author__:cmustard

import threading
import datetime
from flask import render_template, Blueprint,render_template_string,request,jsonify
from mvc import db
from mvc.model.model import Discover
from utils.scan import Masscan


discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")




@discover.route("/add_task",methods=['POST','GET'])
def _discover():
	policy_map = {"1":"icmp","2":"masscan","3":"nmap+masscan","4":"nmap"}
	if request.method == 'POST':
		data = request.form
		task_name = data['task_name']
		target_ip = data['target_ip']
		policy = data['policy']
		policy = policy_map[policy]
		print(task_name,target_ip,policy)
		# 存储数据库中
		db.session.add(Discover(dis_time=datetime.datetime.now(),ip=target_ip,scan_policy=policy))
		db.session.commit()
		
		
		return jsonify({"success":"success"})
	elif request.method == 'GET':
		return render_template("discover.html")

@discover.route("/discover",methods=['GET'])
def _discover_list():

	if request.method == 'GET':
		item = [{"create_time":"2017-11-12 25:33:56","desc":"123","ip":"11.1.1.1","port":"12,80,443"},]
		return render_template("dis_list.html",items=item)
	
	
def msscan(host,ports):
	res = Masscan.scan("-p{}".format(ports),host)
	info = res.get('info')
	port = res.get('open')
	banner = res.get("banner")
	# 数据库更新
	
	