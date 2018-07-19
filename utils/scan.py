#!/usr/bin/env python
# __Author__:cmustard

import subprocess

import nmap
from .model import *

class Nmap(object):
    '''nmap scan'''
    def __init__(self):
        pass

    def scan(self,host,ports):
        nm = nmap.PortScanner()
        result = nm.scan(hosts=host,ports=ports,arguments="-sS",sudo=True)["scan"]
        return result




class Mascan(object):
    pass

if __name__ == '__main__':
    n = Nmap()
    n.scan("192.168.199.1","80,443,22")