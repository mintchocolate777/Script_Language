# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *

#http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sido?ServiceKey=서비스키

def FindSidoCode(target, SidoString):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(SidoString)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        print(item.find("orgdownNm").text)
        if item.find("orgdownNm").text == target :
            print(item.find("orgCd").text)
            return item.find("orgCd").text

server = "/openapi/service/rest/abandonmentPublicSrvc/sido?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"

conn = http.client.HTTPConnection("openapi.animal.go.kr")
conn.request("GET",server)
res = conn.getresponse()

if int(res.status) == 200 :
    SidoString = parseString(res.read().decode('utf-8')).toprettyxml()
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()

print(SidoString)

target = "경기도"

#시도 이름을 넣으면 해당 시,도의 코드를 반환
sidocode = FindSidoCode(target,SidoString)

print(sidocode)