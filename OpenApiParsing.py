# -*- coding:cp949 -*-
import urllib
import http.client
from xml.dom.minidom import *

#http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?
# #serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D

def SearchByDate(bgnde, endde):
    server = "/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
    params = "&bgnde=" + bgnde + "&endde=" + endde

    while(True):
        conn = http.client.HTTPConnection("openapi.animal.go.kr")
        conn.request("GET", server + params)
        res = conn.getresponse()

        if int(res.status) == 200:
            XmlString = parseString(res.read().decode('utf-8')).toprettyxml()
            break

        conn.close()

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(XmlString)
    return tree

def SearchBySigungu(upr_cd, org_cd):
    server = "/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
    params = "&upr_cd=" + upr_cd + "&org_cd=" + org_cd

    conn = http.client.HTTPConnection("openapi.animal.go.kr")
    conn.request("GET", server + params)
    res = conn.getresponse()

    #if int(res.status) == 200:
    import spam
    if spam.myf(res.status):
        XmlString = parseString(res.read().decode('utf-8')).toprettyxml()
    else:
        print("HTTP Request is failed :" + res.reason)
        print(res.read().decode('utf-8'))

    conn.close()

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(XmlString)
    return tree