from tkinter import *
from tkinter import font
from tkinter import ttk

import http.client
from xml.dom.minidom import *

from io import BytesIO # 이미지
import urllib
import urllib.request #이미지
from PIL import Image,ImageTk # 이미지

from xml.etree import ElementTree

import OpenApiParsing
import OpenSidoApi
import OpenSigunguApi
import gmail
from googlemaps import *


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
        if iter.find('popfile') != None:
            self.popfile = iter.find("popfile").text

class WarmHeart:
    state = "Inform"
    HeartList = []
    def __init__(self):
        # 기본 캔버스
        window.title("WarmHeart")
        self.width = 700
        self.height = 500
        self.canvas = Canvas(window, width = self.width, height = self.height, bg = "white")
        self.canvas.pack()

        # 로고 이미지
        self.LogoImage = PhotoImage(file = "Image/WarmHeart로고.png")
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
        self.frameList = []
        self.RightFrameWidth = 300
        self.RightFrameHeight = 427
        self.frameList.append(Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2, relief='ridge', background='white')) # 정보
        self.frameList.append(Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2, relief='ridge', background='white')) # 지도
        self.frameList.append(
            Listbox(window, width=self.LeftFrameWidth, height=self.LeftFrameHeight+5, borderwidth=2, relief='ridge',
                    background='white', selectmode="single"))  # 하트
        self.frameList[0].place(x=375, y=55)
        self.RenderText = []
        for i in range(14):
            self.RenderText.append(Label(self.frameList[0], background='white'))
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

        # 그래프/이미지/하트/이메일 버튼
        self.imageList = []
        self.imageList.append(PhotoImage(file='Image/ImageButton.png'))
        self.imageList.append(PhotoImage(file='Image/EmptyHeartButton.png'))
        self.imageList.append(PhotoImage(file='Image/RedHeartButton.png'))
        self.imageList.append(PhotoImage(file='Image/MailButton.png'))
        self.imageList.append(PhotoImage(file='Image/GraphButton.png'))
        self.GraphButton = Button(window, font=tempFont, image=self.imageList[4], background="pink",
                                  command=self.GraphButtonFunc)
        self.GraphButton.place(x=590, y=33)
        self.ImageButton = Button(window, font=tempFont, image=self.imageList[0], background="pink",
                                  command=self.ImageButtonFunc)
        self.ImageButton.place(x=610, y=33)
        self.HeartButton = Button(window, font=tempFont, image=self.imageList[1], background="pink",command = self.HeartButtonFunc)
        self.HeartButton.place(x=630, y=33)

        self.MailButton = Button(window, font=tempFont, image=self.imageList[3], background="pink", command = self.MailButtonFunc)
        self.MailButton.place(x=650, y=33)

        # 검색 버튼
        self.SearchButton = Button(window, font=tempFont, text=" 검색 ", background="pink", command=self.SearchButtonFunc)
        self.SearchButton.place(x=280, y=110)

        self.i = 0
        self.Hearti = 0
        self.HeartSelect = None
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
        # 프레임 전환
        if self.state == "Inform":
            pass
        elif self.state == "Map":
            self.frameList[1].destroy()
            self.frameList[0] = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2, relief='ridge', background='white')
            self.frameList[0].place(x=375, y=55)
            for i in range(14):
                self.RenderText[i] = Label(self.frameList[0], background='white')
                self.RenderText[i].place(x=0, y=i * 20)
                self.RenderText[i]['text'] = ""
        elif self.state == "Heart":
            self.HeartSelect = self.frameList[2].curselection()
            self.frameList[2].destroy()
            self.frameList[0] = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2,
                                      relief='ridge', background='white')
            self.frameList[0].place(x=375, y=55)
            for i in range(14):
                self.RenderText[i] = Label(self.frameList[0], background='white')
                self.RenderText[i].place(x=0, y=i * 20)
                self.RenderText[i]['text'] = ""
        self.state = "Inform"

        # 처리
        try:
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
            self.RenderText[13]['text'] = "이미지URL " + curAnimalList[s].popfile
        except:
            try:
                i=0
                for h in self.HeartList[self.HeartSelect[0]]:
                    if h != "\n":
                        self.RenderText[i]['text'] += h
                    else:
                        i+=1
            except:
                pass

        # 하트 버튼 어떻게 뜨는지
        self.AnimalInform = str(self.RenderText[0]['text'] + "\n" + self.RenderText[1]['text'] \
                                + "\n" + self.RenderText[2]['text'] + "\n" + self.RenderText[3]['text'] \
                                + "\n" + self.RenderText[4]['text'] + "\n" + self.RenderText[5]['text'] \
                                + "\n" + self.RenderText[6]['text'] + "\n" + self.RenderText[7]['text'] \
                                + "\n" + self.RenderText[8]['text'] + "\n" + self.RenderText[9]['text'] \
                                + "\n" + self.RenderText[10]['text'] + "\n" + self.RenderText[11]['text'] + "\n" + self.RenderText[12]['text'] + "\n" + self.RenderText[13]['text'])
        if self.AnimalInform in self.HeartList:
            self.HeartButton['image'] = self.imageList[2]
        else:
            self.HeartButton['image'] = self.imageList[1]

    def MapButtonFunc(self):
        if self.state == "Inform":
            self.frameList[0].destroy()
            self.frameList[1] = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2,
                                      relief='ridge', background='white')
            self.frameList[1].place(x=375, y=55)
        elif self.state == "Map":
            pass
        elif self.state == "Heart":
            self.frameList[2].destroy()
            self.frameList[1] = Frame(window, width=self.RightFrameWidth, height=self.RightFrameHeight, borderwidth=2,
                                      relief='ridge', background='white')
            self.frameList[1].place(x=375, y=55)
        self.state = "Map"

        # openapi로 이미지 url을 가져옴.
        gmaps = Client(key="AIzaSyAxLxOspCCw6v52W-K593bqAdgIBV351M8")

        selection = self.LeftFrame.curselection()
        s = selection[0]
        geocode = curAnimalList[s].careAddr
        sample = gmaps.geocode("대한민국 " + geocode, language='ko')
        lat = sample[0]['geometry']['location']['lat']
        lng = sample[0]['geometry']['location']['lng']

        key = "http://maps.googleapis.com/maps/api/staticmap?key=AIzaSyAxLxOspCCw6v52W-K593bqAdgIBV351M8"
        center = "&center=" + str(lat) + "," + str(lng)
        size = "&size=512x512"
        visible = "&visible=" + str(lat) + "," + str(lng)
        markers = "&markers=color:blue%7C" + str(lat) + "," + str(lng)
        url = key + center + size + visible + markers
        urllib.request.urlretrieve(url,"map.jpg")
        self.MapImage = PhotoImage(file="map.jpg")
        mapimage = Label(self.frameList[1], image=self.MapImage,width = self.RightFrameWidth, height = self.RightFrameHeight)
        mapimage.place(x=0, y=0)

    def HeartListButtonFunc(self):
        # 프레임 전환
        if self.state == "Inform":
            self.frameList[0].destroy()
            self.frameList[2] = Listbox(window, width=self.LeftFrameWidth, height=self.LeftFrameHeight+5, borderwidth=2, relief='ridge',
                    background='white', selectmode="single")
            self.frameList[2].place(x=375, y=55)
        elif self.state == "Map":
            self.frameList[1].destroy()
            self.frameList[2] = Listbox(window, width=self.LeftFrameWidth, height=self.LeftFrameHeight+5, borderwidth=2, relief='ridge',
                    background='white', selectmode="single")
            self.frameList[2].place(x=375, y=55)
        elif self.state == "Heart":
            pass
        self.state = "Heart"

        # 하트 리스트 출력
        self.frameList[2].delete(0,self.Hearti)
        self.Hearti = 0
        for i in self.HeartList:
            self.frameList[2].insert(self.Hearti, i)
            self.Hearti+=1

    def ImageButtonFunc(self):
        #이미지url 불러오기
        try:
            selection = self.LeftFrame.curselection()
            s = selection[0]
            url = curAnimalList[s].popfile
        except:
            try:
                selection = self.frameList[2].curselection()
                s = selection[0]
                i = 0
                url=""
                check = False
                for h in self.HeartList[s]:
                    if h =="\n":
                        i+=1
                    if i==13:
                        if check:
                            url+=h
                        if h == " ":
                            check = True

            except:
                try:
                    url = ""
                    check = False
                    for h in self.RenderText[13]['text']:
                        if check:
                            url += h
                        if h == " ":
                            check = True
                except:
                    return

        urllib.request.urlretrieve(url, "animal.jpg")
        AnimalImage = Image.open("animal.jpg")
        AnimalPhoto = ImageTk.PhotoImage(AnimalImage)

        self.ImageWindow = Toplevel()
        self.ImageWindow.title("이미지")
        self.ImageWindow.width = 400
        self.ImageWindow.height = 400
        self.ImageCanvas = Canvas(self.ImageWindow, width = self.ImageWindow.width, height=self.ImageWindow.height,bg="pink")
        self.ImageCanvas.pack()

        ImageLabel = Label(self.ImageCanvas, image=AnimalPhoto, width=self.ImageWindow.width, height=self.ImageWindow.height)
        ImageLabel.img = AnimalPhoto
        ImageLabel.place(x=0, y=0)

    def HeartButtonFunc(self):
        if self.state=="Inform":
            try:
                for i in self.HeartList:
                    if self.AnimalInform == i:
                        self.HeartList.remove(self.AnimalInform)
                        self.HeartButton['image'] = self.imageList[1]
                        return
                self.HeartList.append(self.AnimalInform)
                self.HeartButton['image'] = self.imageList[2]
            except:
                pass
        elif self.state=="Heart":
            try:
                self.HeartSelect = self.frameList[2].curselection()
                for h in self.HeartList:
                    if h == self.HeartList[self.HeartSelect[0]]:
                        self.HeartList.remove(self.HeartList[self.HeartSelect[0]])
                        self.HeartButton['image'] = self.imageList[1]
                        return
            except:
                pass

    def MailButtonFunc(self):
        try:
            if self.state == 'Heart':
                self.HeartSelect = self.frameList[2].curselection()
                self.AnimalInform = self.HeartList[self.HeartSelect[0]]
            else:
                self.AnimalInform = str(self.RenderText[0]['text'] + "\n" + self.RenderText[1]['text'] \
                                    + "\n" + self.RenderText[2]['text'] + "\n" + self.RenderText[3]['text'] \
                                    + "\n" + self.RenderText[4]['text'] + "\n" + self.RenderText[5]['text'] \
                                    + "\n" + self.RenderText[6]['text'] + "\n" + self.RenderText[7]['text'] \
                                    + "\n" + self.RenderText[8]['text'] + "\n" + self.RenderText[9]['text'] \
                                    + "\n" + self.RenderText[10]['text'] + "\n" + self.RenderText[11]['text'] + "\n" + self.RenderText[12]['text'] + "\n" + self.RenderText[13]['text'])
            self.emailWindow = Tk()
            self.emailWindow.title("메일 전송")
            self.emailWindow.width = 200
            self.emailWindow.height = 150
            self.emailCanvas = Canvas(self.emailWindow, width=self.emailWindow.width, height=self.emailWindow.height,
                                      bg="pink")
            self.emailCanvas.pack()
            self.emailLabel = Label(self.emailWindow, text="이메일 주소를 입력하세요", bg="pink")
            self.emailLabel.place(x=30, y=40)
            self.emailEntry = Entry(self.emailWindow, text='', justify=LEFT, width=20)
            self.emailEntry.place(x=30, y=70)
            self.emailButton = Button(self.emailWindow, text="Send", background="pink", command=self.SendEmail)
            self.emailButton.place(x=85, y=100)

            self.emailWindow.mainloop()
        except:
            pass

    def SendEmail(self):
        gmail.SendEmail(str(self.emailEntry.get()), self.AnimalInform)

    def GraphButtonFunc(self):
        dog = 0
        cat = 0
        etc = 0
        for h in self.HeartList:
            if h[4] == "개":
                dog += 1
            elif h[4] == "고":
                cat += 1
            else:
                etc += 1
        self.GraphWindow = Tk()
        self.GraphWindow.title("그래프")
        self.GraphWindow.width = 300
        self.GraphWindow.height = 300
        self.GraphCanvas = Canvas(self.GraphWindow, width=self.GraphWindow.width, height=self.GraphWindow.height,
                                  bg="pink")
        self.GraphCanvas.pack()
        self.GraphLabel = Label(self.GraphWindow, text="List of animals in the heart list", bg="pink")
        self.GraphLabel.place(x=70, y=10)
        Graphs = [dog, cat, etc]
        maxCount = int(max(Graphs))
        self.GraphCanvas.create_line(10, self.GraphWindow.height - 10, self.GraphWindow.width - 10, self.GraphWindow.height - 10)
        self.GraphCanvas.create_line(10, 50, 10, self.GraphWindow.height - 10)
        barW = 40
        for i in range(3):
            self.GraphCanvas.create_rectangle(barW * i + 10 + 30 * (i+1), self.GraphWindow.height - ((self.GraphWindow.height * Graphs[i]) / (maxCount + 1)) - 10,
                                         barW * (i + 1) + 10+ 30 * (i+1), self.GraphWindow.height - 10, fill='hotpink')
            if i == 0:
                self.GraphCanvas.create_text(20 + i * barW + 9+30 * (i+1), self.GraphWindow.height - 5, text="개")
            elif i == 1:
                self.GraphCanvas.create_text(20 + i * barW + 7+ 30 * (i+1), self.GraphWindow.height - 5, text="고양이")
            elif i == 2:
                self.GraphCanvas.create_text(20 + i * barW + 9+ 30 * (i+1), self.GraphWindow.height - 5, text="기타")
            self.GraphCanvas.create_text(60 + i * barW + 30*i, self.GraphWindow.height - ((self.GraphWindow.height * Graphs[i]) / (maxCount + 1)) - 20,
                                    text=str(Graphs[i]))
        self.GraphWindow.mainloop()


WarmHeart()