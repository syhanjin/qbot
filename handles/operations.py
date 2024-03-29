# coding=utf-8
from handles.msg_handle import *
import requests
import logging
import pymongo
import datetime

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']


template_data = {
    'favorability': 0,      # 好感度
    'coin': 0,              # 硬币
    'card_warn': 0          # 名片警告次数
}


def create_user_data(group_id, user_id):
    import copy
    data = copy.deepcopy(template_data)
    data['group_id'] = group_id
    data['user_id'] = user_id
    return data


def update_user_data(data):
    for k, v in template_data.items():
        if k not in data:
            data[k] = v
    return data


def create_msg_data(msg):
    data = {}
    data['group_id'] = get_group_id(msg)
    data['user_id'] = get_user_id(msg)
    data['time'] = datetime.datetime.now()
    data['msg_id'] = msg['message_id']
    return data


def get_admin(msg):
    if msg['user_id'] == 2493288137:
        return {
                'user_id': str(get_user_id(msg)),
                'group_id': str(get_group_id(msg)),
                'admin': 5
            }
    admin = db.admin.find_one({
        '$or': [
            {
                'user_id': str(get_user_id(msg)),
                'group_id': str(get_group_id(msg))
            },
            {
                'user_id': str(get_user_id(msg)),
                'admin': {'$gte': 4}
            }
        ]
    })
    if not admin:
        if get_role(msg) == 'admin':
            # 是群管理，自动生成管理等级为2的权限字串
            admin = {
                'user_id': str(get_user_id(msg)),
                'group_id': str(get_group_id(msg)),
                'admin': 2
            }
        if get_role(msg) == 'owner':
            # 是群主，自动生成管理等级为3的权限字串
            admin = {
                'user_id': str(get_user_id(msg)),
                'group_id': str(get_group_id(msg)),
                'admin': 3
            }
    return admin


def logging_put(info):
    logging.basicConfig(
        filename='robot.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.info(info)


def group_ban(group_id, user_id, duration=0):
    if user_id == 'all':
        if duration > 0:
            payload = '/set_group_whole_ban?group_id=' + \
                str(group_id)+'&enable=true'
            logging_put('群['+str(group_id)+']禁言')
        else:
            payload = '/set_group_whole_ban?group_id=' + \
                str(group_id)+'&enable=false'
            logging_put('群['+str(group_id)+']解禁')
    else:
        payload = '/set_group_ban?group_id=' + \
            str(group_id)+'&user_id='+str(user_id)+'&duration='+str(duration)
        logging_put('群['+str(group_id)+']禁言[' +
                    str(user_id)+']'+str(duration)+'秒')
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        logging_put('禁言失败')
        return False
    return True


def delete_msg(msg_id):
    # 撤回消息
    payload = '/delete_msg?message_id='+str(msg_id)
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        return False
    return True


def get_group_member_list(group_id):
    # 获取群成员列表
    payload = '/get_group_member_list?group_id='+str(group_id)
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        return False
    return r.json()


def group_kick(group_id, user_id):
    # 踢出群聊
    payload = '/set_group_kick?group_id=' + \
        str(group_id)+'&user_id='+str(user_id)
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        return False
    return True


def set_group_add_request(flag, sub_type, approve='true'):
    # 处理加群请求
    payload = '/set_group_add_request?flag=' + \
        str(flag)+'&subtype='+str(sub_type)+'&approve='+str(approve)
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        return False
    return True
