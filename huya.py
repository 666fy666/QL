#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Fy
cron: 0 */1 * * * ?
new Env('虎牙直播监控');
"""
# 获取虎牙直播的真实流媒体地址。
import json
import re
from datetime import datetime

import pymysql
import requests

from wx import WeChatPub

url = "https://raw.gitcode.com/qq_35720175/web/raw/main/config.json"
file = requests.get(url)
rid = file.json()["room"]
host = file.json()["host"]
user = file.json()["user"]
pwd = file.json()["password"]
dbs = file.json()["db"]
hy = file.json()["hy"]


class HuYa:
    def __init__(self, id):
        self.room_id = id  # 虎牙房间号
        try:
            db = pymysql.connect(host='192.168.66.239', user='%s' % user, password='%s' % pwd, port=3306, db='%s' % dbs)
            cursor = db.cursor()
            self.db = db
            self.cursor = cursor
        except:
            db = pymysql.connect(host='%s' % host, user='%s' % user, password='%s' % pwd, port=3306, db='%s' % dbs)
            cursor = db.cursor()
            self.db = db
            self.cursor = cursor
        

    def get_real_url(self):
        room_url = 'https://m.huya.com/' + str(self.room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.100 Mobile Safari/537.36 ',
            'Cookie': hy
        }
        data = requests.get(url=room_url, headers=header).text

        # 正则表达式模式
        pattern_tProfileInfo = r'"tProfileInfo":({.*?})'
        pattern_eLiveStatus = r'"eLiveStatus":(\d+)'

        # 提取 tProfileInfo
        match_tProfileInfo = re.search(pattern_tProfileInfo, data)
        tProfileInfo = json.loads(match_tProfileInfo.group(1))
        # print("tProfileInfo:", tProfileInfo)

        # 提取 eLiveStatus
        match_eLiveStatus = re.search(pattern_eLiveStatus, data)
        eLiveStatus = int(match_eLiveStatus.group(1))
        print("eLiveStatus:", eLiveStatus)

        data = {
            "room": self.room_id,
            "name": tProfileInfo["sNick"]
        }
        if eLiveStatus == 2:  # 在直播
            self.deal(data, num=1)
        elif eLiveStatus == 3:  # 下播
            self.deal(data, num=0)
        else:
            self.deal(data, num=0)

    def deal(self, data, num):
        try:
            sql = 'select is_live from huya where room=%s'
            self.cursor.execute(sql, self.room_id)
            result = self.cursor.fetchall()  # 返回所有数据
            old = result[0][0]
            if old == num:
                data["is_live"] = old
                print("%s的直播状态已提醒" % self.room_id)
            else:
                data["is_live"] = num
                self.check(data)
                self.wx_pro(data)
        except:
            data["is_live"] = num
            self.check(data)
            self.wx_pro(data)

    def wx_pro(self, data):  # 采用企业微信图文推送（效果好）
        # 图片消息
        # title,description,url,picurl,btntxt='阅读全文'
        tip = "https://v1.hitokoto.cn/"
        res = requests.get(tip).json()
        res = res["hitokoto"] + "    ----" + res["from"]
        curr_time = datetime.now()
        timestamp = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
        if data["is_live"] == 1:
            is_live = "开播了"
        else:
            is_live = "下播了"
        wechat = WeChatPub()
        wechat.send_news(
            title='{} {}🐯🐯🐯'.format(data["name"], is_live),  # 标题
            description='Ta的虎牙房间号是 : {}\n\n{}\n\n{}'.format
            (self.room_id, res, timestamp),  # 说明文案
            to_url=r'https://m.huya.com/' + str(self.room_id),  # 链接地址
            picurl=r"https://cn.bing.com/th?id=OHR.PortMarseille_ZH-CN3194394496_1920x1080.jpg"  # 图片地址
            # btntxt = '此处跳转'  https://www.picgo.net/image/ymwTq
        )

    def check(self, data):  # 写入并更新直播状态
        self.del_database()
        self.in_database(data)

    def del_database(self):  # 更新数据库(删除旧数据)
        try:
            sql = 'delete from huya where room = %s'
            self.cursor.execute(sql, self.room_id)
            self.db.commit()
            print("delete_successful")
        except Exception as e:
            self.db.rollback()
            print(e)

    def in_database(self, data):  # 更新数据库(插入新数据)
        try:
            sql = ('insert into huya(room,name,is_live) '
                   'VALUES(%(room)s, %(name)s, %(is_live)s)')
            self.cursor.execute(sql, data)
            self.db.commit()
            print("insert_successful")
        except Exception as e:
            self.db.rollback()
            print(e)

def go(rid):
    try:
        app = HuYa(rid)
        app.get_real_url()
    except:
        pass
    

if __name__ == '__main__':
    for i in range(len(rid)):
        go(rid[i])
        print("=" * 40)
      
