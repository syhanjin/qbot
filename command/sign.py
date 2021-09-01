# coding=utf-8
from handles.client import send_msg
# from handles.client import send_msg
import pymongo
import os
from PIL import Image, ImageDraw, ImageFont
import random
import datetime

NAME = ''

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']
userdb = client['user']

root_path = os.path.join('.', 'res', 'sign')
card_ratio = 16 / 9
def rand(st, ed): return random.random()*(ed-st) + st


def putText(draw, x, y, text: 'str | tuple', font='微软雅黑', fontsize=16, fill=(0, 0, 0), border=0, borderFill=(0, 0, 0)):
    font = ImageFont.truetype(font, size=fontsize)
    if type(text) == type(()):
        tmp = text
        text = ''
        for i in tmp:
            text += str(i) + ' '
    text = str(text)
    if border > 0:
        # 文字阴影
        # thin border
        draw.text((x-border, y), text, font=font, fill=borderFill)
        draw.text((x+border, y), text, font=font, fill=borderFill)
        draw.text((x, y-border), text, font=font, fill=borderFill)
        draw.text((x, y+border), text, font=font, fill=borderFill)
        # thicker border
        draw.text((x-border, y-border), text, font=font, fill=borderFill)
        draw.text((x+border, y-border), text, font=font, fill=borderFill)
        draw.text((x-border, y+border), text, font=font, fill=borderFill)
        draw.text((x+border, y+border), text, font=font, fill=borderFill)
    draw.text((x, y), text, font=font, fill=fill)
    return draw.textsize(text, font=font, spacing=0)


def create_data(msg):
    data = {'qq': msg['user_id'], 'group': msg['group_id']}
    data['favorability'] = 0    # 好感度
    data['favorLevel'] = 0      # 好感等级
    data['continuity'] = 0      # 连续签到
    data['last'] = None         # 上次签到时间
    data['coin'] = 0            # 硬币
    return data


def generate_card(msg, data):
    # 信息变更
    now = datetime.datetime.now()
    # 今天凌晨
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute,
                                         seconds=now.second, microseconds=now.microsecond)

    if data.get('last') and data.get('last') + datetime.timedelta(hours=24) >= zeroToday:
        data['continuity'] += 1
    else:
        data['continuity'] = 1
    last = data['last']
    data['last'] = now
    fav = db.favlvl.find_one({'lvl': data['favorLevel']})
    favorability = float(format(rand(fav['fav'][0], fav['fav'][1]), '.2f'))
    coin = int(rand(5, 20))
    data['favorability'] += favorability
    data['coin'] += coin
    if data['favorability'] > fav['max']:
        data['favorLevel'] += 1

    # 生成图片
    # region 随机背景
    bg = os.path.join(root_path, 'H', str(random.randint(1, 30))+'.jpg')
    img = Image.open(bg)
    img = img.resize((1920, 1080), Image.ANTIALIAS)
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # endregion
    # region 构造画布
    draw = ImageDraw.Draw(tmp)
    fillcolor = '#3e3e3e'
    fontpath = os.path.join('.', 'res', 'sign', 'fonts',
                            'LXGWWenKai-Regular.ttf')
    draw.rectangle((0, 400, 1920, 1080), fill=(216, 216, 216, 216))
    # endregion

    # region 输出用户名 && QQ && sakuyark
    y = 10
    y += putText(draw, 40, y, msg['sender']['card'], font=fontpath,
                 fill=(255, 255, 255), fontsize=128, border=1.5)[1]
    y += putText(draw, 40, y, ('QQ:', msg['user_id']), font=fontpath,
                 fill=(255, 255, 255), fontsize=96, border=1.5)[1]
    if data.get('user'):
        putText(draw, 40, y, ('Sakuyark:', data['user']), font=fontpath, fill=(
            255, 255, 255), fontsize=96, border=1.5)
    # endregion
    # region 输出连签
    x = 40
    x += putText(draw, x, 430, u"Accumulative check-in for",
                 font=fontpath, fontsize=60)[0]
    x += 15
    x += putText(
        draw, x, 410, data['continuity'],
        font=fontpath, fill='#ff00ff', fontsize=80,
        border=1, borderFill=(200, 0, 200)
    )[0]
    x += 15
    putText(draw, x, 430, 'days',
            font=fontpath, fontsize=60)
    # endregion
    # region 输出上次签到时间
    '''
    x = 1180
    x += putText(draw, x, 430, u"上次签到", font=fontpath, fontsize=60)[0]
    x += 30
    putText(draw, x, 430, last.__format__('%Y-%m-%d') if(last)
            else '无', font=fontpath, fontsize=60, fill=(216, 64, 64))
    '''
    # endregion

    # region 左侧 头像

    # endregion

    # region 中间 当前信息
    x, y = 400, 600
    # 分割线
    draw.line((x, y, x, 950), fill='#000', width=3)
    # 内容
    x += 50
    y += 20
    y += putText(draw, x, y, ('当前好感度 :',
                 data['favorability']), font=fontpath, fontsize=48)[1]
    y += 15
    dx, h = 15, 40
    draw.rectangle((x + dx, y, x + dx + 360, y + h), fill='#fff')
    draw.ellipse((x + dx + 340, y, x + dx+380, y + h), fill='#fff')
    w = data['favorability'] / fav['max'] * 340 + 40
    draw.rectangle((x + dx, y, x + dx + w - 20, y + h), fill='#f0f')
    draw.ellipse((x + dx + w - 40, y, x + dx + w, y + h), fill='#f0f')
    y += h+15
    y += putText(
        draw, x, y,
        ('· 与', NAME, '的关系 :', fav['label']),
        font=fontpath, fontsize=36
    )[1]
    y += putText(
        draw, x, y,
        ('· ', NAME, '对你的态度 :', fav['attitude']),
        font=fontpath, fontsize=36
    )[1]
    y += putText(
        draw, x, y,
        ('· 关系提升还需要:', fav['max'] - data['favorability'], '好感度'),
        font=fontpath, fontsize=36
    )[1]
    y += 15
    y += putText(
        draw, x, y,
        ('时间: ', now.__format__('%Y-%m-%d %a %H:%M')),
        font=fontpath, fontsize=48
    )[1]
    # endregion

    # region 右侧 今日签到信息 全部信息
    x, y = 1150, 430
    y += putText(draw, x, y, '今日签到', font=fontpath, fontsize=72)[1]
    x += 50
    y += 15
    txy = putText(draw, x, y, '好感度', font=fontpath, fontsize=60)
    putText(draw, x + 350, y, ('+', favorability),
            font=fontpath, fontsize=60, fill=(128, 64, 64))
    y += txy[1]
    y += 15
    txy = putText(draw, x, y, '金币', font=fontpath, fontsize=60)
    putText(draw, x + 350, y, ('+', str(coin)),
            font=fontpath, fontsize=60, fill=(128, 64, 64))
    y += txy[1] + 60
    y += putText(draw, x, y,
                 ('金币总数:', data['coin']), font=fontpath, fontsize=60)[1]
    # endregion

    # region 输出水印
    putText(draw, 1750, 20, now.__format__('%m/%d'),
            font=fontpath, fill=(255, 255, 255), fontsize=48,
            border=1
            )
    putText(draw, 1600, 1020, 'Sakuyark@2021',
            font=fontpath, fill=(128, 128, 128), fontsize=36)
    # endregion

    # region 合成并保存
    img = Image.alpha_composite(img.convert('RGBA'), tmp)
    img = img.convert("RGB")
    out_path = os.path.join(root_path, 'cards', now.__format__(
        '%Y%m%d%H%M%S')+str(random.randint(10, 99))+'.jpg')
    img.save(out_path)
    # endregion
    return data, os.path.abspath(out_path)


def main(msg, args=None):
    data = db.sign.find_one({'qq': msg['user_id'], 'group': msg['group_id']})
    '''
    now = datetime.datetime.now()
    if (
        now
        - datetime.timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
            microseconds=now.microsecond
        )
    ) == (
            data['last']
            - datetime.timedelta(
                hours=data['last'].hour,
                minutes=data['last'].minute,
                seconds=data['last'].second,
                microseconds=data['last'].microsecond
            )
    ):
        send_msg({
            'msg_type': 'group',
            'number': msg['group_id'],
            'msg': '[CQ=at, qq='+str(msg['user_id'])+'] 你今天已经签过到了，明天再来吧~~~'
        })
    '''
    flag = False
    if data == None:
        data = create_data(msg)
        flag = True
    else:
        sydata = userdb.userdata.find_one({'qq': msg['user_id']})
        if sydata:
            data['user'] = sydata.get('user')
    data, img = generate_card(msg, data)
    if flag:
        db.sign.insert_one(data)
    else:
        db.sign.update_one(
            {'qq': msg['user_id'], 'group': msg['group_id']}, {'$set': data})
    send_msg({
        'msg_type': 'group',
        'number': msg['group_id'],
        'msg': '[CQ=image, file='+img+']'
    })
    return
