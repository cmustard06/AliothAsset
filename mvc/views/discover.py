#!/usr/bin/env python
# __Author__:cmustard


import threading
import datetime
from flask import render_template, Blueprint,redirect,request,jsonify
from mvc import db
from mvc.model.model import Discover
from utils.scan import Masscan


discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")




@discover.route("/add_task",methods=['POST','GET'])
def _discover():
	policy_map = {"2":"masscan","3":"nmap+masscan","4":"nmap"}
	if request.method == 'POST':
		data = request.form
		task_name = data['task_name']
		target_ip = data['target_ip']
		policy = data['policy']
		policy = policy_map[policy]
		print(task_name,target_ip,policy)
		# 是否已经在数据库中
		result = Discover.query.filter(Discover.ip==target_ip).all()
		if len(result) == 0:
			# 存储数据库中
			db.session.add(Discover(dis_time=datetime.datetime.now(),ip=target_ip,scan_policy=policy))
			db.session.commit()
			if policy == "masscan":
				th = threading.Thread(target=masscan,args=(target_ip,))
				th.start()
		else:
			if policy == 'masscan':
				th = threading.Thread(target=masscan, args=(target_ip,))
				th.start()

		return jsonify({"success":"success"})
	elif request.method == 'GET':
		return render_template("discover.html")
	else:
		redirect("/404",404)

@discover.route("/discover",methods=['GET'])
def _discover_list():
	if request.method == 'GET':
		items = db.session.query(Discover).all()
		return render_template("dis_list.html",items=items)
	
	
def masscan(host):
	temp_1 = Discover.query.filter(Discover.ip == host).first()
	temp_1.scan_status = "RUNNING"
	ports = temp_1.config_port
	db.session.add(temp_1)
	db.session.commit()
	res = Masscan().scan("-p{}".format(ports),host)
	info = res.get('info')
	port = res.get('open')
	banner = res.get("banner")
	print(info,port,banner)
	# 数据库更新
	result = Discover.query.filter(Discover.ip==host).first()
	result.masscan_result = info
	result.service  = banner
	result.scan_port = ",".join([str(x) for x in list(port)])
	result.scan_status = "FINISH"
	db.session.add(result)
	db.session.commit()

if __name__ == '__main__':
    masscan("192.168.199.1")
	