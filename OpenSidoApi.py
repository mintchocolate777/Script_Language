# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *

def FindSidoCode(target):
    server = "/openapi/service/rest/abandonmentPublicSrvc/sido?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"

    while(True):
        conn = http.client.HTTPConnection("openapi.animal.go.kr")
        conn.request("GET", server)
        res = conn.getresponse()

        import spam
        if spam.myf(res.status):
            SidoString = parseString(res.read().decode('utf-8')).toprettyxml()
            break

        conn.close()

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(SidoString)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        if item.find("orgdownNm").text == target :
            return item.find("orgCd").text

FindSidoCode("서울특별시")