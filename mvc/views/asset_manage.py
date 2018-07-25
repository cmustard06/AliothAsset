#!/usr/bin/env python
# __Author__:cmustard


import datetime
from flask import render_template, Blueprint, render_template_string, request, url_for, redirect,jsonify
from mvc import db
from mvc.model.model import Record
from utils import comm
from utils.icmp import ICMP

manage = Blueprint("manage", __name__, template_folder="templates", static_folder="static", static_url_path="")
logger = comm.get_logger()


@manage.route("/detail", methods=['GET', 'POST'])
def display_detail():
    # 查询select
    try:
        if request.method == 'GET':
            info_id = request.args["info_id"]
        if request.method == 'POST':
            info_id = request.form["info_id"]
        print(info_id)
        result_list = Record.query.filter(Record.id == int(info_id)).first()
        print("-->", type(result_list))
        if result_list is None:
            return redirect(url_for(".index"))

        return render_template("detail.html", item=result_list)
    except Exception as e:
        logger.warn(str(e))
        return redirect(url_for(".index"))



@manage.route("/list", methods=['GET', ])
def index():
    test = [{"first_time": datetime.datetime.ctime(datetime.datetime.now()),
             "update_time": datetime.datetime.ctime(datetime.datetime.now()),
             "local_ip": "192.168.199.2", "local_port": "80,22", "global_ip": "8.8.8.8", "global_port": "80",
             "service": "apache->80,tomcat->8080", "status": "Online", "id": 1}, ]
    try:
        if request.method == 'GET' or request.method == 'POST':
            # 查询数据库
            all_data = db.session.query(Record).all()
            return render_template("list.html", items=all_data)

        else:
            return redirect(url_for("/404"))
    except Exception as e:
        logger.error(str(e))
        return redirect("/404")


@manage.route("/add",methods=['GET','POST'])
def asset_add():
    server_type_map = {"1":"虚拟机","2":"物理机"}
    deployment_type_map = {"4":"在线","5":"库存","6":"借出","7":"报废"}

    if request.method == 'GET':
        return render_template("add.html")
    if request.method == 'POST':
        data = request.form
        # ([('server_type', '2'), ('server_name', 'Web应用服务器'), ('deployment_type', '4'),
        # ('service', 'apache->80,tomcat->8080'), ('local_ip', '192.168.199.2'), ('local_port', '80,8080,22'),
        #  ('global_ip', '1.1.1.1'), ('global_port', '80,8080'), ('eth1_mac', '12:34:56:78:25:44'), ('eth2_mac', ''),
        #  ('manager', '慕君要'), ('manager_phone', '13111111111'),
        #  ('manager_email', 'dmmjy9.com'), ('maintainer', ''), ('maintainer_email', ''), ('desc', '')])
        server_type = server_type_map[data['server_type']]
        server_name = data['server_name']
        deployment_type = deployment_type_map[data['deployment_type']]
        service = data['service']
        if service == "":
            service = None
        local_ip =  data['local_ip']
        local_port = data["local_port"]
        global_ip = data['global_ip']
        if global_ip == "":
            global_ip = None
        global_port = data['global_port']
        if global_port == "":
            global_port = None

        eth1_mac = data['eth1_mac']
        eth2_mac = data['eth2_mac']
        if eth2_mac == "":
            eth2_mac = None

        manager = data['manager']
        manager_phone = data['manager_phone']
        manager_email = data['manager_email']

        maintainer = data['maintainer']
        if maintainer == "":
            maintainer = None
        maintainer_phone = data["maintainer_phone"]
        if maintainer_phone == "":
            maintainer_phone = None
        maintainer_email = data['maintainer_email']
        if maintainer_email == "":
            maintainer_email = None
        desc = data["desc"]
        if desc == "":
            desc = None
        server_os = data["server_os"]
        configuration = data['configuration']
        if configuration == "":
            configuration = None
            
        # icmp
        icmp = ICMP()
        isAlive=icmp.ping(local_ip)
        # 数据库
        first_time = datetime.datetime.now()
        db.session.add(Record(server_type=server_type,first_time=first_time,update_time=first_time,deployment_type=deployment_type,
                              server_name=server_name,server_os=server_os,service=service,local_ip=local_ip,local_port=local_port,
                              global_ip=global_ip,global_port=global_port,configuration=configuration,eth1_mac=eth1_mac,
                              eth2_mac=eth2_mac,isAlive=isAlive,manager=manager,manager_phone=manager_phone,manager_email=manager_email,
                              maintainer=maintainer,maintainer_email=maintainer_email,maintainer_phone=maintainer_phone))
        db.session.commit()
        return jsonify({"success":"success"})
    
@manage.route("/update",methods=['GET',"POST"])
def asset_update():
    pass
