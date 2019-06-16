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

import noti

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('날짜검색') and len(args)>1:
        print('try to 날짜검색', args[1])
        SearchByDate( args[1], chat_id, args[2] )
    elif  text.startswith('지역검색') and len(args)>1:
        print('try to 지역검색', args[1])
        SearchBySigungu( args[1], chat_id, args[2] )
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n날짜검색 [시작날짜] [종료날짜] 을 입력하세요.')

def SearchByDate(start, user, end):
    print(user, start, end)
    res_list = noti.getData(start, end)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r + msg) + 1 > noti.MAX_MSG_LENGTH:
            noti.sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '{} ~ {} 기간에 해당하는 데이터가 없습니다.'.format(start, end))

today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)