#!/usr/bin/env python
# __Author__:cmustard

import nmap
import subprocess
import sys
import os
import shutil
import json
import time
from tempfile import NamedTemporaryFile
from utils.comm import get_logger


logger = get_logger()

class Nmap(object):
    '''nmap scan'''
    def __init__(self):
        pass

    def scan(self,host,ports):
        nm = nmap.PortScanner()
        result = nm.scan(hosts=host,ports=ports,arguments="-sS",sudo=True)["scan"]
        return result




class Masscan(object):
    def __init__(self):
        self.__exec_path()
        if self.exec_path == None:
            print("Critical Error!!!")
            return

    def __exec_path(self):
        if sys.platform == 'win32':
            paths = ["ext/masscan.exe","../ext/masscan.exe"]
            for path in paths:
                self.exec_path = os.path.join(os.getcwd(),path)
                if os.path.exists(self.exec_path):
                    break
                else:
                    continue
            else:
                raise os.error("execute file path is not right")
        elif sys.platform == 'linux':
            # 暂时还未写
            paths = []
            pass
        else:
            logger.critical("Not support the platform!!!")
            self.exec_path = None


    def scan(self,*args):
        temp_file = NamedTemporaryFile(delete=True,suffix=".json")
        print(temp_file.name)
        # exit(1)
        try:
            start_time = time.time()
            exec_args = [self.exec_path,"-oJ", temp_file.name,"--banners"]
            exec_args.extend(args)
            result = subprocess.check_call(exec_args)
            if result == 0:
                print("scan finish!!!")
            else:
                print("scan failed!!!")
            print(result)
            # 需要处理
            data = temp_file.read().decode("utf-8")
            print(data)
            print(json.loads(data))
            temp_file.close()
            end_time = time.time()
            speed_time = end_time-start_time
            print("speed time %ss"% speed_time)
        except Exception as e:
            print(e)
            logger.debug(str(e))
            data = ""
            temp_file.close()
        return data

if __name__ == '__main__':
    # n = Nmap()
    # n.scan("192.168.199.1","80,443,22")
    m = Masscan()
    m.scan("-p1-1080","--rate", "10000","39.106.160.62")