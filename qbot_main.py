# coding=utf-8
from handles import sever
from handles.client import send_msg
from handles.msg_handle import *
import command
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


# ----- ----- ----- -----
def private_msg_handle(msg):
    content = get_raw_message(msg)
    # 指令检测
    cmd_data = db.cmd.find_one({'key': content.split(' ',1), 'private': True})
    if cmd_data != None:
        if cmd_data['type'] == 'function': 
            getattr(command, cmd_data['value']).main(msg, content.split(' ',1)[1])
        
    # 从数据库中查找答案
    else:

        pass

    return


def group_msg_handle(msg):
    content = get_raw_message(msg)
    # 指令检测
    cmd_data = db.cmd.find_one({'key': content, 'group': True})
    if cmd_data != None:
        getattr(command, cmd_data['value']).main(msg)
    # 从数据库中查找答案
    else:

        pass

    return


def message_handle(msg):
    logging_put("收到消息"+get_raw_message(msg)+"来自"+str(get_number(msg)))
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


def main():
    while True:
        msg = sever.rev_msg()
        print(msg)
        if msg:
            try:
                post_type = get_post_type(msg)  # 获取上报类型
                if post_type == 'message':  # 消息事件
                    message_handle(msg)
                elif post_type == 'notice':  # 通知事件
                    notice_handle(msg)
                elif post_type == 'request':  # 请求事件
                    request_handle(msg)
                else:
                    default(msg)
            except BaseException as e:
                logging_put(e)
                print(e)
                continue


if __name__ == '__main__':
    main()
