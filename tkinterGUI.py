from tkinter import *
from tkinter import font
from tkinter import ttk

import http.client
from xml.dom.minidom import *
import urllib
from xml.etree import ElementTree

#import OpenApiParsing
import OpenSidoApi
import OpenSigunguApi

#OpenApiParsing.SearchByDate()

window = Tk()

class WarmHeart:
    def __init__(self):
        # 기본 캔버스
        self.width = 700
        self.height = 500
        self.canvas = Canvas(window, width = self.width, height = self.height, bg = "white")
        self.canvas.pack()

        # 로고 이미지
        self.LogoImage = PhotoImage(file = "WarmHeart로고.png")
        self.logo = Label(window, image = self.LogoImage)
        self.logo.place(x=25, y=10)

        # 라디오 버튼 (지역/날짜)
        RadioFrame = Frame(window)
        self.RadioVar = IntVar()
        self.localRadio = Radiobutton(RadioFrame, text='지역', variable=self.RadioVar, value=1, command=self.localRadioFunc, background='white')
        self.localRadio.grid(row=1, column=1)
        self.dayRadio = Radiobutton(RadioFrame, text='날짜', variable=self.RadioVar, value=2, command=self.localRadioFunc, background='white')
        self.dayRadio.grid(row=1, column=2)
        RadioFrame.place(x=25, y=60)
        self.prevRadioVal = 0

        # 라벨 (시/도 시/군/구, 검색 시작일 ~ 종료일 (20xxxxxx))
        tempFont = font.Font(window, size=8, weight='bold', family='Consolas')
        self.Label = Label(window, font=tempFont, text = ' ', background='white')
        self.Label.place(x=25, y=90)

        # 좌측 프레임 (리스트 박스)
        self.LeftFrameWidth = 42
        self.LeftFrameHeight = 21
        self.LeftFrame = Listbox(window, width=self.LeftFrameWidth, height=self.LeftFrameHeight, borderwidth=2,relief='ridge', background='white', selectmode="extended" )
        self.LeftFrame.place(x=25, y=140)

        # 우측 프레임
        self.RightFrameWidth = 300
        self.RightFrameHeight = 427
        self.RightFrame = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2, relief='ridge', background='white')
        self.RightFrame.place(x=375, y=55)

        # 정보/지도/하트 탭
        self.InformButton = Button(window, font=tempFont, text=" 정보 ", background="pink", command=self.RightButtonFunc)
        self.InformButton.place(x=375,y=33)
        self.MapButton = Button(window, font=tempFont, text=" 지도 ", background="pink", command=self.RightButtonFunc)
        self.MapButton.place(x=418, y=33)
        self.HeartButton = Button(window, font=tempFont, text=" 하트 ", background="pink", command=self.RightButtonFunc)
        self.HeartButton.place(x=461, y=33)

        # 검색 버튼
        self.SearchButton = Button(window, font=tempFont, text=" 검색 ", background="pink", command=self.SearchButtonFunc)
        self.SearchButton.place(x=280, y=110)

        window.mainloop()

    def localRadioFunc(self):   # 라디오 버튼 처리 함수
        if self.RadioVar.get()==1:
            if self.prevRadioVal == 2:
                self.startEntry.destroy()
                self.endEntry.destroy()
            self.Label['text'] = "시/도       시/군/구"
            sidos=["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시"]    #시도 받아오자
            self.startCombo=ttk.Combobox(window, width=5, values=sidos)
            self.startCombo.place(x=25, y=110)
            self.startCombo.current(0)
            #sigungus = self.MakeSigunguList(self.FindSidoCode(self.startCombo.get()))
            #OpenSidoApi.FindSidoCode("서울특별시")#self.startCombo.get())

            self.endCombo = ttk.Combobox(window, width=5)#, command = self.MakeEndList)
            self.endCombo.place(x=100, y=110)
            self.prevRadioVal = 1

        elif self.RadioVar.get()==2:
            if self.prevRadioVal == 2:
                self.startCombo.destroy()
                self.endCombo.destroy()
            self.Label['text'] = "검색 시작일 ~ 종료일 (20xxxxxx)"
            self.EntryWidth = 8
            self.startEntry = Entry(window, width=self.EntryWidth)
            self.endEntry = Entry(window, width=self.EntryWidth)
            self.startEntry.place(x=25, y=110)
            self.endEntry.place(x=105, y=110)
            self.prevRadioVal = 2

    def SearchButtonFunc(self):
        if self.RadioVar.get()==1:
            pass
        elif self.RadioVar.get()==2:
            pass

    def RightButtonFunc(self):
        pass

    def MakeEndList(self):
        self.endCombo['values'] = OpenSigunguApi.MakeSIgunguList(OpenSidoApi.FindSidoCode(self.startCombo.get()))

    def Printdd(self):
        print("dasfsa")

    def MakeSigunguList(self, sidocode):
        #sidocode = "6410000"
        # http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd=6110000&ServiceKey=서비스키
        # 해당 시,도의 시군구목록 받아오기
        servicekey = "&ServiceKey=QNsNyJUh2SBMrJ6%2BBGKW54UWg1l3DmN0l0%2F7DjXC%2BLSrzbdKZaHHODRMXS1CQvallUQqH5032TefPXykbUq%2BTQ%3D%3D"
        server = "/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd="

        conn = http.client.HTTPConnection("openapi.animal.go.kr")
        conn.request("GET", server + sidocode + servicekey)
        res = conn.getresponse()

        # 시군구 리스트 만들어서 반환


WarmHeart()

