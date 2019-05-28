# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *

#�ñ��� Ÿ���� �ָ� �� �ñ����� �ڵ带 ��ȯ
def FindSigunguCode(target, SigunguString):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(SigunguString)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        #print(item.find("orgdownNm").text)
        if item.find("orgdownNm").text == target :
            #print(item.find("orgCd").text)
            return item.find("orgCd").text

sidocode = "6410000"

#http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd=6110000&ServiceKey=����Ű
#�ش� ��,���� �ñ������ �޾ƿ���
servicekey = "&ServiceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
server = "/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd="

conn = http.client.HTTPConnection("openapi.animal.go.kr")
conn.request("GET",server + sidocode + servicekey)
res = conn.getresponse()

if int(res.status) == 200 :
    SigunguString = parseString(res.read().decode('utf-8')).toprettyxml()
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()

print(SigunguString)