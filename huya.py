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
            
            status_num = 1 if live_status == 2 else 0  # 简化状态判断
            self._process_status({
                "room": self.room_id,
                "name": profile_info["sNick"]
            }, status_num)
            
        except requests.RequestException as e:
            print(f"请求异常: {e}")
        except (AttributeError, json.JSONDecodeError) as e:
            print(f"数据解析失败: {e}")

    def _process_status(self, data, status):
        """处理直播状态变更"""
        try:
            with closing(self.db.cursor()) as cursor:
                cursor.execute('SELECT is_live FROM huya WHERE room = %s', self.room_id)
                result = cursor.fetchone()

                if result and result['is_live'] == status:
                    print(f"{self.room_id} 的直播状态未变化")
                    return

                self._update_database(data, status)
                self._send_notification(data, status)

        except pymysql.Error as e:
            print(f"数据库操作失败: {e}")
            self.db.rollback()

    def _update_database(self, data, status):
        """更新数据库记录"""
        with closing(self.db.cursor()) as cursor:
            try:
                cursor.execute('DELETE FROM huya WHERE room = %s', self.room_id)
                cursor.execute(
                    'INSERT INTO huya (room, name, is_live) VALUES (%s, %s, %s)',
                    (data["room"], data["name"], status)
                )
                self.db.commit()
                print("数据库更新成功")
            except pymysql.Error as e:
                self.db.rollback()
                print(f"数据库更新失败: {e}")

    def _send_notification(self, data, status):
        """发送微信通知"""
        try:
            hitokoto = requests.get("https://v1.hitokoto.cn/").json()
            quote = f'{hitokoto["hitokoto"]} —— {hitokoto["from"]}'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status_text = "开播了" if status else "下播了"

            # 企业微信通知
            WeChatPub().send_news(
                title=f'{data["name"]} {status_text}🐯🐯🐯',
                description=f'房间号: {self.room_id}\n\n{quote}\n\n{timestamp}',
                to_url=f'https://m.huya.com/{self.room_id}',
                picurl="https://cn.bing.com/th?id=OHR.DolbadarnCastle_ZH-CN5397592090_1920x1080.jpg"
            )

            # 其他通知方式
            try:
                QLAPI.notify(
                    f'{data["name"]} {status_text}',
                    f'房间号: {self.room_id}\n\n{quote}\n\n{timestamp}'
                )
            except Exception as e:
                print(f"QLAPI通知失败: {e}")

        except requests.RequestException as e:
            print(f"获取每日语录失败: {e}")


def main():
    for room_id in ROOM_IDS:
        try:
            monitor = HuYaMonitor(room_id)
            monitor.get_real_url()
            print("=" * 40)
        except Exception as e:
            print(f"处理房间 {room_id} 时发生错误: {e}")
        finally:
            monitor.db.close()  # 确保关闭数据库连接


if __name__ == '__main__':
    main()
