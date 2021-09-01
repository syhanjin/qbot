# coding=utf-8
# 在5700端口的角度上，我们是发送消息的客户端
import requests
import json


ip = '127.0.0.1'

# 通过发送http请求让傀儡QQ发送消息
# 在参数resp_dict中，我们要指定好类型、回复信息、账号（群号）


def send_msg(resp_dict):

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "/send_group_msg?group_id=" + \
            str(number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + \
            ip+":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "/send_private_msg?user_id=" + \
            str(number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + \
            ip+":5700\r\nConnection: close\r\n\r\n"
    print("发送"+payload)
    r = requests.get(payload.encode("utf-8"))
    if r.status_code != 200:
        print('发送失败')
    return 0
