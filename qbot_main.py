# coding=utf-8
from handles import sever, msg_handle
import logging


def logging_put(info):
    logging.basicConfig(
        filename='robot.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.info(info)


# ----- ----- ----- -----

def message_handle(msg):

    return


def notice_handle(msg):

    return


def request_handle(msg):

    return


def default():

    return

# ----- ----- ----- -----


def msg_handle(msg):
    post_type = msg_handle.get_post_type(msg)  # 获取上报类型
    if post_type == 'message':  # 消息事件
        message_handle(msg)
    elif post_type == 'notice':  # 通知事件
        notice_handle(msg)
    elif post_type == 'request':  # 请求事件
        request_handle(msg)
    else:
        default(msg)


def main():
    while True:
        all_messages = sever.rev_msg()
        try:
            msg_handle(all_messages)
        except BaseException as e:
            logging_put(e)
            print(e)
            continue


if __name__ == '__main__':
    main()
