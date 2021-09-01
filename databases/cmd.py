
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

db.drop_collection('cmd')
db.create_collection('cmd')
db.cmd.insert_many([
    {'key': '^签到$', 'value': 'sign', 'type': 'function', 'group': True},
    {'key': '^禁言 *\[CQ:at,qq=(\d+)[^\]]*\] *(\d+)?$', 'value': 'group_ban', 'type': 'function', 'group': True, 'inline': True},
])