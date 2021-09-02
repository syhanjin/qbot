import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

db.drop_collection('increase')
db.create_collection('increase')
db.increase.insert_many([
    {'group_id': '457263503', 'msg':
     '''[AT] 欢迎新同学！
改名片！改名片！重要的事情说两遍！
不改的管理员会t人
【机器人自动识别名片中】
请规范格式，新高一请在名片中出现"新高一"三个字
老学员请在名片中包含 c/k开头的班级 [忽略大小写]
包含以下字段的也可
高二，高三，高四，墙$(表示这个字在最后)，社$，社长$, 站$
只要满足正则表达式 /新高一|[ck]\d{2,4}|高[二三四]|[墙社站]$|社长$/i 即可
'''}
])

db.drop_collection('card')
db.create_collection('card')
db.card.insert_many([
    {
        'group_id': '457263503',
        'reg': '新高一|[ck]\d{2,4}|高[二三四]|[墙社站]$|社长$',
        'warn': 3, # 警告次数
        'interval': 3600, # 单位 s
        # 'operation': 'kick', # 操作：踢出
    },{
        'group_id': '1003132999',
        'reg': '新高一|[ck]\d{2,4}|高[二三四]|[墙社站]$|社长$',
        'warn': 3, # 警告次数
        'interval': 3600, # 单位 s
        # 'operation': 'kick', # 操作：踢出
    }
])
