#!/usr/bin/python3
# coding=utf-8

# 功能：读取日志文件中的指定文本，比如接口调用方法，
# 并写入json文件，最后可以将json文件导出到Excel表

import os
import re
import json
import pandas as pd

filePath = './files/'
filePath = filePath.encode('utf-8')
# 读取的内容，以/ExIAServer/services/开头
startKey = '/ExIAServer/services/'
# 文件后缀
ext = '.txt'
# 列出当前目录下所有文件和目录,日志文件
totalList = os.listdir(filePath)
# 输出json文件
fo = open(r'./files/calculate.json', 'w', encoding='UTF-8')

dictionary = {}
for file in totalList:
    if not file.endswith(b'.txt'):
        continue
    # print(file)
    f = open(filePath + file)
    lines = f.readlines()
    for line in lines:
        # 逐行查找要匹配的内容
        result = re.search(str(startKey) + '.*', line)
        if result is not None:
            string = result.group()
            if string is not None:
                # 截取前半部分
                new_str = string.split(' ')[0]
                print(new_str)
                if new_str in dictionary:
                    dictionary[new_str] = dictionary.get(new_str) + 1
                else:
                    dictionary[new_str] = 1
    f.close()

print(dictionary)

# 写到json内容写入Excel中
jsObj = json.dumps(dictionary, indent=2)
fo.write(jsObj)
fo.close()

# 将json写入Excel
df = pd.DataFrame()
# json对象转为Python字典
py_json = json.loads(jsObj)

dic1 = {'标题列1': ['张三', '李四'],
        '标题列2': [80, 90]
        }

excel_data = {}
columns_1 = []
columns_2 = []
for obj in py_json:
    columns_1.append(obj)
    value = py_json[obj]
    columns_2.append(value)

excel_data['接口名称'] = columns_1
excel_data['累计使用次数'] = columns_2
df1 = pd.DataFrame(excel_data)
df = df.append(df1)

# 在excel表格的第1列写入, 不写入index, header=['接口名称', '累计使用数量']
df.to_excel('./files/calculate.xls', sheet_name='sheet1', startcol=0, index=False)
