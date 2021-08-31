
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

db.drop_collection('favlvl')
db.create_collection('favlvl')
db.favlvl.insert_many([
    {'lvl': -1, 'max': 0, 'label': '陌生人', 'attitude': '排斥', 'fav': (0.2, 0.5)},
    {'lvl': 0, 'max': 10, 'label': '陌生人', 'attitude': '正常', 'fav': (0.5, 1)}
])
