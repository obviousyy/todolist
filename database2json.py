import json

import mongodb

todolist = mongodb.MongoDBPool.get_mongodb_pool()

jsondata = dict()

datas = todolist.find()
i = 0

obj2id = dict()

for data in datas:
    obj2id[data['_id']] = str(i)
    data['_id'] = str(i)
    if 'begin' in data:
        data['begin'] = data['begin'].strftime('%Y-%m-%d %H:%M:%S')
    if 'end' in data:
        data['end'] = data['end'].strftime('%Y-%m-%d %H:%M:%S')
    jsondata[str(i)] = data
    i += 1

for (_, data) in jsondata.items():
    if 'parent_task' in data:
        data['parent_task'] = obj2id[data['parent_task']]
    if 'subtask' in data:
        subtasks = []
        for subtask in data['subtask']:
            subtasks.append(obj2id[subtask])
        data['subtask'] = subtasks

pass

with open("data.json", "w") as f:
    json.dump(jsondata, f)
