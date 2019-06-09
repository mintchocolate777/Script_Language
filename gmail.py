# -*- coding: utf-8 -*-
import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def SendEmail(recipientAddr, AnimalInform):
    #global value
    host = "smtp.gmail.com" # Gmail STMP 서버 주소.
    port = "587"

    senderAddr = "xhwlddj98@gmail.com"     # 보내는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "WarmHeart"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    #recipientAddr = MIMEText(recipientAddr, _charset='UTF-8')
    AnimalInform = MIMEText(AnimalInform, _charset='UTF-8')
    msg.attach(AnimalInform)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("xhwlddj98@gmail.com","y6u7i8o9p0!")
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()





































