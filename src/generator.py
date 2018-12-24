#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setting import *
import chardet
import csv
from Cheetah.Template import Template
import Cheetah.NameMapper
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
    def makeDict(filePath, arrKeys = [], encoding = "utf-8"):
        """
        解析csv为字典  并转换编码

        Args:
            filePoint: csv文件指针
            arrKeys: 字典key组成的数组
            encoding: 转换成编码 默认utf-8
        """
        csvData = None

        with open(filePath, "r") as filePoint:
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

class TemplateMaker:
    """
    Cheetah 模板解析  附加debug提示
    """
    @staticmethod
    def Template(filePath, searchList, encoding = "utf-8"):
        """
        套用模板  DEBUG_MODEL = true 附加错误提示

        Args:
            searchList: 模板变量列表 [{}]格式
            encoding: 转换成编码 默认utf-8

        Returns:
            string 模板套用后的字符串
        """
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
                    except Cheetah.NameMapper.NotFound:
                        print "error: TemplateMaker.Template() 解析未知变量. 文件: ", filePath, " 行号: ", thisLine
                        isError = True
                    except:
                        pass
                if isError:
                    return deriveData
                fp.seek(0)

            # 导出解析
            allLine = fp.read().decode(fileEncoding).encode(encoding)
            deriveData = str(Template(allLine, searchList = searchList))
            
        return deriveData

class Generator:
    """
    解析逻辑
    """
    def __tplRootS(self, rootData):
        """
        套用模板rootS
        """
        fileName = dPath.savePath + rootData["data"]["name"] + ".lua"

        strScene =  TemplateMaker.Template("../model/SceneBox.m", [{
            "rootName": rootData["data"]["name"],
            "startLog": rootData["data"]["note"]
            }])

        with open(fileName, "w") as fp:
            fp.write(strScene)

    def __tplRootNClass(self, rootData):
        """
        套用模板root节点系列  rootP 或 rootN
        """
        # logic模板
        loginFileName = dPath.savePath + "UiLogic" + rootData["data"]["name"] + ".lua"

        strLogic =  TemplateMaker.Template("../model/LogicBox.m", [{
            "rootType": rootData["rootType"],
            "rootName": rootData["data"]["name"],
            "startLog": rootData["data"]["note"],
            "onCreateBody": rootData["LogicCreate"],
            "funcBody": rootData["LogicFunc"]
            }])

        with open(loginFileName, "w") as fp:
            fp.write(strLogic)

        # view模板
        viewFileName = dPath.savePath + "UiView" + rootData["data"]["name"] + ".lua"

        strView =  TemplateMaker.Template("../model/ViewBox.m", [{
            "rootType": rootData["rootType"],
            "rootName": rootData["data"]["name"],
            "fileName": rootData["data"]["param1"] or rootData["data"]["name"],
            "startLog": rootData["data"]["note"],
            "ctorBody": rootData["ViewCtor"],
            "funcBody": rootData["ViewFuncGet"] + rootData["ViewFuncCall"]
            }])

        with open(viewFileName, "w") as fp:
            fp.write(strView)

    def __tplNode(self, rootData, lineData):
        """
        套用模板cc.Node
        """
        rootData["ViewCtor"] += TemplateMaker.Template("../model/ViewCtor.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"]
            }])
        rootData["ViewFuncGet"] += TemplateMaker.Template("../model/ViewFunc.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"],
            "funcType": "getFunc",
            "rootName": rootData["data"]["name"]
            }])

        rootData["LogicCreate"] += TemplateMaker.Template("../model/LogicCreate.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"]
            }])

    def __tplBtn(self, rootData, lineData):
        """
        套用模板cc.Node
        """
        rootData["ViewCtor"] += TemplateMaker.Template("../model/ViewCtor.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"]
            }])
        rootData["ViewFuncGet"] += TemplateMaker.Template("../model/ViewFunc.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"],
            "funcType": "getFunc",
            "rootName": rootData["data"]["name"]
            }])
        rootData["ViewFuncCall"] += TemplateMaker.Template("../model/ViewFunc.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"],
            "funcType": "callFunc",
            "rootName": rootData["data"]["name"]
            }])

        rootData["LogicCreate"] += TemplateMaker.Template("../model/LogicCreate.m", [{
            "nodeType": lineData["type"],
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"]
            }])
        rootData["LogicFunc"] += TemplateMaker.Template("../model/LogicFunc.m", [{
            "nodeName": lineData["name"],
            "nodeLog": lineData["note"],
            "rootName": rootData["data"]["name"]
            }])

    def __saveRoot(self, rootData):
        """
        分发至rootData保存模板
        """
        listTplFun = {
            "rootS": self.__tplRootS,
            "rootP": self.__tplRootNClass,
            "rootN": self.__tplRootNClass
            }

        if rootData.has_key("rootType"):
            listTplFun[rootData["rootType"]](rootData)
            print "root: ", rootData["data"]["name"], " ", rootData["data"]["note"], " 保存成功"

    def generate_code(self):
        """
        解析全文件

        lineData  {"type", "name", "note", "voice"}

        rootData  {"ViewCtor", "ViewFuncGet", "ViewFuncCall", "LogicCreate", "LogicFunc", 
                   "rootType", "data"{"type", "name", "note", "voice"}}
        """
        # csv解析
        csvData =  CsvMaker.makeDict(dPath.csvPath, ["type", "name", "note", "voice", "param1"])
        for idx in range(dCsv.startLine):
            csvData.pop(0)

        # 类型分发
        rootData = {}
        listTplFun = {
            "rootS": "func",
            "rootP": "func",
            "rootN": "func",
            "node": self.__tplNode,
            "btn": self.__tplBtn
            }

        # 分行解析
        for line in csvData:

            if not listTplFun.has_key(line["type"]):
                 print "error: 解析错误: 节点 ", line["name"], " 类型非法"
                 return

            if line["type"] == "rootS" or line["type"] == "rootP" or line["type"] == "rootN":
                # 保存
                self.__saveRoot(rootData)
                # 新建rootData
                rootData = {
                    "ViewCtor": "",
                    "ViewFuncGet": "",
                    "ViewFuncCall": "",
                    "LogicCreate": "",
                    "LogicFunc": "",
                    "rootType": line["type"],
                    "data": line
                }
                print "解析开始:", line["type"], ": ", line["name"], " ", line["note"]
            else:
                # 解析节点
                if not rootData.has_key("rootType"):
                    print "error: 解析错误: 节点 ", line["name"], " 之前 没有设置root节点"
                    return
                listTplFun[line["type"]](rootData, line)
        # 结尾保存
        self.__saveRoot(rootData)

def main():
    generator = Generator()
    generator.generate_code()

main()