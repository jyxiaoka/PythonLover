#!/usr/bin/python3
# coding=utf-8

# pip install cloudant  （安装couchdb py库）
import datetime
import uuid
# from urllib import parse
from cloudant.client import CouchDB

# 连接couchdb数据库
couchdb_url = 'http://127.0.0.1:4784'
couchdb_userName = 'admin'
couchdb_password = '123456'

couchClient = CouchDB(couchdb_userName, couchdb_password, url=couchdb_url, connect=True)
# 创建数据库
couchDb = couchClient.create_database('exiaresource')
if couchDb.exists():
    print('CouchDB exiaresource数据库已创建或存在！')


# 通过UUID自动生成ID
def create_uid():
    return str(uuid.uuid1()).replace('-', '')


importedCount = 0

# for bat in range(0,5):
#     dataList = []
#     for index in range(0,10):
#         document = {"id":create_uid(),"title":"这是测试的标题标题","content":"这是测试的内容啊啊啊啊对对对发递四方速递","isPart":1,
#                     "status":1,"source":"哈哈哈哈哈","html_content":"地方撒发生发顺丰发的说法的时刻范德萨借款方哈师大李开复和卡仕达开了房哈第三方",
#                     "partResourceId":"0ef55b60669c70dd53709f9abf0012e7"}
#         dataList.append(document)
#         importedCount = importedCount + len(dataList)
#     # 批量插入到CouchDB
#     couchDb.bulk_docs(dataList)
#     print('导入：'+str(len(dataList))+"条数据！")

# 关闭连接
couchClient.disconnect()

if __name__ == '__main__':
    print(create_uid())
