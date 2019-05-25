import urllib
import http.client

conn = http.client.HTTPConnection("openapi.animal.go.kr:80")
conn.request("GET","/openapi/service/rest/abandonmentPublicSrvc?_wadl&type=xml")
req = conn.getresponse()
print(req.status,req.reason)
print(req.read().decode('utf-8'))
