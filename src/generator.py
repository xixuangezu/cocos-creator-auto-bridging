#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setting import *
import chardet
import csv

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
            encoding: 转换成编码 默认
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

def main():
    with open("../test/UIConfig.csv", "r") as fp:
        print CsvMaker.makeDict(fp, ["tt0", "tt1", "tt2"], "utf-8")[0]["tt0"]

main()