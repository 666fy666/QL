#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
cron: 0 5 0 * * ?
new Env('百度贴吧');
"""

import os
import requests
import re
import time
import json
import random

tieba='BIDUPSID=27D7253D9334696C06D4DEC6FE4BE7BF; PSTM=1693760491; BDUSS=Dlvdmhrd0owdDVDcVRXNzlmS1Q2S1VNcUxUNVJCRnJPcVVyTEl1MVhFUFJnVkZsRVFBQUFBJCQAAAAAAAAAAAEAAAD1I-VGZnk2NjY2wNbUsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANH0KWXR9Clld; BDUSS_BFESS=Dlvdmhrd0owdDVDcVRXNzlmS1Q2S1VNcUxUNVJCRnJPcVVyTEl1MVhFUFJnVkZsRVFBQUFBJCQAAAAAAAAAAAEAAAD1I-VGZnk2NjY2wNbUsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANH0KWXR9Clld; BAIDUID=27D7253D9334696CF934BED0958EB3BD:SL=0:NR=10:FG=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1698215771; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1698215772; H_WISE_SIDS=60236_60360_60450; H_WISE_SIDS_BFESS=60236_60360_60450; H_PS_PSSID=60236_60450_60360_60452_60466_60498_60516_60521; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=27D7253D9334696CF934BED0958EB3BD:SL=0:NR=10:FG=1; BA_HECTOR=2g2k2k2l0l01ala105842501b7sg3a1jaeab01v; ZFY=B0PVqM9eOVoICOoxHe5:BBx:AoZigvdJXOTug4BnFrVuw:C; delPer=0; PSINO=5; BCLID=9451502627084325613; BCLID_BFESS=9451502627084325613; BDSFRCVID=0XuOJexroG3Q5sbt6g0nJTq6LgKKvV3TDYLEOwXPsp3LGJLVY4LSEG0Pt8lgCZu-2ZlgogKK0eOTHkAF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=0XuOJexroG3Q5sbt6g0nJTq6LgKKvV3TDYLEOwXPsp3LGJLVY4LSEG0Pt8lgCZu-2ZlgogKK0eOTHkAF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=JJkO_D_atKvDqTrP-trf5DCShUFsBlvJB2Q-XPoO3KOGMtOP55jJ0M_p3hLqWPbiW5cpoMbgylRp8P3y0bb2DUA1y4vpX63rL2TxoUJ2fnRJEUcGqj5Ah--ebPRiJPQ9QgbW5lQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0MC09j6KhDTPVKgTa54cbb4o2WbCQL-5r8pcN2b5oQTtujqba-T5MLTRZ-PDKBn3vOPQKDpOUWfAkXpJvQnJjt2JxaqRCyCbdVp5jDh3Me-AsLn6te6jzaIvy0hvctn5cShncLfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhjGtOtjDttb3aQ5rtKRTffjrnhPF3LDuUXP6-hnjy3b7I_4OtbIQJVbv_3bL-X--UypjpJh3RymJ42-39LPO2hpRjyxv4Wj0T0PoxJpOJfIJM5McaHCoADb3vbURvD-Lg3-7W3x5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE_D0yJD_hhIvPKITD-tFO5eT22-us-CJt2hcHMPoosIOhjJbD55KshG3ZLn_qBIvia-QCtMbUoqRHXnJi0btQDPvxBf7pyRnrbh5TtUJMbbRTLp6hqjDlhMJyKMnitIT9-pno0lQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuj6tWj6j0DNRabK6aKC5bL6rJabC3hMnGXU6q2bDeQNbItRJabncMonrFQPD-8b3oynj4Dp0vWtv4WbbvLT7johRTWqR4oDbs0UonDh83eMvM3hTtHRrzWn3O5hvvhb5O3M7OLfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qR-toKbP; H_BDCLCKID_SF_BFESS=JJkO_D_atKvDqTrP-trf5DCShUFsBlvJB2Q-XPoO3KOGMtOP55jJ0M_p3hLqWPbiW5cpoMbgylRp8P3y0bb2DUA1y4vpX63rL2TxoUJ2fnRJEUcGqj5Ah--ebPRiJPQ9QgbW5lQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0MC09j6KhDTPVKgTa54cbb4o2WbCQL-5r8pcN2b5oQTtujqba-T5MLTRZ-PDKBn3vOPQKDpOUWfAkXpJvQnJjt2JxaqRCyCbdVp5jDh3Me-AsLn6te6jzaIvy0hvctn5cShncLfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhjGtOtjDttb3aQ5rtKRTffjrnhPF3LDuUXP6-hnjy3b7I_4OtbIQJVbv_3bL-X--UypjpJh3RymJ42-39LPO2hpRjyxv4Wj0T0PoxJpOJfIJM5McaHCoADb3vbURvD-Lg3-7W3x5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE_D0yJD_hhIvPKITD-tFO5eT22-us-CJt2hcHMPoosIOhjJbD55KshG3ZLn_qBIvia-QCtMbUoqRHXnJi0btQDPvxBf7pyRnrbh5TtUJMbbRTLp6hqjDlhMJyKMnitIT9-pno0lQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuj6tWj6j0DNRabK6aKC5bL6rJabC3hMnGXU6q2bDeQNbItRJabncMonrFQPD-8b3oynj4Dp0vWtv4WbbvLT7johRTWqR4oDbs0UonDh83eMvM3hTtHRrzWn3O5hvvhb5O3M7OLfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qR-toKbP; STOKEN=f4a5a4e6fa0e04d2e785746270e38432459a61b9061f8cd306749b290a70e7c3; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1722231139; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1722231139; HMACCOUNT=AF075B089144DE90; BAIDU_WISE_UID=wapp_1722231092080_250; USER_JUMP=-1; XFI=ec708050-4d6b-11ef-9cc8-1da7f1226133; ab_sr=1.0.1_ODVjYmM0NDE2ODE5Y2M4Njc0M2IwYmE5MmVjZWMyNGQyZDcxMDBlZjJkYTc4ZDg0MGMwOWJmMzM0OGMwMzVhZjk5NTU4NGQ5NTRmNDhhY2I5NjFlNzk4OWU2NDRlNWJmNTA0YTM2ODNiNWQ3NzRjMzY0NDU3ZjFjZDNkMWQ3ZDQwZjc4MzJiNGYzNzRiNDY1ZWMxYmViMWI2ODgxZjAyMWZjODllOGMzMTNlMzZiZTcxNGMwYTVmMGFlMjgyZTAw; st_data=9b80f6504addab01d07ceb92e015ae0ebe28e78229acc49a1f98e7a34252fd92f2aeedde3c579e4e4f02a455df0977b5c15672c5195c9410b11a8b75b3e465145d1dd0d6ed5fdba6e74990d871368657bf0b686990bd2ca20d998791dfe9bcfff9be93bfea398af7a04f734faa9edccee7100edefe85f35308e4b69ff4f8826c6c9c152b7c6cb1519b8cc28656e95d1c; st_key_id=17; st_sign=3f490e07; arialoadData=false; XFCS=CB163ECD8A688436403FE2DF9F662E748A0653C7AC1132A59E07E672FE325114; XFT=tRyi3rjHxHv/XW9HV0UKL6qjvLyrL/Y3UxrSt/60Mis=; RT="z=1&dm=baidu.com&si=7f3fb8ab-5fc5-4d65-8288-c00a318a5d69&ss=lz6jya55&sl=2&tt=4ix&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4l9&ul=ccb"'

# 请求头信息，定义为全局方便重用
headers = {
    "User-Agent": "Firefox/92.0",  # 替换为你的UA
    "Referer": "https://tieba.baidu.com/",
    "Cookie": tieba,  # 替换为你的cookie
}


# 从HTML中获取tbs参数和贴吧关注列表
def getTiebaInfo():
    try:
        url = "https://tieba.baidu.com/"

        # 发送请求，下载贴吧HTML页面
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        html = response.text

        # 从HTML中提取tbs参数
        tbs = getTbs(html)

        # 从HTML中提取贴吧关注列表
        forums = getAllForums(html)

        return {"forums": forums, "tbs": tbs}
    except Exception as e:
        print("获取贴吧数据失败，原因:", e)
        return None


# 用正则表达示从HTML中提取参数 tbs 的值
def getTbs(html):
    # 正则表达式学得不太好，用得有点呆板，凑合用
    match = re.search(r'PageData.tbs = "(.*)";PageData.is_iPad', html)
    if match:
        tbs = match.group(0).split('"')[1]
        return tbs
    return None


# 获取关注的贴吧列表
def getAllForums(html):
    #  _.Module.use('spage/widget/forumDirectory', {"forums": [...],"directory": {}})
    match = re.search(r'{"forums":\[.*\],"directory"', html)
    if match:
        data = match.group(0)
        forums = json.loads(data[data.find('['):data.rfind("]") + 1])
        return forums
    return None


# 逐个吧签到
def tiebaSigninOneByOne(tiebaInfo):
    # 签到接口
    signin_url = "https://tieba.baidu.com/sign/add"
    tbs = tiebaInfo.get("tbs")

    # 统计结果
    success_count = 0
    fail_count = 0

    # 签到
    for forum in tiebaInfo.get("forums"):
        # 跳过已经签到的贴吧，减少请求次数，防止验证码
        is_sign = forum.get("is_sign")
        forum_name = forum.get("forum_name")
        if is_sign == 1:
            print("{}吧已经签到,跳过".format(forum_name))
            continue

        # 构建请求数据
        sigin_data = {
            "ie": "utf-8",
            "kw": forum_name,
            "tbs": tbs,
        }

        try:
            # 发送请求签到
            response = requests.post(
                url=signin_url, data=sigin_data, headers=headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            content = response.json()

            # 判断签到结果，打印消息
            if content.get("no") == 0:
                success_count += 1
                print("{}吧签到成功".format(forum_name))
            else:
                fail_count += 1
                print("{}吧签到失败，失败原因：{}".format(
                    forum_name, content.get("error")))
        except Exception as e:
            fail_count += 1
            print("Error: {}吧签到发生错误，{}".format(forum_name, e))

        # 随机睡眠1-5秒，防止弹验证码，自动化不追求速度，一切求稳
        second = random.randint(1, 5)
        time.sleep(second)

    print("本次签到成功%d个，失败%d个" % (success_count, fail_count))
    info = "本次签到成功%d个，失败%d个" % (success_count, fail_count)
    QLAPI.notify('百度贴吧签到提醒', '{}'.format(info))


# 主方法
def baidu_tieba():
    print("-----------百度贴吧开始签到-------------")
    tiebaInfo = getTiebaInfo()
    if tiebaInfo:
        tiebaSigninOneByOne(tiebaInfo)
    else:
        print("签到失败")
    print("-----------百度贴吧签到结束-------------")


if __name__ == "__main__":
    baidu_tieba()
