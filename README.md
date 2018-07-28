# AliothAsset
## 内网资产管理与外网发现工具  
**该工具前端基于惊蛰扫描器，后端分为三个模块，分别是内网资产管理模块，公网服务器发现模块和资产分析模块**


# 数据库
## table asset_record
该表用于存储资产的详细信息
## table asset_discover
该表用于存储使用扫描器在公网上发现的资产信息

# 使用
## 创建数据库
```sql
create database asset
```
**修改配置文件**
```python
#utils/config.py
SQLCONFIG = 'mysql://root:123456@127.0.0.1/asset'
```
**创建表**
```bash
python model/model.py
```
**启动**
```bash
python asset.py
```