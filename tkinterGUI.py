from tkinter import *
from tkinter import font
from tkinter import ttk

import http.client
from xml.dom.minidom import *
import urllib
from xml.etree import ElementTree

import OpenApiParsing
import OpenSidoApi
import OpenSigunguApi

#OpenApiParsing.SearchByDate()

window = Tk()
curAnimalList = []


class AnimalList:
    def __init__(self, iter):
        if iter.find('kindCd')!=None:
            self.kind = iter.find('kindCd').text
        if iter.find('age') != None:
            self.age = iter.find("age").text
        if iter.find('sexCd')!=None:
            self.gender = iter.find("sexCd").text
        if iter.find('colorCd')!=None:
            self.color = iter.find("colorCd").text
        if iter.find('weight')!=None:
            self.weight = iter.find("weight").text
        if iter.find('specialMark')!=None:
            self.specialMark = iter.find("specialMark").text
        if iter.find('happenPlace')!=None:
            self.happenPlace = iter.find("happenPlace").text
        if iter.find('happenDt')!=None:
            self.happenDt = iter.find("happenDt").text
        if iter.find('neuterYn')!=None:
            self.neuterYn = iter.find("neuterYn").text
        if iter.find('careNm')!=None:
            self.careNm = iter.find("careNm").text
        if iter.find('careAddr')!=None:
            self.careAddr = iter.find("careAddr").text
        if iter.find('chargeNm')!=None:
            self.chargeNm = iter.find("chargeNm").text
        if iter.find('careTel')!=None:
            self.careTel = iter.find("careTel").text


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
        self.LeftFrame = Listbox(window, width=self.LeftFrameWidth, height=self.LeftFrameHeight, borderwidth=2,relief='ridge', background='white', selectmode="single")
        self.LeftFrame.place(x=25, y=140)

        # 우측 프레임
        self.RightFrameWidth = 300
        self.RightFrameHeight = 427
        self.RightFrame = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2, relief='ridge', background='white')
        self.RightFrame.place(x=375, y=55)
        self.RenderText = []
        for i in range(13):
            self.RenderText.append(Label(self.RightFrame, background='white'))
            self.RenderText[i].place(x=0,y=i*20)
            self.RenderText[i]['text'] = ""
        #self.RenderText.configure(state='disabled')

        # 정보/지도/하트 탭
        self.InformButton = Button(window, font=tempFont, text=" 정보 ", background="pink", command=self.InformButtonFunc)
        self.InformButton.place(x=375,y=33)
        self.MapButton = Button(window, font=tempFont, text=" 지도 ", background="pink", command=self.MapButtonFunc)
        self.MapButton.place(x=418, y=33)
        self.HeartListButton = Button(window, font=tempFont, text=" 하트 ", background="pink", command=self.HeartListButtonFunc)
        self.HeartListButton.place(x=461, y=33)

        # 이미지/하트/이메일 버튼
        self.imageList = []
        self.imageList.append(PhotoImage(file='Image/ImageButton.png'))
        self.ImageButton = Button(window, font=tempFont, image = self.imageList[0], background="pink",command = self.ImageButtonFunc)
        self.ImageButton.place(x=610, y=33)
        self.imageList.append(PhotoImage(file='Image/EmptyHeartButton.png'))
        self.imageList.append(PhotoImage(file='Image/RedHeartButton.png'))
        self.HeartButton = Button(window, font=tempFont, image=self.imageList[1], background="pink",command = self.HeartButtonFunc)
        self.HeartButton.place(x=630, y=33)
        self.imageList.append(PhotoImage(file='Image/MailButton.png'))
        self.MailButton = Button(window, font=tempFont, image=self.imageList[3], background="pink")
        self.MailButton.place(x=650, y=33)

        # 검색 버튼
        self.SearchButton = Button(window, font=tempFont, text=" 검색 ", background="pink", command=self.SearchButtonFunc)
        self.SearchButton.place(x=280, y=110)

        self.i = 0
        self.upr_cd = "0" # 시도
        self.org_cd = "0" # 시군구
        window.mainloop()

    def localRadioFunc(self):   # 라디오 버튼 처리 함수
        if self.RadioVar.get()==1:
            if self.prevRadioVal == 2:
                self.startEntry.destroy()
                self.endEntry.destroy()
            self.Label['text'] = "시/도       시/군/구"
            sidos=["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시"
                   ,"세종특별자치시", "대전광역시", "울산광역시","경기도","강원도","충청북도"]    #시도 받아오자
            self.startCombo=ttk.Combobox(window, width=5, values=sidos)
            self.startCombo.place(x=25, y=110)

            self.endCombo = ttk.Combobox(window, width=5)
            self.endCombo.place(x=100, y=110)

            self.sidoButton = Button(window, text=" ", background = "pink", command = self.sidoButtonFunc)
            self.sidoButton.place(x=83,y=110)
            self.prevRadioVal = 1

        elif self.RadioVar.get()==2:
            if self.prevRadioVal == 1:
                self.startCombo.destroy()
                self.endCombo.destroy()
                self.sidoButton.destroy()
            self.Label['text'] = "검색 시작일 ~ 종료일 (20xxxxxx)"
            self.EntryWidth = 8
            self.startEntry = Entry(window, width=self.EntryWidth)
            self.endEntry = Entry(window, width=self.EntryWidth)
            self.startEntry.place(x=25, y=110)
            self.endEntry.place(x=105, y=110)
            self.prevRadioVal = 2

    def sidoButtonFunc(self):
        sigungus = []
        self.upr_cd = OpenSidoApi.FindSidoCode(self.startCombo.get())
        sigungus = OpenSigunguApi.MakeSIgunguList(self.upr_cd)
        self.endCombo['values'] = sigungus

    def SearchButtonFunc(self):
        if self.RadioVar.get()==1:
            self.org_cd = OpenSigunguApi.FindSigunguCode(self.endCombo.get(),self.upr_cd)
            tree = OpenApiParsing.SearchBySigungu(self.upr_cd, self.org_cd)
            itemElements = tree.getiterator("item")
            self.LeftFrame.delete(0, self.i)
            self.i = 0
            curAnimalList.clear()
            for item in itemElements:
                curAnimalList.append(AnimalList(item))
                kind = item.find("kindCd")
                self.LeftFrame.insert(self.i, kind.text)
                self.i += 1

        elif self.RadioVar.get()==2:
            bgnde = self.startEntry.get()
            endde = self.endEntry.get()
            tree = OpenApiParsing.SearchByDate(bgnde,endde)
            itemElements = tree.getiterator("item")
            self.LeftFrame.delete(0,self.i)
            self.i = 0
            curAnimalList.clear()
            for item in itemElements:
                curAnimalList.append(AnimalList(item))
                kind = item.find("kindCd")
                self.LeftFrame.insert(self.i,kind.text)
                self.i += 1

    def InformButtonFunc(self):
        selection = self.LeftFrame.curselection()
        s = selection[0]

        self.RenderText[0]['text'] = "품종 " + curAnimalList[s].kind
        self.RenderText[1]['text'] = "성별 " + curAnimalList[s].gender
        self.RenderText[2]['text'] = "털색 " + curAnimalList[s].color
        self.RenderText[3]['text'] = "체중 " + curAnimalList[s].weight
        self.RenderText[4]['text'] = "나이 " + curAnimalList[s].age
        self.RenderText[5]['text'] = "발견 " + curAnimalList[s].happenPlace
        self.RenderText[6]['text'] = "특징 " + curAnimalList[s].specialMark
        self.RenderText[7]['text'] = "접수 " + curAnimalList[s].happenDt
        self.RenderText[8]['text'] = "중성화여부 " + curAnimalList[s].neuterYn
        self.RenderText[9]['text'] = "보호소이름 " + curAnimalList[s].careNm
        self.RenderText[10]['text'] = "보호장소 " + curAnimalList[s].careAddr
        self.RenderText[11]['text'] = "담당자 " + curAnimalList[s].chargeNm
        self.RenderText[12]['text'] = "연락처 " + curAnimalList[s].careTel

    def MapButtonFunc(self):
        pass

    def HeartListButtonFunc(self):
        pass

    def ImageButtonFunc(self):
        pass

    def HeartButtonFunc(self):
        pass

    def MailButtonFunc(self):
        pass



WarmHeart()

