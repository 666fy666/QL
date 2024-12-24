#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Fy
cron: 0 */2 * * * ?
new Env('斗鱼直播监控');
"""

# 获取斗鱼直播间的真实流媒体地址，默认最高画质
import hashlib
import re
import time
from datetime import datetime

import pymysql
import requests

from Send import PrivateMessage
from wx import WeChatPub

url = "https://raw.gitcode.com/qq_35720175/web/raw/main/config.json"
file = requests.get(url)
host = file.json()["host"]
user = file.json()["user"]
pwd = file.json()["password"]
dbs = file.json()["db"]
douyu = file.json()["douyu"]


class DouYu:
    def __init__(self, rid):
        """
        房间号通常为1~8位纯数字，浏览器地址栏中看到的房间号不一定是真实rid.
        Args:
            rid:
        """
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
        # "https://www.douyu.com/japi/livebiznc/web/anchorstardiscover/redbag/room/list?rid=314761"
        self.did = '10000000000000000000000000001501'

        self.s = requests.Session()
        self.res = self.s.get('https://m.douyu.com/' + str(rid), timeout=30).text
        name = self.s.get(
            'https://www.douyu.com/japi/livebiznc/web/anchorstardiscover/redbag/room/list?rid=' + str(rid),
            timeout=30).json()
        result = re.search(r'rid":(\d{1,8}),"vipId', self.res)
        self.name = (name["data"]["anchorName"])
        # print(self.name)
        if result:
            self.rid = result.group(1)
        else:
            raise Exception('房间号错误')

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_pre(self):
        url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + self.rid
        data = {
            'rid': self.rid,
            'did': self.did
        }
        t13 = str(int((time.time() * 1000)))
        auth = DouYu.md5(self.rid + t13)
        headers = {
            'rid': self.rid,
            'time': t13,
            'auth': auth
        }
        res = self.s.post(url, headers=headers, data=data, timeout=30).json()
        error = res['error']
        return error

    def get_real_url(self):
        data = {
            "room": self.rid,
            "name": self.name
        }
        error = self.get_pre()
        if error == 0:
            self.deal(data, num=1)
        elif error == 102:
            #raise Exception('房间不存在')
            self.deal(data, num=0)
        elif error == 104:
            #raise Exception('房间未开播')
            self.deal(data, num=0)

    def deal(self, data, num):
        try:
            sql = 'select is_live from douyu where room=%s'
            self.cursor.execute(sql, self.rid)
            result = self.cursor.fetchall()  # 返回所有数据
            old = result[0][0]
            if old == num:
                data["is_live"] = old
                print("%s的直播状态已提醒" % self.rid)
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
        '''
        wechat = WeChatPub()
        wechat.send_news(
            title='{} {}'.format(data["name"], is_live),  # 标题
            description='Ta的斗鱼房间号是 : {}\n\n{}\n\n{}'.format
            (self.rid, res, timestamp),  # 说明文案
            to_url=r'https://m.douyu.com/' + str(self.rid),  # 链接地址
            picurl=r"https://cn.bing.com/th?id=OHR.PortMarseille_ZH-CN3194394496_1920x1080.jpg"  # 图片地址
            # btntxt = '此处跳转'  https://www.picgo.net/image/ymwTq
        )
        '''
        try:
            QLAPI.notify('{} {}🐟🐟🐟'.format(data["name"], is_live), 'Ta的斗鱼房间号是 : {}\n\n{}\n\n{}'.format(self.rid, res, timestamp))
            info = '{} {}🐟🐟🐟'.format(data["name"], is_live), 'Ta的斗鱼房间号是 : {}\n\n{}\n\n{}'.format(self.rid, res,
                                                                                                        timestamp)
            responder_pri = PrivateMessage()
            responder_pri.send_private_message("657769008", info)
        except:
            pass

    def check(self, data):  # 写入并更新直播状态
        self.del_database()
        self.in_database(data)

    def del_database(self):  # 更新数据库(删除旧数据)
        try:
            sql = 'delete from douyu where room = %s'
            self.cursor.execute(sql, self.rid)
            self.db.commit()
            print("delete_successful")
        except Exception as e:
            self.db.rollback()
            print(e)

    def in_database(self, data):  # 更新数据库(插入新数据)
        try:
            sql = ('insert into douyu(room,name,is_live) '
                   'VALUES(%(room)s, %(name)s, %(is_live)s)')
            self.cursor.execute(sql, data)
            self.db.commit()
            print("insert_successful")
        except Exception as e:
            self.db.rollback()
            print(e)


def go(rid):
    app = DouYu(rid)
    app.get_real_url()


if __name__ == '__main__':
    for i in range(len(douyu)):
        go(douyu[i])
        print("=" * 40)
