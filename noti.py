#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
import re
from datetime import date, datetime, timedelta
import traceback
import OpenApiParsing
import OpenSidoApi
import OpenSigunguApi

TOKEN = '859315018:AAGuh_RkfYjDy9MToyfeWjK4XkLBUcaA43s'#'여기에 텔레그램 토큰을 입력하세요'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getData(bgnde, endde):
    res_list = []
    tree = OpenApiParsing.SearchByDate(bgnde, endde)
    itemElements = tree.getiterator("item")
    for item in itemElements:
        print(item)
        kind = "품종: " + item.find("kindCd").text
        gender = "성별: " + item.find("sexCd").text
        color = "털색: " + item.find("colorCd").text
        weight = "체중: " + item.find("weight").text
        age = "나이: " + item.find("age").text
        happenPlace = "발견: " + item.find("happenPlace").text
        specialMark = "특징: " + item.find("specialMark").text
        happenDt = "접수: " +item.find("happenDt").text
        neuterYn = "중성화여부: " + item.find("neuterYn").text
        careNm = "보호소이름: " + item.find("careNm").text
        careAddr = "보호장소: " + item.find("careAddr").text
        chargeNm = "담당자: " + item.find("chargeNm").text
        careTel = "연락처: " + item.find("careTel").text
        popfile = "이미지URL: "+ item.find("popfile").text
        try:
            row = kind+"\n"+gender+"\n"+color+"\n"+weight+"\n"+age+"\n"+happenPlace+"\n"+specialMark+"\n"+happenDt+"\n"+neuterYn+"\n"+\
                careNm+"\n"+careAddr+"\n"+chargeNm+"\n"+careTel+"\n"+popfile
        except IndexError:
            return
        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
