from pymongo import MongoClient


class MongoDBPool:
    db: MongoClient | None = None

    @classmethod
    def get_mongodb_pool(cls):
        if cls.db is None:
            cls.db = MongoClient(host='localhost', port=27017)
        return cls.db['todolist']['todolist']


if __name__ == '__main__':
    from bson import ObjectId
    todolist = MongoDBPool.get_mongodb_pool()
    type = todolist.find_one({'_id': ObjectId('65dc7bd07d06000036006df3')}, {'_id': 0, 'begin': 1, 'end': 1, 'cycle.type': 1})
    type['type'] = type['cycle']['type']
    del type['cycle']
    print(type)

