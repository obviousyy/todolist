import json
import os


class Json2Database:
    def __init__(self):
        if os.path.exists('./data.json'):
            with open('./data.json', 'r', encoding='utf-8') as db:
                self.data = json.load(db)
        else:
            self.data = {'max': 0}

    @staticmethod
    def check_condition(condition, data):
        for (key, value) in condition.items():
            if key == '_id':
                continue
            if value is None:
                if key in data:
                    return None
                else:
                    continue
            if key.find('.') != -1:
                parent = key[:key.find('.')]
                child = key[key.find('.') + 1:]
                if parent not in data:
                    return None
                if child not in data[parent]:
                    return None
                check = data[parent][child]
            else:
                if key not in data:
                    return None
                check = data[key]
            if isinstance(value, list):
                if value[0] == '$in':
                    flag = None
                    for i in range(len(value[1])):
                        if value[1][i] == check:
                            flag = True
                            break
                    if not flag:
                        return None
                elif value[0] == '$nin':
                    flag = None
                    for i in range(len(value[1])):
                        if value[1][i] == check:
                            flag = True
                            break
                    if not flag:
                        return None
                elif value[0] == '$lt':
                    if check >= value[1]:
                        return None
                elif value[0] == '$gt':
                    if check <= value[1]:
                        return None
                elif value[0] == '$lte':
                    if check > value[1]:
                        return None
                elif value[0] == '$gte':
                    if check < value[1]:
                        return None
                elif value[0] == '$ne':
                    if check == value[1]:
                        return None
            elif check != value:
                return None
        return True

    def find_one(self, condition):
        if '_id' in condition:
            if condition['_id'] is None:
                return None
            data = None
            if isinstance(condition['_id'], list):
                for i in range(len(condition['_id'])):
                    if condition['_id'][i] in self.data:
                        data = self.data[condition['_id'][i]]
                        break
                if data is None:
                    return None
            else:
                if condition['_id'] in self.data:
                    data = self.data[condition['_id']]
            if data is not None and self.check_condition(condition, data):
                return data
            else:
                return None
        else:
            for (i, data) in self.data.items():
                if i == 'max':
                    continue
                if self.check_condition(condition, data):
                    return data
            return None

    def find(self, condition):
        if '_id' in condition:
            if condition['_id'] is None:
                return None
            datas = []
            if isinstance(condition['_id'], list):
                for i in range(len(condition['_id'])):
                    if condition['_id'][i] in self.data:
                        data = self.data[condition['_id'][i]]
                        if self.check_condition(condition, data):
                            datas.append(data)
                return datas
            else:
                if condition['_id'] in self.data:
                    data = self.data[condition['_id']]
                    if self.check_condition(condition, data):
                        return [data]
                    else:
                        return None
                else:
                    return None
        else:
            result = []
            for (i, data) in self.data.items():
                if i == 'max':
                    continue
                if self.check_condition(condition, data):
                    result.append(data)
            return result

    def update_data(self, data, new):
        if new[0] == '$set':
            for (key, value) in new[1].items():
                if key.find('.') != -1:
                    parent = key[:key.find('.')]
                    child = key[key.find('.') + 1:]
                    if parent not in data:
                        data[parent] = dict()
                    data[parent][child] = value
                else:
                    data[key] = value
        elif new[0] == '$unset':
            for i in range(len(new[1])):
                key = new[1][i]
                if key.find('.') != -1:
                    parent = key[:key.find('.')]
                    child = key[key.find('.') + 1:]
                    if parent in data and child in data[parent]:
                        del data[parent][child]
                else:
                    if key in data:
                        del data[key]
        elif new[0] == '$addToSet':
            for (key, value) in new[1].items():
                if key.find('.') != -1:
                    parent = key[:key.find('.')]
                    child = key[key.find('.') + 1:]
                    if parent not in data:
                        data[parent] = dict()
                    s = set(data[parent][child])
                    s.update(value)
                    data[parent][child] = list(s)
                else:
                    s = set(data[key])
                    s.update(value)
                    data[key] = list(s)
        elif new[0] == '$pull':
            for (key, value) in new[1].items():
                if key.find('.') != -1:
                    parent = key[:key.find('.')]
                    child = key[key.find('.') + 1:]
                    if parent not in data:
                        data[parent] = dict()
                    s = set(data[parent][child])
                    s.discard(value)
                    data[parent][child] = list(s)
                else:
                    s = set(data[key])
                    s.discard(value)
                    data[key] = list(s)
        elif new[0] == '$inc':
            for (key, value) in new[1].items():
                if key.find('.') != -1:
                    parent = key[:key.find('.')]
                    child = key[key.find('.') + 1:]
                    if parent not in data:
                        data[parent] = dict()
                    data[parent][child] += value
                else:
                    data[key] += value
        self.data[data['_id']] = data

    def update_one(self, condition, new):
        data = self.find_one(condition)
        if data:
            self.update_data(data, new)
            return True
        else:
            return False

    def update(self, condition, new):
        data = self.find(condition)
        if data:
            for i in range(len(data)):
                self.update_data(data[i], new)
            return True
        else:
            return False

    def insert_one(self, new):
        _id = str(self.data['max'])
        self.data['max'] += 1
        new['_id'] = _id
        self.data[_id] = new
        return _id

    def delete_one(self, condition):
        data = self.find_one(condition)
        if data:
            del self.data[data['_id']]
            return True
        else:
            return False

    def delete_many(self, condition):
        data = self.find(condition)
        if data:
            for i in range(len(data)):
                del self.data[data[i]['_id']]
            return True
        else:
            return False

    def save(self):
        with open("./data.json", "w") as f:
            json.dump(self.data, f)
