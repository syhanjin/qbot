# coding=utf-8
from handles.msg_handle import *
import requests
import logging
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

def get_admin(msg):
    return db.admin.find_one({
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
            payload = '/set_group_whole_ban?group_id='+str(group_id)+'&enable=true'
            logging_put('群['+str(group_id)+']禁言')
        else:
            payload = '/set_group_whole_ban?group_id='+str(group_id)+'&enable=false'
            logging_put('群['+str(group_id)+']解禁')
    else:
        payload = '/set_group_ban?group_id='+str(group_id)+'&user_id='+str(user_id)+'&duration='+str(duration)
        logging_put('群['+str(group_id)+']禁言['+str(user_id)+']'+str(duration)+'秒')
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        logging_put('禁言失败')
        return False
    return True