# coding=utf-8
import requests
import logging
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']
def logging_put(info):
    logging.basicConfig(
        filename='robot.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.info(info)

def group_ban(group_id, user_id, duration=0):
    if user_id == 'all':
        if duration != 0:
            r = requests.get('/set_group_whole_ban?group_id='+str(group_id)+'&enable=true')
            logging_put('群['+str(group_id)+']禁言')
        else:
            r = requests.get('/set_group_whole_ban?group_id='+str(group_id)+'&enable=false')
            logging_put('群['+str(group_id)+']解禁')
    else:
        payload = '/set_group_ban?group_id='+str(group_id)+'&user_id='+str(user_id)+'&duration='+str(duration)
        logging_put('群['+str(group_id)+']禁言['+str(user_id)+']'+str(duration)+'秒')
        r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        logging_put('禁言失败')
        return False
    return True

def is_admin(qq):
    return bool(db.admin.find_one({'user_id':str(qq)}))