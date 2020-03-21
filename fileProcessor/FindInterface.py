#!/usr/bin/python3
# coding=utf-8

import os
import re
import json
import pandas as pd
import xlwt

# 功能：比较两中Java文件，确定代码调用的方法中的接口名，
# 即获取所有controller中的接口方法，找出调用统一接口工具B类方法中的接口url; 绝大部分有规则，小部分特殊处理

iaFilePath = '/Users/jyxioakai/develop/test/ServiceClient.java'
dicPath = '/Users/jyxioakai/develop/test/controller/'
json_file = '/Users/jyxioakai/develop/test/calculate_1.json'
# 调用方式
findKey = 'ServiceClient.'
# 方法名
methodKey = 'public static '
# 接口形式
faceKey = '/Server/'
# 列出所有Controller文件
file_list = os.listdir(dicPath)
ia_file = open(iaFilePath)
fo = open(json_file, 'w', encoding='UTF-8')

method_list = []
face_list = []
temp_name = ''
temp_face = ''
# 遍历所有方法名及获取其中的接口名
for line in ia_file.readlines():
    methodName = re.search(methodKey + '.*', line)
    interFace = re.search(faceKey + '.*', line)
    simple_name = ''
    if methodName is not None:
        format_str = methodName.group()
        simple_name = format_str.split(' ')[3].split('(')[0]
        if simple_name == 'getToken' or simple_name == temp_name or simple_name == 'getConceptByKeyword' \
                or simple_name == 'getHttpClient':
            continue
        # print(simple_name)
        method_list.append(simple_name)
        temp_name = simple_name
    if interFace is not None:
        format_face = interFace.group().split('\"')[0]
        if format_face == temp_face:
            continue
        # print(format_face)
        face_list.append(format_face)
        temp_face = format_face

print(len(method_list))
print(len(face_list))

method_face = {}
for index in range(0, len(method_list)):
    method_face[method_list[index]] = face_list[index]

# print(method_face)

# 遍历所有Controller文件，并找出调用上述Java文件中的方法
call_array = []
list_call_face = {}
for java_file in file_list:
    # print(java_file)
    f = open(dicPath + java_file)
    for line in f.readlines():
        result = re.search(findKey + '.*', line)
        if result is not None:
            res_str = result.group().split('(')[0]
            if res_str not in call_array and res_str != 'IaServiceClient;':
                call_array.append(res_str)
                simple_method = res_str.split('.')[1]
                if simple_method in method_face:
                    face = method_face[simple_method]
                    list_call_face[simple_method] = face
                    print(simple_method)

# print(len(call_array))
print(len(list_call_face))

# 写到json文件中
jsObj = json.dumps(list_call_face, indent=2)
fo.write(jsObj)
fo.close()

# 写入Excel
# df = pd.DataFrame()
# for line in jsObj:
#     print(line)
#     for i in line:
#         df1 = pd.DataFrame([i])
#         df = df.append(df1)

# 在excel表格的第1列写入, 不写入index
# df.to_excel('./files/calculate_1.xls', sheet_name='sheet1', startcol=0, index=False)
