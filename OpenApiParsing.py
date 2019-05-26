import urllib
import http.client
from xml.dom.minidom import *

#http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?
# #serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D
# &bgnde=20140601
# &endde=20140630
# &upkind=417000
# &state=notice
# &pageNo=1
# &numOfRows=10
# &neuter_yn=Y

server = "/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?serviceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
params = "&neuter_yn=Y"

conn = http.client.HTTPConnection("openapi.animal.go.kr")
conn.request("GET",server + params)
res = conn.getresponse()

if int(res.status) == 200 :
    XmlString = parseString(res.read().decode('utf-8')).toprettyxml()
else:
    print ("HTTP Request is failed :" + res.reason)
    print (res.read().decode('utf-8'))

conn.close()

print(XmlString)