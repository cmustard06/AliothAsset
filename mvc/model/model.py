#!/usr/bin/env python
# __Author__:cmustard

"""
数据库文件
"""

from mvc import db

class Record(db.Model):
	__tablename__ = 'asset_record'
	id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	first_time = db.Column(db.DateTime,nullable=False)
	update_time = db.Column(db.DateTime,nullable=False)
	server_type = db.Column(db.String(128),nullable=False)
	deployment_type = db.Column(db.String(128),nullable=False)
	server_name = db.Column(db.String(256),nullable=False)
	server_os = db.Column(db.String(64),nullable=False)
	service = db.Column(db.Text,nullable=False)
	local_ip = db.Column(db.String(128),nullable=False,unique=True)
	local_port = db.Column(db.Text,nullable=True)
	global_ip = db.Column(db.String(128),nullable=True)
	global_port = db.Column(db.Text,nullable=True)
	configuration = db.Column(db.Text,nullable=True)
	eth1_mac = db.Column(db.String(48),nullable=True)
	eth2_mac = db.Column(db.String(48),nullable=True)
	isAlive = db.Column(db.Boolean,nullable=False,default=False)
	manager = db.Column(db.String(128),nullable=False)
	manager_email = db.Column(db.String(128),nullable=True)
	manager_phone = db.Column(db.String(32),nullable=True)
	maintainer = db.Column(db.String(128),nullable=True)
	maintainer_phone = db.Column(db.String(32),nullable=True)
	maintainer_email = db.Column(db.String(128),nullable=True)
	desc = db.Column(db.Text,nullable=True)

	def __repr__(self):
		return "< Record {}".format(self.server_name)


class Discover(db.Model):
	__tablename__ = 'asset_discover'
	id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	dis_time = db.Column(db.DateTime,nullable=False)
	ip = db.Column(db.String(128),nullable=False,unique=True)
	service = db.Column(db.Text,nullable=True,default="None")
	scan_policy = db.Column(db.String(32),default="icmp")
	scan_status = db.Column(db.String(32),default="None")
	scan_port = db.Column(db.Text,nullable=True)
	config_port = db.Column(db.Text,default="21,22,23,25,31,42,53,67,69,79,80,99,102,109,110,113,119,135,137,138,139,143,161,177,389,443,456,513,993,1024,1080,1433,1999,3389,3306,8000,8080,13223,88,137,161,162,445,500")
	nmap_result = db.Column(db.Text,nullable=True,default=None)
	masscan_result = db.Column(db.Text,nullable=True,default=None)

	def __repr__(self):
		return "< Discover {}>".format(self.ip)

def create_database():
	db.drop_all()
	db.create_all()

if __name__ == '__main__':
    create_database()