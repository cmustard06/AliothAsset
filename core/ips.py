#!/usr/bin/env python
# __Author__:cmustard
import struct
import socket
import re

from core.ipy import IP
from core.util import logger

Logger = logger()


def ip_check(ip):
	ip_pattern = re.compile(r"^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3}$")
	ret = re.fullmatch(ip_pattern, ip)
	if ret is None:
		return False
	else:
		return True


def ip_handler(raw_ips):
	"""
	对输入的ip进行格式化处理，返回一个列表
	:param raw_ips:
	:return:  outputs=>list
	"""
	raw_ips = raw_ips.replace(" ", "")  # 处理空格，待优化
	outputs = []
	if "/" in raw_ips:  # 192.168.1.0/24
		outputs = _subnet(raw_ips)
	elif "-" in raw_ips:  # 192.168.1.1-192.168.1.4
		outputs = _range(raw_ips)
	elif "," in raw_ips:  # 192.168.1.2,192.168.1.5
		outputs = _simple_segment(raw_ips)
	else:  # 192.168.1.1
		if (ip_check(raw_ips)):
			outputs.append(raw_ips)
	return outputs


def _subnet(raw_ips):
	"""
	处理192.168.1.0/24,先凑合用
	:param raw_ips:
	:return:  outputs=>list
	"""
	outputs = []
	try:
		ips = IP(raw_ips)
	except Exception as e:
		Logger.warning(str(e))
		return outputs
	for x in ips:
		outputs.append("{}".format(x))
	return outputs


def _range(raw_ips):
	"""
	192.168.1.2-192.168.1.66类
	:param raw_ips:
	:return: list
	"""
	try:
		start, end = raw_ips.split("-")
		if not ip_check(start) or not ip_check(end):
			return []
		
		ipstruct = struct.Struct('>I')
		start, = ipstruct.unpack(socket.inet_aton(start))
		end, = ipstruct.unpack(socket.inet_aton(end))
		# print(end)
		return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]
	
	except Exception as e:
		Logger.warning(str(e))
		return []


def _simple_segment(raw_ips):
	"""
	形如192.168.1.1，192.168.1.3.192.168.23.4
	:param raw_ips:
	:return: outputs ->list
	"""
	outputs = []
	temp = raw_ips.split(",")
	for i in temp:
		if not ip_check(i):
			Logger.debug("%s:Data is not recognized", i)
			continue
		else:
			outputs.append(i)
	return outputs

# ############IPV6###################



if __name__ == '__main__':
	print(_simple_segment("192.167.0.1,192.167.1.444"))
