#!/usr/bin/python3
# coding=utf-8

# pip install cloudant  （couchdb py库
# python -m easy_install pymongo  （mongodb py库）

import datetime
import uuid
from urllib import parse
from cloudant.client import CouchDB
import pymongo
import threading
import time


def getMongoDbCol():
    # 连接MongoDB数据库进行查询数据
    # mongo_passwd = "Mongodb@123456"
    mongo_passwd = "123456"
    # 对密码先进行编码
    mongo_passwd = parse.quote(mongo_passwd)
    mongo_user = "admin"
    mango_uri = 'mongodb://%s:%s@%s:%s/%s' % (mongo_user, mongo_passwd, "localhost", "27017", "exiaresource")

    mongoclient = pymongo.MongoClient(mango_uri)
    mongodb = mongoclient["exiaresource"]

    # wcmmetatablespecialpolicy 查询专项政策库集合
    mongoCollection = mongodb["wcmmetatablespecialpolicy"]
    return mongoCollection


def getCouchDb():
    # 连接CouchDB数据导入数据
    # 本地CouchDB数据库
    # couchdb_url = 'http://127.0.0.1:5984'
    # couchdb_userName = 'root'
    # couchdb_password = 'root123qwe'

    # 远程数据库
    couchdb_url = 'http://localhost:5984'
    couchdb_userName = 'admin'
    couchdb_password = '123456'

    couchClient = CouchDB(couchdb_userName, couchdb_password, url=couchdb_url, connect=True)
    # 创建数据库
    couchDb = couchClient.create_database('exiaresource')
    if couchDb.exists():
        print('CouchDB exiaresource数据库已创建或存在！')

    return couchDb


# 通过UUID自动生成ID
def create_uid():
    return str(uuid.uuid1()).replace('-', '')


def beginImportData():
    mongoCollection = getMongoDbCol()
    couchDb = getCouchDb()
    # 分页查询
    limitCount = 1000
    # totalCount = 40
    totalCount = mongoCollection.estimated_document_count()
    totalCount = 2000
    print('mongodb数据总数：' + str(totalCount))
    totalPage = totalCount / limitCount
    totalPage = int(totalPage) + 1

    importedCount = 0

    for page in range(1, totalPage):
        print('查询MongoDB第' + str(page) + '页数据')
        dataList = []
        pageResult = mongoCollection.find().skip((page - 1) * limitCount).limit(limitCount)
        for document in pageResult:
            # 导入数据到CouchdDB
            # 处理_id，自动生成uuid
            document['_id'] = create_uid()
            # 如果有_class 则移除该字段
            if '_class' in document:
                del document['_class']
            # 处理时间格式
            for key in document:
                if isinstance(document[key], datetime.datetime):
                    document[key] = document[key].strftime("%Y-%m-%d %H:%M:%S")
                # 处理扩展属性
                if key == 'extendAttrs':
                    extendAttrsArr = document[key]
                    for extObj in extendAttrsArr:
                        for extKey in extObj:
                            if isinstance(extObj[extKey], datetime.datetime):
                                extObj[extKey] = extObj[extKey].strftime("%Y-%m-%d %H:%M:%S")
                # 处理文件fileInfos
                if 'fileInfos' == key:
                    fileInfosArr = document[key]
                    for fileObj in fileInfosArr:
                        for fileKey in fileObj:
                            if '_id' == fileKey:
                                fileObj['_id'] = create_uid()
                            if isinstance(fileObj[fileKey], datetime.datetime):
                                fileObj[fileKey] = fileObj[fileKey].strftime("%Y-%m-%d %H:%M:%S")

            # print(document)
            # 单个插入文档到couchdb
            # doc = couchDb.create_document(document)
            # if doc.exists():
            # importedCount = importedCount + 1
            # 添加处理后的document到list
            dataList.append(document)
        # 批量插入到CouchDB
        print("正在批量导入数据...")
        couchDb.bulk_docs(dataList)
        importedCount = importedCount + len(dataList)
    print('导入数据完成，共导入：' + str(importedCount))


# 执行查询和导入
# beginImportData()


# 多线程方式执行导入
class importThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print("开始执行线程：" + self.name)
        threadImport(self.name, self.delay)
        print("退出线程：" + self.name)


def threadImport(threadName, delay):
    time.sleep(delay)
    # 导入数据
    beginImportData()
    print("%s: %s" % (threadName, time.ctime(time.time())))


# 启动线程执行
myThread1 = importThread("Thread-1", 3)
# myThread2 = importThread("Thread-2", 3)
myThread1.start()
# myThread2.start()
myThread1.join()
# myThread2.join()

print("结束，退出线程。")

if __name__ == '__main__':
    print(create_uid())
