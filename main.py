import requests
import time
import random


def DataPost():
    send_msg = time.strftime("%m月%d日%H时%M分  签到", time.localtime())
    ti = int(time.time())

    url = 'https://api.live.bilibili.com/msg/send'

    data = {
        'color': '5566168',
        'fontsize': '25',
        'mode': '1',
        'msg': send_msg,
        'rnd': '{}'.format(ti),
        'roomid': '1479861',
        'bubble': '0',
        'csrf_token': 'YourToken',
        'csrf': 'YourToken'
    }
    cookie = "YourCookie"
    headers = {
        'cookie': cookie,
        'origin': 'https://live.bilibili.com',
        'referer': 'https://live.bilibili.com/blanc/1479861?liteVersion=true',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    response = requests.post(url=url, data=data, headers=headers)


while True:
    ls = random.randint(1,10)
    if ls == 5:
        DataPost()
        print(time.strftime("%m月%d日%H时%M分已执行", time.localtime()))
        time.sleep(43200)
    else:
        t = ls * 600
        time.sleep(t)


