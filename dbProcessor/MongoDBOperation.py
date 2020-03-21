#!/usr/bin/python3
# coding=utf-8

import pymongo


mongoHost = '127.0.0.1'
mongoPort = '27017'
mclient = pymongo.MongoClient('mongodb://'+mongoHost+':'+mongoPort)
# 判断数据是否已存在
dblist = mclient.list_database_names()
if 'exiaresource' in dblist:
    print('s数据库已存在！')
# 集合操作
mdb = mclient['exiaresource']
mcollect = mdb['wcmmetatablespecialpolicy']
colllist = mdb.list_collection_names()
if 'wcmmetatablespecialpolicy' in colllist:
    print('集合已存在！')


# 查询数据
oneDoc = mcollect.find_one()
print(oneDoc)

# 查询所有
# allDoc = mcollect.find()
# for doc in allDoc:
#     print(doc)

# 查询指定字段数据
# allDoc_fields = mcollect.find({},{'_id':1233,'status':1,'isPart':0})

# 根据指定条件查询
# query = {'title':'中国共产党'}
# mDoc = mcollect.find(query)


# 限制返回条数
# mresult = mcollect.find().limit(10)

# 分页
pageResult = mcollect.find().skip(10).limit(10)

# 删除数据