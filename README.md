# AliothAsset
内网资产管理与外网自动发现工具

# 数据库
## table asset_record
id  
first_time  数据第一次记录时间   
update_time  数据上一次更新时间  
server_type  服务器类型，物理机，虚拟机  
deployment_type 部署类型  在线，库存，借出，报废  
server_name  服务器名称   
server_os  服务器操作系统  
service   运行服务  apache->80  
local_ip  内网ip  
local_port  内网开放的端口  
global_ip    对外公网ip  可为空  
global_port  公网端口  可为空  
configuration   服务器配置 CPU等  
eth1_mac    网卡mac地址  
eth2_mac    网卡mac地址  
isAlive   是否在线  
manager  管理员   
manager_email  管理员email  
manager_phone   管理员电话  
maintainer    运维人员  
maintainer_phone   运维人员电话  
maintainer_email  运维人员邮件  
desc  其他  
