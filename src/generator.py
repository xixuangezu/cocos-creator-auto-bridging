#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setting import *
import chardet
import csv
from Cheetah.Template import Template
import os

class IOEncode:
    """
    处理io编码问题
    """
    @staticmethod
    def fileEncoding(filePoint):
        """
        解析文件所用编码

        Args:
            filePoint: 文件指针
        """
        fpP = filePoint.tell()
        allLine = filePoint.read()
        filePoint.seek(fpP)

        encoding = chardet.detect(allLine)["encoding"]
        if not encoding:
            print "warning: IOEncode.fileEncoding() 无法自动检测编码  默认为: ", "GB2312", " 文件: ", filePoint.name
        
        return encoding

class CsvMaker:
    """
    csv解析器
    """

    @staticmethod
    def makeDict(filePoint, arrKeys = [], encoding = None):
        """
        解析csv为字典  并转换编码

        Args:
            filePoint: csv文件指针
            arrKeys: 字典key组成的数组
            encoding: 转换成编码 默认utf-8
        """
        encoding = encoding or "utf-8"

        fileEncoding = IOEncode.fileEncoding(filePoint)

        csvReader = csv.reader(filePoint, delimiter=',', quotechar='"')

        csvData = [[data.decode(fileEncoding).encode(encoding) 
                    for data in line]
                    for line in csvReader]

        if not (csvData[0] and csvData[0][0]):
            print "error: CsvMaker.makeDict() file: \"" + filePoint.name + "\" 没有内容"
            return [{}]

        #平齐key与var的数量
        keys = []
        for i in range(len(csvData[0])):
            if len(arrKeys) > i:
                keys.insert(i, arrKeys[i])
            else:
                keys.insert(i, "key" + str(i))

        csvDict = [dict(zip(keys, line)) for line in csvData]

        return csvDict

class TemplataMaker:
    """
    Cheetah 模板解析  附加debug提示
    """
    @staticmethod
    def Template(filePath, searchList, encoding = None):
        """
        套用模板  DEBUG_MODEL = true 附加错误提示

        Args:
            searchList: 模板变量列表 [{}]格式
            encoding: 转换成编码 默认utf-8
        """
        encoding = encoding or "utf-8"
        deriveData = ""     # 解析结果

        with open(filePath, "r") as fp:
            fileEncoding = IOEncode.fileEncoding(fp)
            # 单行检测错误
            if DEBUG_MODEL :
                oneLine = fp.readline().decode(fileEncoding).encode(encoding)
                thisLine = 0
                isError = False
                while oneLine:
                    try:
                        thisLine += 1
                        templateData = oneLine
                        oneLine = fp.readline().decode(fileEncoding).encode(encoding)
                        str(Template(templateData, searchList = searchList))
                    except:
                        print "error: TemplataMaker.Template() 解析错误. 文件: ", filePath, " 行号: ", thisLine
                        isError = True
                if isError:
                    return deriveData
                fp.seek(0)
            # 导出解析
            allLine = fp.read().decode(fileEncoding).encode(encoding)
            deriveData = str(Template(allLine, searchList = searchList))
        return deriveData

def main():
    print TemplataMaker.Template("../model/testModel.h", [{"testNum": "100"}])

main()