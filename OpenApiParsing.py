# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *
from xml.etree import ElementTree

#http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?
# #serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D
# &bgnde=20140601
# &endde=20140630
# &upkind=417000
# &state=notice
# &pageNo=1
# &numOfRows=10
# &neuter_yn=Y

def extractAnimalData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        kind = item.find("kindCd")
        age = item.find("age")
        gender = item.find("sexCd")
       # color = item.find("colorCd")
       # weight = item.find("weight")
       # happenPlace = item.find("happenPlace")
       # happenDt = item.find("happenDt")
       # specialMark = item.find("specialMark")
       # neuterYn = item.find("neuterYn")
       # careNm = item.find("careNm")
       # careAddr = item.find("careAddr")
       # chargeNm = item.find("chargeNm")
       # careTel = item.find("careTel")
        print(kind.text, ' ' , age.text , ' ' , gender.text)
        #if len(kind.text)>0:
        #    return {"KIND":kind.text, "AGE":age.text, "GENDER": gender.text}


bgnde = input("검색날짜 시작일을 입력하세요 (yyyymmdd)")
endde = input("검색날짜 종료일을 입력하세요 (yyyymmdd)")

server = "/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
params = "&bgnde=" + bgnde + "&endde=" + endde

conn = http.client.HTTPConnection("openapi.animal.go.kr")
conn.request("GET",server + params)
res = conn.getresponse()

if int(res.status) == 200 :
    XmlString = parseString(res.read().decode('utf-8')).toprettyxml()
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()

extractAnimalData(XmlString)
#print(XmlString)
