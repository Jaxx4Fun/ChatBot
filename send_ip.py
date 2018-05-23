import os, time
import socket, fcntl, struct
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('1.1.1.1',80))
    return s.getsockname()[0]

def send_mail():
    from_addr = "309329794@qq.com"
    password = "zj226605"
    authorization = 'nirkrcbezwgibjge'
    smtp_server = "smtp.qq.com"
    to_addr = "309329794@qq.com"

    server = SMTP_SSL(smtp_server)
    server.ehlo(smtp_server)
    server.login(from_addr, authorization)

    msg = MIMEText('Hello, My ip address is ' + get_ip_address('eth0'), 'plain', 'utf-8')
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == "__main__":
    # 睡眠20秒，使程序在系统初始化成功后进行运行。
    # 不然可能会因为系统还没准备好你的程序就强行运行而导致启动失败。
    while True:
        try:
            send_mail()
            break
        except:
            time.sleep(3)
