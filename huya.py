#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Fy
cron: 0 */2 * * * ?
new Env('虎牙直播监控');
"""
import json
import re
from datetime import datetime
from contextlib import closing

import pymysql
import requests
from wx import WeChatPub

CONFIG_URL = "https://raw.gitcode.com/qq_35720175/web/raw/main/config.json"

# 获取全局配置
config = requests.get(CONFIG_URL).json()
ROOM_IDS = config["room"]
DB_HOSTS = [config["host"], '192.168.66.189']  # 优先尝试内网地址
DB_USER = config["user"]
DB_PWD = config["password"]
DB_NAME = config["db"]
HY_COOKIE = config["hy"]


class HuYaMonitor:
    def __init__(self, room_id):
        self.room_id = room_id
        self.db = self._connect_database()
        self.cursor = self.db.cursor()

    def _connect_database(self):
        """尝试多个数据库主机进行连接"""
        for host in DB_HOSTS:
            try:
                return pymysql.connect(
                    host=host,
                    user=DB_USER,
                    password=DB_PWD,
                    port=3306,
                    database=DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor
                )
            except pymysql.Error:
                continue
        raise ConnectionError("无法连接到任何数据库主机")

    def get_real_url(self):
        """获取直播状态并处理"""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36',
            'Cookie': HY_COOKIE
        }

        try:
            response = requests.get(f'https://m.huya.com/{self.room_id}', headers=headers)
            response.raise_for_status()
            page_content = response.text

            profile_info = json.loads(re.search(r'"tProfileInfo":({.*?})', page_content).group(1))
            live_status = int(re.search(r'"eLiveStatus":(\d+)', page_content).group(1))
            
            status_num = 1 if live_status == 2 else 0
            self._process_status({
                "room": self.room_id,
                "name": profile_info["sNick"]  # 确保此处获取主播名称
            }, status_num)
            
        except requests.RequestException as e:
            print(f"[{self.room_id}] 请求异常: {e}")
        except (AttributeError, json.JSONDecodeError) as e:
            print(f"[{self.room_id}] 数据解析失败: {e}")

    def _process_status(self, data, status):
        """处理直播状态变更"""
        try:
            with closing(self.db.cursor()) as cursor:
                cursor.execute('SELECT is_live FROM huya WHERE room = %s', self.room_id)
                result = cursor.fetchone()

                # 修改点1：添加主播名称到日志输出
                if result and result['is_live'] == status:
                    print(f"主播 {data['name']}（房间号：{self.room_id}）的直播状态未变化")
                    return

                self._update_database(data, status)
                self._send_notification(data, status)

        except pymysql.Error as e:
            print(f"[{data['name']}] 数据库操作失败: {e}")
            self.db.rollback()

    def _update_database(self, data, status):
        """更新数据库记录"""
        with closing(self.db.cursor()) as cursor:
            try:
                # 修改点2：添加操作对象信息
                print(f"正在更新 {data['name']}（{self.room_id}）的直播状态...")
                cursor.execute('DELETE FROM huya WHERE room = %s', self.room_id)
                cursor.execute(
                    'INSERT INTO huya (room, name, is_live) VALUES (%s, %s, %s)',
                    (data["room"], data["name"], status)
                )
                self.db.commit()
                print(f"主播 {data['name']}（{self.room_id}）数据库更新成功")
            except pymysql.Error as e:
                self.db.rollback()
                print(f"主播 {data['name']}（{self.room_id}）数据库更新失败: {e}")

    def _send_notification(self, data, status):
        """发送微信通知"""               
        # 修改点：添加语录获取的容错处理
        try:
            hitokoto = requests.get("https://v1.hitokoto.cn/", timeout=3).json()
            quote = f'\n\n{hitokoto["hitokoto"]} —— {hitokoto["from"]}\n\n'
        except Exception as e:
            print(f"[{data['name']}] 获取语录失败: {e}")
            quote = ''  # 失败时设为空文本
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_text = "开播了" if status else "下播了"

         # 修改点3：日志添加主播信息
        print(f"正在给 {data['name']}（{self.room_id}）发送通知...")
        '''
        WeChatPub().send_news(
            title=f'{data["name"]} {status_text}🐯🐯🐯',
            description=f'房间号: {self.room_id}\n\n{quote}\n\n{timestamp}',
            to_url=f'https://m.huya.com/{self.room_id}',
            picurl="https://cn.bing.com/th?id=OHR.DolbadarnCastle_ZH-CN5397592090_1920x1080.jpg"
        )
         '''
        try:
            QLAPI.notify(
                f'{data["name"]} {status_text}',
                f'房间号: {self.room_id}\n\n{quote}\n\n{timestamp}'
            )
        except Exception as e:
            print(f"[{data['name']}] QLAPI通知失败: {e}")
 




def main():
    for room_id in ROOM_IDS:
        try:
            print(f"\n{' 开始处理 ':*^40}")
            monitor = HuYaMonitor(room_id)
            monitor.get_real_url()
            print(f"{' 处理完成 ':*^40}\n")
        except Exception as e:
            print(f"[{room_id}] 处理异常: {e}")
        finally:
            monitor.db.close()


if __name__ == '__main__':
    main()
