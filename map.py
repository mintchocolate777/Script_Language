import folium
from googlemaps import *

#AIzaSyAxLxOspCCw6v52W-K593bqAdgIBV351M8 구글 API KEY
gmaps = Client(key = "AIzaSyAxLxOspCCw6v52W-K593bqAdgIBV351M8")
sample = gmaps.geocode('대한민국 경기도 시흥시 산기대학로 237', language = 'ko')
lat = sample[0]['geometry']['location']['lat']
lng = sample[0]['geometry']['location']['lng']
print(type(lng))
#위도 경도 지정
map_osm = folium.Map(location= [lat, lng],zoom_start=13)
#마커 지정
folium.Marker([lat,lng], popup = 'MT. Hood Meadows').add_to(map_osm)
#html 파일로 저장
map_osm.save('osm.html')