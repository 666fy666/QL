"""
Author: Fy
new Env('企业微信推送');
"""
import json
import os
import time

import requests


class WeChatPub:
    s = requests.session()

    def __init__(self):
        self.corpid = 'wwa721a143a22ceed4'
        self.secret = 'OZwYUc5FABoqJVonBioH3DekVeuvlf5pjkxLTdaHJus'  # 企业微信应用后台查看
        self.token = self.get_token()

        # print('init_token',self.token)

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.secret}&debug=1"
        rep = self.s.get(url)
        # print('rep_token', rep.content)
        if rep.status_code != 200:
            print('get token failed')
            return
        return json.loads(rep.content)['access_token']

    def send_news(self, title, description, to_url, picurl, btntxt='阅读全文'):# 跳转为链接
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        # python 字典若要转json，千万不能用单引号，要用双引号~@@双引号~~~！！！
        form_data = {
            "touser": "NiHenPi",
            "toparty": "",
            "msgtype": "news",
            "agentid": "1000002",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": description,
                        "url": to_url,
                        "author": "FengYu",
                        "picurl": picurl,
                        "btntxt": btntxt
                    }
                ]
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        print(form_data, type(form_data))
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed")
            return
        return json.loads(rep.content)

    def send_markdown(self, ms):# 跳转为链接
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        # python 字典若要转json，千万不能用单引号，要用双引号~@@双引号~~~！！！
        form_data = {
            "touser": "FengYu",
            "msgtype": "markdown",
            "agentid": "1000002",
            "markdown": {
                "content": ms
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        print(form_data, type(form_data))
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed")
            return
        return json.loads(rep.content)


'''
if __name__ == '__main__':
    # 图片消息模板
    # title,description,url,picurl,btntxt='阅读全文'
    wechat = WeChatPub()

    wechat.send_news(
        title='iKuuu机场签到提醒(*￣▽￣*)ブ',  # 标题
        description='\n{}\n\n{}',  # 说明文案
        to_url=r"https://ikuuu.pw/",  # 链接地址
        picurl="https://cn.bing.com/th?id=OHR.PortMarseille_ZH-CN3194394496_1920x1080.jpg"  # 图片地址
        # btntxt = '此处跳转'  https://www.picgo.net/image/ymwTq
    )

    #  wechat.send_text(title='iKuuu机场签到提醒', message='\n{}\n\n{}', purl="https://bing.img.run/1366x768.php")  # 说明文案

    # <img src="https://bing.img.run/rand_uhd.php" alt="随机获取Bing历史壁纸UHD超高清原图" />
    # <img src="https://bing.img.run/rand.php" alt="随机获取Bing历史壁纸1080P高清" />
    # <img src="https://bing.img.run/rand_1366x768.php" alt="随机获取Bing历史壁纸普清" />
    # <img src="https://bing.img.run/rand_m.php" alt="随机获取Bing历史壁纸手机版1080P高清" />
    # <img src="https://bing.img.run/uhd.php" alt="Bing每日壁纸UHD超高清原图" />
    # <img src="https://bing.img.run/1920x1080.php" alt="Bing每日壁纸1080P高清" />
    # <img src="https://bing.img.run/1366x768.php" alt="Bing每日壁纸普清" />
    # <img src="https://bing.img.run/m.php" alt="Bing每日壁纸手机版1080P高清" />
'''
