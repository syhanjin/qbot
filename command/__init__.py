from handles.client import send_msg
import command.sign

# 微型指令
from handles import operations
import re
import json
import pymongo
import datetime
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

def group_ban(msg, cmd, cmd_data):
    if not operations.get_admin(msg):
        send_msg({
            'msg': '你不是管理员，无权进行操作',
            'number': msg['group_id'],
            'msg_type': 'group'
        })
        return
    m = re.match(cmd_data['key'], cmd)
    qq = m.group(1)
    duration = m.group(2)
    if not duration:
        duration = 60
    operations.group_ban(msg['group_id'], qq, duration)

def cancel_group_ban(msg, cmd, cmd_data):
    if not operations.get_admin(msg):
        send_msg({
            'msg': '你不是管理员，无权进行操作',
            'number': msg['group_id'],
            'msg_type': 'group'
        })
        return
    m = re.match(cmd_data['key'], cmd)
    qq = m.group(1)
    operations.group_ban(msg['group_id'], qq)


    
def test_cards(msg, cmd=None, cmd_data=None):
    if not operations.get_admin(msg):
        send_msg({
            'msg': '你不是管理员，无权进行操作',
            'number': msg['group_id'],
            'msg_type': 'group'
        })
        return
    group_id = str(msg['group_id'])
    reg = db.card.find_one({'group_id': group_id})
    if not reg:
        return False
    datas = operations.get_group_member_list(group_id)['data']
    wids = []
    flag = False
    for i in datas:
        card = i['card'] if(i.get('card')) else i['nickname']
        if not re.match(reg['reg'], card, re.I):
            user = db.user.find_one({'user_id':i['user_id'],'group_id':int(group_id)})
            if not user:
                user = operations.create_user_data(group_id, i['user_id'])
                user['card_warn'] = 1
                db.user.insert_one(user)
            else:
                db.user.update_one({'_id':user['_id']},{'$inc':{'card_warn':1}})
            if user['card_warn'] >= reg['warn']:
                operations.group_kick(group_id, i['user_id'])
                flag = True
            else:
                wids.append(i['user_id'])
    msg = '【群名片警告】\n'
    for i in wids:
        msg += '[CQ:at,qq='+i+']'
    msg += '请修改群名片，名片格式参见公告，三次警告后踢出\n'
    if flag: msg+='警告满'+str(reg['warn'])+'次的已t出'
    if flag or len(wids) > 0:
        send_msg({
            'number': group_id,
            'msg': msg,
            'msg_type': 'group'
        })
    return