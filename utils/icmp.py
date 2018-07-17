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
	def __init__(self,timeout=2,IPv6=False):
		self.timeout = timeout
		self.IPv6 = IPv6
		self._data = struct.pack('d',time.time()) # 构造ICMP的负荷字段
		self._id = os.getpid()  # 构造ICMP报文的ID字段
		self._flag = []
		
	@property  # 属性装饰器
	def __icmpSocket(self):
		"""创建ICMP Socket"""
		if not self.IPv6:
			Sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname("icmp"))
		else:
			Sock = socket.socket(socket.AF_INET6,socket.SOCK_RAW,socket.getprotobyname("ipv6-icmp"))
		return Sock
	
	def __inChecksum(self,packet):
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
	
	def __icmpPacket(self):
		'''构造ICMP报文'''
		if not self.IPv6:
			header = struct.pack('bbHHh',8,0,0,self._id,0)
		else:
			header = struct.pack("BbHHh",128,0,0,self._id,0)
			
		packet = header +self._data
		chkSum = self.__inChecksum(packet)
		if not self.IPv6:
			header = struct.pack('bbHHh',8,0,chkSum,self._id,0)
		else:
			header = struct.pack('BhHHh',128,0,chkSum,self._id,0)
		
		return header+self._data
	
	
	def ping(self,ip):
		'''利用ICMP报文探测网络主机存活'''
		Sock = self.__icmpSocket
		Sock.settimeout(self.timeout)
		packet = self.__icmpPacket()
		# print(repr(packet))
		# send
		for index in range(4):
			try:
				Sock.sendto(packet,(ip,0))
			except socket.timeout:
				print("access timeout")
				continue
			except WindowsError as e:
				self._flag.append(False)
				print("Unable to connect to host")
				break
			except Exception as e:
				print("send execption:%s"%str(e))
				self._flag.append(False)
			# receive
			try:
				recv_result = Sock.recvfrom(1024)[1][0]
				self._flag.append(True)
				continue
			except socket.timeout:
				print("recv timeout")
				continue
			except Exception as e:
				print("receive exception:{}".format(e))
				break
		if self._flag.count(True)>=1:
			print(len(self._flag))
			return True
		else:
			return False
		
if __name__ == '__main__':
	n = ICMP()

	ip = "baidu.com"
	print(n.ping(ip))