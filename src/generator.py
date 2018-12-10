#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setting import *
import chardet

class CsvMaker:
    """
    csv解析器
    """

    @staticmethod
    def makeOneLine(filePoint):
        """
        解析单行  默认解析 文件 当前指针行

        Args:
            filePoint: csv文件指针
        """
        fp = open("../test/UIConfig.csv", "r")
        allLine = fp.read()
        fp.seek(0)
        oneLine = fp.readline()
        fp.close()
        encoding = chardet.detect(allLine)["encoding"]
        ttencoding = chardet.detect("warning: 无法自动检测编码  默认为: ")["encoding"]
        print ttencoding
        if not encoding:
            print "warning: 无法自动检测编码  默认为: ", "GB2312"
        else:
            print "自动检测编码  结果为: ", encoding
        utf8OneLine = (oneLine.decode(encoding)).encode("utf-8")

        print "一行", utf8OneLine

import sys

print sys.stdout.encoding

def main():
    CsvMaker.makeOneLine(" ")

main()