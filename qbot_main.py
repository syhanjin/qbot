# coding=utf-8
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


def group_msg_handle(msg):
    content = get_raw_message(msg)
    # 指令检测
    cmd_data = db.cmd.find_one({'$where': '"'+content+'".match(this.key)', 'group': True})
    if cmd_data != None:
        logging_put('收到指令['+msg['group_id']+']:'+content)
        getattr(command, cmd_data['value']).main(msg, content)
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

    return


def request_handle(msg):

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
