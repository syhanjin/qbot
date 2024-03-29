# coding=utf-8
# 该文件主要是对主文件中得到的字典中得到关键数据的方法


# 获取上报类型：message、notice、request
def get_post_type(msg): return msg.get('post_type')


# 获取信息类型 群聊/私聊 group/private
def get_message_type(msg): return msg.get('message_type')


# 获取群号/私聊qq号
def get_number(msg):
    if get_message_type(msg) == 'group':
        return msg.get('group_id')
    elif get_message_type(msg) == 'private':
        return msg.get('user_id')


# 获取角色
def get_role(msg): return msg.get('sender').get(
    'role') if (msg.get('sender')) else None


# 获取群号
def get_group_id(msg): return msg.get('group_id')


# 获取QQ号
def get_user_id(msg): return msg.get('user_id')


# 获取信息发送者的QQ号
def get_user_id(msg): return msg.get('user_id')


# 获取发送的信息
def get_raw_message(msg): return msg.get('raw_message')


# 得到通知类型
def get_notice_type(msg): return msg.get('notice_type')


# 得到请求类型
def get_request_type(msg): return msg.get('request_type')
