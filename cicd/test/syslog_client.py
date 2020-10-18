"""Модуль реализует отсылку данных на 514 порт, для тестирования Syslog-сервера. """
import socket
import time
from datetime import datetime
import random

message = ['WPA2-AES PSK authentication in progress...',
           'A wireless client is associated - 70:F3:95:E5:59:EE to ssid zxc3',
           'Open and authenticated', 'A wireless client is disassociated - 84:85:06:21:D5:5A',
           '(zxc3) Disassoc received from 84:85:06:21:d5:5a Reason: Leaving (or has left) BSS[8]']
tags = ['kernel: wlan0:']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("192.168.0.102", 5140))
sock.connect(("localhost", 5140))


def random_mac():
    """Генерирует случайные маки."""
    r_m = []
    for _ in range(6):
        r_m.append(str(random.randint(10, 99)))
    return ':'.join(r_m)


def random_ip():
    """Генерирует случайные ип."""
    r_i = []
    for _ in range(4):
        r_i.append(str(random.randint(100, 255)))
    return '.'.join(r_i)


while True:
    mes = random.choice(message)
    if 'assoc' in mes:
        mes = mes.replace('70:F3:95:E5:59:EE', random_mac())
    prior = random.randint(1, 12)
    d = datetime.now().day
    t = datetime.now().time().strftime("%H:%M:%S")
    from_host = random_ip()
    tag = random.choice(tags)
    TEMPLATE = '<{}>Jul {} {} {} {} {}'
    s = bytes(TEMPLATE.format(prior, d, t, from_host, tag, mes), encoding='UTF-8')
    sock.send(s)
    print(s)
    time.sleep(5)
