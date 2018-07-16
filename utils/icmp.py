#!/usr/bin/env python
# __Author__:cmustard


"""
 RFC792, echo/reply message:
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |     Type      |     Code      |          Checksum             |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |           Identifier          |        Sequence Number        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |     Data ...
 +-+-+-+-+-
"""

import os
import struct
import array
import time
import socket

class ICMP(object):
	def __init__(self,timeout=3,IPv6=False):
		self.timeout = timeout
		self.IPv6 = IPv6
		self._data = struct.pack('d',time.time()) # 构造ICMP的负荷字段
		self._id = os.getpid()  # 构造ICMP报文的ID字段
		
	@property  # 属性装饰器
	def _icmpSocket(self):
		"""创建ICMP Socket"""
		if not self.IPv6:
			Sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname("icmp"))
		else:
			Sock = socket.socket(socket.AF_INET6,socket.SOCK_RAW,socket.getprotobyname("ipv6-icmp"))
		return Sock
	
	def _inChecksun(self,packet):
		'''ICMP报文校验和计算方法'''
		if len(packet) & 1:
			packet = packet + '\\0'
		words = array.array('h',packet)
		sum = 0
		for word in words:
			sum += (word & 0xffff)
		sum = (sum >> 16) + (sum & 0xffff)
		sum = sum+(sum>>16)
		return (~sum) & 0xffff
	
	def _icmpPacket(self):
		'''构造ICMP报文'''
		if not self.IPv6:
			header = struct.pack('bbHHh',8,0,0,self._id,0)
		else:
			header = struct.pack("BbHHh",128,0,0,self._id,0)
			
		
		