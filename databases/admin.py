
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['qbot']

db.drop_collection('admin')
db.create_collection('admin')
db.admin.insert_many([
    {'user_id': '2819469337', 'admin': 5}
])