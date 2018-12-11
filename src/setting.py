#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 输出流编码转化
import sys
import locale
  
class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = locale.getpreferredencoding()
    def write(self, s):
        if type(s) == str:
            s = s.decode("utf-8")
        s = s.encode(self.encode_to, self.errors)
        self.target.write(s)
          
# if locale.getpreferredencoding() == 'cp936':
sys.stdout = UnicodeStreamFilter(sys.stdout)


# csv配置
class dCsv:
    startLine = 2
