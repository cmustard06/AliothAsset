#!/usr/bin/env python
# __Author__:cmustard


import threading
import datetime
from flask import render_template, Blueprint,redirect,request,jsonify,url_for
from mvc import db
from mvc.model.model import Discover
from utils.scan import Masscan,Nmap
from utils.comm import *

discover = Blueprint("discover", __name__, template_folder="templates", static_folder="static")


logger = get_logger()

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
			th = threading.Thread(target=scan,args=(target_ip,policy))
			th.start()
		else:

			th = threading.Thread(target=scan, args=(target_ip,policy))
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

@discover.route("/delete", methods=['POST',])
def delete_task():
    if request.method == 'POST':
        try:
            _id = request.form['delete_id']
            select = Discover.query.filter_by(id=_id).first()
            db.session.delete(select)
            db.session.commit()
            return jsonify({"success":"success"})
        except Exception as e:
            print(e)
            logger.warn(str(e))
            return jsonify({"error":"error"})
    else:
        return redirect(url_for("_discover_list"))
	
def scan(host,scanmode="masscan"):
	temp_1 = Discover.query.filter(Discover.ip == host).first()
	temp_1.scan_status = "RUNNING"
	ports = temp_1.config_port
	db.session.add(temp_1)
	db.session.commit()
	info = None
	banner = None
	port = []
	if scanmode =="masscan":
		res = Masscan().scan("-p{}".format(ports),host)
		info = res.get('info')
		port = res.get('open')
		banner = res.get("banner")
		print(info,port,banner)
	elif scanmode == "nmap":
		res = Nmap().scan(host,ports)
		info = res.get("info")
		port = res.get("port")
		banner = res.get("service")
	# 数据库更新
	result = Discover.query.filter(Discover.ip==host).first()
	result.masscan_result = info
	result.service  = banner
	try:
		result.scan_port = ",".join([str(x) for x in list(port)])
	except Exception as e:
		result.scan_port = None
	result.scan_status = "FINISH"
	db.session.add(result)
	db.session.commit()




if __name__ == '__main__':
    masscan("192.168.199.1")
	