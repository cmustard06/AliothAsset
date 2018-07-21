#!/usr/bin/env python
# __Author__:cmustard

import pymysql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SECRET_KEY'] ='@1`qweer,.?123'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1/asset' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app) #实例化