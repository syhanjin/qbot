# coding=utf-8
import requests
import logging
def logging_put(info):
    logging.basicConfig(
        filename='robot.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.info(info)

def group_ban(group_id, user_id, duration):
    payload = '/set_group_ban?group_id='+str(group_id)+'&user_id='+str(user_id)+'&duration='+str(duration)
    logging_put('群['+str(group_id)+']禁言['+str(user_id)+']'+str(duration)+'秒')
    r = requests.get('http://127.0.0.1:5700' + payload)
    if r.status_code != 200:
        logging_put('禁言失败')
        return False
    return True