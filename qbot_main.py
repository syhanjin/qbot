# coding=utf-8
import datetime
from flask import Flask, request
# from handles import sever
from handles.client import send_msg
from handles.msg_handle import *
from handles.operations import *
import command
import logging
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

# ----- ----- ----- -----


def create_msg_data(msg):
    data = {}
    data['group_id'] = get_group_id(msg)
    data['user_id'] = get_user_id(msg)
    data['time'] = datetime.datetime.now()
    data['msg_id'] = msg['message_id']
    return data

# ----- ----- ----- -----


def private_msg_handle(msg):
    content = get_raw_message(msg)
    # 指令检测
    cmd_data = db.cmd.find_one({'key': content.split(' ', 1), 'private': True})
    if cmd_data != None:
        if cmd_data['type'] == 'function':
            getattr(command, cmd_data['value']).main(
                msg, content.split(' ', 1)[1])

    # 从数据库中查找答案
    else:

        pass

    return


def count_group_msg(msg):
    # 统计群消息
    group_id, user_id = get_group_id(msg), get_user_id(msg)
    data = create_msg_data(msg)
    data_i4 = db.msg.find({
        'group_id':group_id,
        'user_id':user_id,
        'time' :{'$gte': data['time'] - datetime.timedelta(seconds=4)}
    })
    data_i4_count = data_i4.count()
    admin = get_admin(msg)
    if not admin and data_i4_count >= 3:
        # 4秒内发送消息4次则禁言 60s
        group_ban(group_id, user_id, 60)
        # 执行消息撤回
        for i in list(data_i4):
            delete_msg(i['msg_id'])
        delete_msg(msg['message_id'])
    # 关键词拦截 --等待网站控制台
    
    

    db.msg.insert_one(data)
    return


def group_msg_handle(msg):
    content = get_raw_message(msg)
    count_group_msg(msg)
    # 指令检测
    cmd_data = db.cmd.find_one(
        {'$where': '"'+content+'".match(this.key)', 'group': True})
    if cmd_data != None:
        logging_put('收到指令['+str(msg['group_id'])+']:'+content)
        if cmd_data.get('inline'):
            getattr(command, cmd_data['value'])(msg, content, cmd_data)
        else:
            getattr(command, cmd_data['value']).main(msg, content, cmd_data)
    # 从数据库中查找答案
    else:

        pass

    return


def message_handle(msg):
    logging_put("收到消息'"+get_raw_message(msg)+"'来自"+str(get_number(msg)))
    if get_message_type(msg) == 'private':
        private_msg_handle(msg)
    elif get_message_type(msg) == 'group':
        group_msg_handle(msg)
    return


def notice_handle(msg):
    if get_notice_type(msg) == 'group_increase':
        # 群成员增加
        send_msg({
            'msg': '欢迎新人入群[CQ:face,id=99][CQ:face,id=99][CQ:face,id=99]~~~\n有问题请先看群公告',
            'number': msg['group_id'],
            'msg_type': 'group'
        })
    return


def request_handle(msg):
    logging_put("收到请求 来自"+str(get_group_id(msg)))
    return


def default():

    return

# ----- ----- ----- -----


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.json:
        msg = request.json
        post_type = get_post_type(msg)  # 获取上报类型
        if post_type == 'message':  # 消息事件
            message_handle(msg)
        elif post_type == 'notice':  # 通知事件
            notice_handle(msg)
        elif post_type == 'request':  # 请求事件
            request_handle(msg)
        else:
            default()
    return 'OK'


app.debug = True
if __name__ == '__main__':
    app.run('127.0.0.1', 5701)
    # main()
