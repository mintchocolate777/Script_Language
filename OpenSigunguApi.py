# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *

def MakeSIgunguList(sidocode):
    # http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd=6110000&ServiceKey=서비스키
    # http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd=6110000&ServiceKey=서비스키
    # 해당 시,도의 시군구목록 받아오기
    servicekey = "&ServiceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
    server = "/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd="

    conn = http.client.HTTPConnection("openapi.animal.go.kr")
    conn.request("GET", server + sidocode + servicekey)
    res = conn.getresponse()

    import spam
    if spam.myf(res.status):
        SigunguString = parseString(res.read().decode('utf-8')).toprettyxml()
    else:
        print("HTTP Request is failed :" + res.reason)
        print(res.read().decode('utf-8'))

    conn.close()

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(SigunguString)
    itemElements = tree.getiterator("item")
    sigungulist = []
    for item in itemElements:
        sigunguname = item.find("orgdownNm").text
        sigungulist.append(sigunguname)

    return sigungulist

#시군구 타겟을 주면 그 시군구의 코드를 반환
def FindSigunguCode(target, sidocode):
    servicekey = "&ServiceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
    server = "/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd="
    while(True) :
        conn = http.client.HTTPConnection("openapi.animal.go.kr")
        # 리퀘스트에서 문제생김
        str = server+sidocode+servicekey
        conn.request("GET", str)
        res = conn.getresponse()
        if int(res.status) == 200:
            SigunguString = parseString(res.read().decode('utf-8')).toprettyxml()
            break

        conn.close()

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(SigunguString)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        if item.find("orgdownNm").text == target :
            return item.find("orgCd").text