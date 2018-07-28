#!/usr/bin/env python
# __Author__:cmustard

import subprocess
import sys
import os
import time
import json
import datetime
import nmap


from tempfile import NamedTemporaryFile
from utils.comm import get_logger


logger = get_logger()

class Nmap(object):
    '''nmap scan'''
    def __init__(self):
        pass

    def scan(self,host,ports):
        nm = nmap.PortScanner()
        if sys.platform == "win32":
            result = nm.scan(hosts=host,ports=ports,arguments="-sS",sudo=False)["scan"]
        #result = {'192.168.199.1': {'hostnames': [{'name': 'Hiwifi.lan', 'type': 'PTR'}], 'addresses': {'ipv4': '192.168.199.1', 'mac': 'D4:EE:07:58:D8:C2'}, 'vendor': {'D4:EE:07:58:D8:C2': 'Hiwifi'}, 'status': {'state': 'up', 'reason': 'arp-response'}, 'tcp': {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 81: {'state': 'open', 'reason': 'syn-ack', 'name': 'hosts2-ns', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 82: {'state': 'open', 'reason': 'syn-ack', 'name': 'xfer', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 83: {'state': 'open', 'reason': 'syn-ack', 'name': 'mit-ml-dev', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 443: {'state': 'open', 'reason': 'syn-ack', 'name': 'https', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'microsoft-ds', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}}}}
        elif sys.platform == "linux":
            result = nm.scan(hosts=host, ports=ports, arguments="-sS", sudo=True)["scan"]
        else:
            logger.critical("Not support the platform!!!")
            print("Not support the platform!!!")
        try:
            result = result[host]
        except Exception as e:
            logger.error(str(e))
            return {}
        hostnames = ""
        for hostname in result['hostnames']:
            hostnames += "name->{}\t\t type->{}\t\t\n".format(hostname["name"],hostname['type'])

        address= ""
        addresses = result['addresses']
        if addresses.get("ipv4") is not None:
            address = "ip->{}\t\t mac->{}\t\t\n".format(addresses['ipv4'],addresses['mac'])
        status = "hoststatus->{}\n".format(result["status"]['state'])

        ports = []
        try:
            tcp_ports = []
            tcp_ports = list(result.get("tcp").keys())
            ports.extend(tcp_ports)
        except AttributeError as e:
            pass
        try:
            udp_ports = []
            udp_ports= list(result.get('udp').keys())
            ports.extend(udp_ports)
        except AttributeError as e:
            pass

        #  83: {'state': 'open', 'reason': 'syn-ack', 'name': 'mit-ml-dev', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}
        services = "TCP:\n"
        if len(tcp_ports)>0:
            for t_port in tcp_ports:
                services += "port->{}\n\tstate->{}\n\tname->{}\n\tproduct->{}\n\tversion->{}\n\textrainfo->{}\n\tconf->{}\n\tcpe->{}\n{}\n".format(
                    str(t_port), result.get("tcp")[t_port]['state'],result.get("tcp")[t_port]['name'],result.get("tcp")[t_port]['product'],result.get("tcp")[t_port]['version'],
                    result.get("tcp")[t_port]['extrainfo'],result.get("tcp")[t_port]['conf'],result.get("tcp")[t_port]['cpe'],'*'*50
                )
        services += "UDP:\n"
        if len(udp_ports)>0:
            for u_port in udp_ports:
                services += "port->{}\n\tstate->{}\n\tname->{}\n\tproduct->{}\n\tversion->{}\n\textrainfo->{}\n\tconf->{}\n\tcpe->{}\n{}\n".format(
                    str(u_port),result.get("tcp")[u_port]['state'], result.get("tcp")[u_port]['name'],
                    result.get("tcp")[u_port]['product'], result.get("tcp")[u_port]['version'],
                    result.get("tcp")[u_port]['extrainfo'], result.get("tcp")[u_port]['conf'],
                    result.get("tcp")[u_port]['cpe'],"*"*50
                )

        info = "{}\n{}\n{}\n{}\n".format(hostnames,address,status,services)
        services = "{}\n".format(services)
        result['info'] = info # scan result
        result['service'] = services # service info
        result["port"] = ports  # port info
        print(result)
        return result




class Masscan(object):
    def __init__(self):
        self.__exec_path()
        if self.exec_path == None:
            print("Critical Error!!!")
            return

    def __exec_path(self):
        if sys.platform == 'win32':
            paths = ["ext/windows/masscan.exe","../ext/windows/masscan.exe","../../ext/windows/masscan.exe"]
        elif sys.platform == "linux":
            paths = ["ext/linux/masscan", "../ext/linux/masscan", "../../ext/linux/masscan","masscan"]
        else:
            logger.critical("Not support the platform!!!")
            self.exec_path = None

        for path in paths:
            self.exec_path = os.path.join(os.getcwd(),path)
            if os.path.exists(self.exec_path):
                break
            else:
                continue
        else:
            raise os.error("execute file path is not right")



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
            dict_json['open'] = set()
            for data_json in data_jsons:
                dict_json['time'] = datetime.datetime.fromtimestamp(int(data_json['timestamp']))

                for item in data_json['ports']:
                    print(item)
                    if item.get("service"):
                        dict_json["banner"] += u"名称->{}\t 签名->{}\n".format(item['service']['name'],item['service']['banner'])
                    else:
                        dict_json['info'] += u"端口->{}\t 协议->{}\t 状态->{}\n".format(item.get('port'), item.get('proto'),
                                                                                 item.get("status"))
                        dict_json['open'].add(item.get("port"))

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
            if sys.platform == 'win32':
                exec_args = [self.exec_path,"-oJ", temp_file.name,"-sS","-Pn", "--banners"]
            elif sys.platform =="linux":
                exec_args = [self.exec_path,"-oJ", temp_file.name,"-sS","-Pn", "--banners"]
            else:
                logger.critical("Not support the platform!!!")
                print("Not support the platform!!!")
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
            result_dict = self.__json_parser(content=data)
            temp_file.close()
            end_time = time.time()
            speed_time = end_time-start_time
            print("speed time %ss"% speed_time)
        except Exception as e:
            print(e)
            logger.debug(str(e))
            result_dict = {}
            temp_file.close()
        return result_dict

    def test(self):
        print(self.__json_parser(jsonpath="1.xml"))

if __name__ == '__main__':
    n = Nmap()
    n.scan("192.168.199.1","1-1080")
    # m = Masscan()
    # print(m.scan("-p1-1080","--rate", "1000","192.168.199.1"))
    # # # m.test()