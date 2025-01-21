#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Fy
cron: 0 55 23 * * ?
new Env('ikuuu机场签到');
"""
import os
import re
import requests
from lxml import etree


class Ikuuu:
    def __init__(self):
        self.UserAgent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36")
        self.url = "https://ikuuu.org/"
        if os.getenv('Ikuuu'):
            total = os.getenv('Ikuuu')
            allin = re.split(r'[:：;]', total)
            self.acc = allin[0]
            self.pwd = allin[1]
            print("找到环境变量!")
        else:
            self.acc = "657769008@qq.com"
            self.pwd = "Fy12345678"

    def main(self):
        cookies = self.login()
        info = self.analysis(cookies) + "\n"
        info += self.sign(cookies)
        self.wx_pro(info)
        print(info)

    def analysis(self, cookies):
        url = "{}user".format(self.url)
        headers = {
            "User-Agent": self.UserAgent,
            "Cookie": cookies,
            "Referer": "{}auth/login".format(self.url),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
        }
        r = requests.get(url, headers=headers)
        html = etree.HTML(r.text)
        info = ""
        name = html.xpath('//*[@id="app"]/div/nav/ul/li[2]/a/div/text()')[0]
        info += name + ":\n"
        timing = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[1]/div/div[2]/div[2]/span/text()')[0].replace(
            " ", "").replace("\n", "")
        info += "                       会员时长还剩%s天\n" % timing
        date = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[1]/div/div[3]/div/nav/ol/li/text()')[0].replace(
            " ", "").replace("\n", "")
        info += "                       " + date + "\n"
        net1 = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[2]/div/div[2]/div[2]/span/text()')[0].replace(
            " ", "").replace("\n", "")
        info += "                       剩余流量:{}GB\n".format(net1)
        today = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[2]/div/div[2]/div[3]/div/nav/ol/li/text()')[
            0].replace(" ", "").replace("\n", "")
        info += "                       " + today + "\n"
        num1 = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[3]/div/div[2]/div[2]/span[1]/text()')[
            0].replace(" ", "").replace("\n", "")
        num2 = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[3]/div/div[2]/div[2]/span[2]/text()')[
            0].replace(" ", "").replace("\n", "")
        info += "                       在线设备数: {} / {}\n".format(num1, num2)
        money = html.xpath('//*[@id="app"]/div/div[3]/section/div[3]/div[4]/div/div[2]/div[2]/span/text()')[0].replace(
            " ", "").replace("\n", "")
        info += "                       钱包余额 ¥ %s" % money
        return info

    def sign(self, cookies):  # 签到得流量
        url = "{}user/checkin".format(self.url)
        headers = {
            "User-Agent": self.UserAgent,
            "Cookie": cookies,
            "Referer": "{}auth/login".format(self.url),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
        }
        r = requests.post(url, headers=headers)
        try:
            info = "                       " + r.json()["msg"]
        except:
            info = "                       cookies似乎过期了"
        return info

    def login(self):  # 拿账号密码登录获取cookies
        url = "{}auth/login".format(self.url)
        headers = {
            "User-Agent": self.UserAgent,
            "Referer": "{}auth/login".format(self.url),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
        }
        data = {
            "email": self.acc,
            "passwd": self.pwd,
            "code": "",
            "remember_me": "on"
        }
        r = requests.post(url, data=data, headers=headers)
        # 获取cookie
        cookies = r.cookies.items()
        cookie = ''
        for name, value in cookies:
            cookie += '{0}={1};'.format(name, value)
        print(cookie)
        return cookie

    def wx_pro(self, info):
        try:
            QLAPI.notify('iKuuu机场签到提醒', '{}'.format(info))
        except:
            pass


if __name__ == '__main__':
    for u in range(0, 5):
        try:
            ik = Ikuuu()
            ik.main()
            break
        except Exception as e:
            print(e)
