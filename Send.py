#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Fy
new Env('QQ推送');
"""
import json

import requests


class PrivateMessage:
    def __init__(self):
        self.api_url = "http://e5914m9946.oicp.vip:3000/send_private_msg"

    def send_private_message(self, user_id, message):
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        return response.json()

    def send_recive_message(self, user_id, msg_id, message):
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "reply",
                    "data": {
                        "id": msg_id
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        return response.json()


class GroupMessage:
    def __init__(self):
        self.api_url = "http://e5914m9946.oicp.vip:3000/send_group_msg"

    def send_group_message(self, group_id, message):
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        return response.json()

    def send_recive_message(self, group_id, msg_id, message):
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "reply",
                    "data": {
                        "id": msg_id
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        return response.json()

    def send_at_message(self, group_id, user_id, message):
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "at",
                    "data": {
                        "qq": user_id
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        })
        
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        return response.json()

'''
if __name__ == "__main__":
    responder_pri = PrivateMessage()
    responder_pri.send_private_message("657769008", '你好！有什么可以帮助你的吗？')
    responder_gro = GroupMessage()
    #responder_gro.send_group_message("340576690", '你好！有什么可以帮助你的吗？')
    responder_gro.send_at_message("340576690", '657769008',"nihao ")
'''