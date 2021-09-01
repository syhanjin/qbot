from handles.client import send_msg
import command.sign

# 微型指令
from handles import operations


def group_ban(msg, cmd):
    if not operations.is_admin(msg['user_id']):
        send_msg({
            'msg': '你不是管理员，无权进行操作',
            'number': msg['group_id'],
            'msg_type': 'group'
        })
        return
    m = cmd.match('^禁言 *\[CQ:at,qq=(\d+)[^\]]*\]$ *(\d+)?')
    qq = m.group(1)
    duration = m.group(2)
    if not duration:
        duration = 60
    operations.group_ban(msg['group_id'], qq, duration)
