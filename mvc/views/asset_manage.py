#!/usr/bin/env python
# __Author__:cmustard


import datetime
from flask import render_template, Blueprint, render_template_string, request, url_for, redirect
from mvc import db
from mvc.model.model import Record
from utils import comm

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


@manage.route("/")
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
        return redirect(url_for("/404"))


@manage.route("/add")
def asset_add():
    return render_template("add.html")
