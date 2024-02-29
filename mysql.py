import traceback

import pymysql


class MysqlUtil:
    def __init__(self):
        host = 'localhost'
        user = 'root'
        password = '3125'
        database = 'todolist'
        self.db = pymysql.connect(host=host, user=user, password=password, db=database)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()

    def fetchone(self, sql):
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()
        return result

    def fetchall(self, sql):
        result = None
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()
        return result

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()


def get_son(id):
    sql = 'SELECT * FROM todo WHERE parent_id=%s' % str(id)
    db = MysqlUtil()
    son = db.fetchall(sql)
    return son


def delete_point(id):
    son = get_son(id)
    if son is None:
        db = MysqlUtil()
        sql = 'DELETE FROM todo WHERE id=%s' % str(id)
        db.delete(sql)
    else:
        for i in son:
            delete_point(i['id'])
        db = MysqlUtil()
        sql = 'DELETE FROM todo WHERE id=%s' % str(id)
        db.delete(sql)


def create_point(title, content, ddl, priority=0, count=0, parent_id=None):
    sql = "INSERT INTO todo(title, content, ddl, priority) VALUES('%s', '%s', '%s', %s)" % (title, content, ddl, priority)
    db = MysqlUtil()
    db.insert(sql)
    sql = 'SELECT MAX(id) FROM todo'
    db = MysqlUtil()
    id = db.fetchone(sql)
    id = id['MAX(id)']
    if parent_id is not None:
        sql = 'UPDATE todo SET parent_id=%s WHERE id=%s' % (str(parent_id), str(id))
        db = MysqlUtil()
        db.update(sql)
    if count != 0:
        db = MysqlUtil()
        sql = 'UPDATE todo SET count=%s WHERE id=%s' % (str(count), str(id))
        db.update(sql)
    return id


def edit_point(id, title=None, content=None, ddl=None, priority=0, count=0):
    if content is not None:
        sql = "UPDATE todo SET content='%s' WHERE id=%s" % (content, str(id))
        db = MysqlUtil()
        db.update(sql)
    if ddl is not None:
        sql = "UPDATE todo SET ddl='%s' WHERE id=%s" % (ddl, str(id))
        db = MysqlUtil()
        db.update(sql)
    if priority is not None:
        sql = 'UPDATE todo SET priority=%s WHERE id=%s' % (str(priority), str(id))
        db = MysqlUtil()
        db.update(sql)
    if title is not None:
        sql = "UPDATE todo SET title='%s' WHERE id=%s" % (title, str(id))
        db = MysqlUtil()
        db.update(sql)
    if count is not None:
        db = MysqlUtil()
        sql = 'UPDATE todo SET count=%s WHERE id=%s' % (str(count), str(id))
        db.update(sql)


def finish(id):
    sql = 'UPDATE todo SET is_finish=1 WHERE id=%s' % str(id)
    db = MysqlUtil()
    db.update(sql)


def get_id(id):
    sql = 'SELECT * FROM todo WHERE id=%s' % str(id)
    db = MysqlUtil()
    result = db.fetchone(sql)
    return result


def set_priority(id, flag):
    sql = 'UPDATE todo SET is_finish=%s WHERE id=%s' % (str(flag), str(id))
    db = MysqlUtil()
    db.update(sql)


def get_priority(id):
    db = MysqlUtil()
    sql = "SELECT priority FROM todo WHERE id=%s" % str(id)
    priority = db.fetchone(sql)
    priority = priority['priority']
    return priority
