#!/usr/bin/env python
# __Author__:cmustard

import nmap
import subprocess
import sys
import os
import time
import json
import datetime
import xml.etree.ElementTree as ET


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
            paths = ["ext/windows/masscan.exe","../ext/windows/masscan.exe"]
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

    def __json_parser(self,**kwargs):
        dict_json = {}
        if kwargs.get("jsonpath"):
            with open(kwargs.get("jsonpath"),"r") as f:
                raw_data = f.read()
        elif kwargs.get("content"):
            raw_data = kwargs.get("content")
        else:
            return None
        raw_data = raw_data.replace(" ", "").replace("\n", "")[:-2]

        raw_data = "{}]".format(raw_data)
        try:
            data_jsons = json.loads(raw_data)
            dict_json['info'] = ""
            dict_json['banner'] = ""
            for data_json in data_jsons:
                dict_json['time'] = datetime.datetime.fromtimestamp(int(data_json['timestamp']))

                for item in data_json['ports']:
                    print(item)
                    if item.get("service"):
                        dict_json["banner"] += u"名称->{}\t 签名->{}\n".format(item['service']['name'],item['service']['banner'])
                    else:
                        dict_json['info'] += u"端口->{}\t 协议->{}\t 状态->{}\n".format(item['port'], item['proto'],
                                                                                 item.get("status"))

        except Exception as e:
            logger.critical(str(e))
            return None
        return dict_json

    def scan(self,*args):
        temp_file = NamedTemporaryFile(delete=True,suffix=".xml")
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
            result_dict = self.__json_parser(content=data)
            temp_file.close()
            if result_dict is not None:
                with open("1.json","w") as f:
                    f.write(result_dict['info'])
                    f.write(result_dict['banner'])
            else:
                pass
            end_time = time.time()
            speed_time = end_time-start_time
            print("speed time %ss"% speed_time)
        except Exception as e:
            print(e)
            logger.debug(str(e))
            data = ""
            temp_file.close()
        return data

    def test(self):
        print(self.__json_parser(jsonpath="1.xml"))

if __name__ == '__main__':
    # n = Nmap()
    # n.scan("192.168.199.1","80,443,22")
    m = Masscan()
    m.scan("-p1-1080","--rate", "10000","39.106.160.62")
    # m.test()