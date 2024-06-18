# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QDataStream
from PyQt5.QtGui import QCursor, QDrag
from PyQt5.QtWidgets import QMenu, QMessageBox, QTreeWidgetItem, QHeaderView, QMainWindow, QTreeWidget
from bson import ObjectId
from dateutil.relativedelta import relativedelta

import mongodb
import todo

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

todolist = mongodb.MongoDBPool.get_mongodb_pool()


class CustomTreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        value1 = self.foreground(3)
        value2 = other.foreground(3)
        if value1 == value2:
            value1 = self.text(3)
            value2 = other.text(3)
            order = {'没空不做': 1, '有空再做': 2, '早做早超生': 3, '不可忘记': 4, '急急急': 5, '已完成': 0}
            if order[value1] != order[value2]:
                return order[value1] < order[value2]
            else:
                value1 = self.checkState(0)
                value2 = other.checkState(0)
                if value1 != value2:
                    return value1 > value2
                else:
                    value1 = self.text(2)
                    value2 = other.text(2)
                    if value1 != value2:
                        return value1 > value2
                    else:
                        value1 = self.text(1)
                        value2 = other.text(1)
                        return value1 > value2
        else:
            return value1 == QtGui.QBrush(QtGui.QColor('gray'))


class CustomTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.move_item = None
        self.old_parent = None
        self.setHeaderLabels(['Items'])
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)
        self.move_item = self.currentItem()
        self.old_parent = get_id(self.move_item.parent())

    def dropEvent(self, event):
        super().dropEvent(event)
        it = self.move_item
        _id = ObjectId(get_id(it))
        new_parent = get_id(it.parent())
        if self.old_parent:
            parent_id = ObjectId(self.old_parent)
            todolist.update_one({'_id': parent_id}, {'$pull': {'subtask': _id}})
            subtask = todolist.find_one({'_id': parent_id}, {'_id': 0, 'subtask': 1})
            if len(subtask['subtask']) == 0:
                todolist.update_one({'_id': parent_id}, {'$unset': {'subtask': ""}})
        if new_parent:
            parent_id = ObjectId(new_parent)
            subtask = todolist.find_one({'_id': parent_id}, {'_id': 0, 'subtask': 1})
            if 'subtask' in subtask and len(subtask['subtask']) > 0:
                todolist.update_one({'_id': parent_id}, {'$addToSet': {'subtask': _id}})
            else:
                todolist.update_one({'_id': parent_id}, {'$set': {'subtask': [_id]}})
            todolist.update_one({'_id': _id}, {'$set': {'parent_task': parent_id}})
        else:
            todolist.update_one({'_id': _id}, {'$unset': {'parent_task': ""}})
        self.expandItem(it.parent())


item_id = list()


def get_id(node):
    for i in item_id:
        if i[0] == node:
            return i[1]


def get_node(id):
    for i in item_id:
        if i[1] == id:
            return i[0]


class Ui_MainWindow(object):
    def __init__(self, app):
        super(Ui_MainWindow, self).__init__()
        self.app = app
        self.windows = list()
        self.root = None
        self.item = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = CustomTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setText(0, 'self')
        item_id.append((item_0, None))
        self.root = item_0
        self.treeWidget.setHeaderLabels(['概要', '开始时间', '结束时间', '优先级'])
        self.horizontalLayout.addWidget(self.treeWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        header = self.treeWidget.header()  # 获取表头
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.treeWidget.itemDoubleClicked.connect(self.show_assi)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_menu)
        self.treeWidget.expandItem(item_0)  # 展开添加的节点
        self.treeWidget.setSortingEnabled(True)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.treeWidget.itemChanged.connect(self.check)

        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(QTreeWidget.InternalMove)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "任务列表"))
        self.show()

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        super().dropEvent(event)

    def show(self):
        # db = mysql.MysqlUtil()
        # sql = "SELECT * FROM todo WHERE parent_id is null"
        # roots = db.fetchall(sql)
        roots = todolist.find({'parent_task': None})
        for i in roots:
            self.create_node(i, self.root)
        self.treeWidget.sortItems(3, Qt.DescendingOrder)

    def create_node(self, i, root):
        if i['cycle']['type'] > 0:
            self.new_day(i)
        node = CustomTreeWidgetItem(root)
        item_id.append((node, str(i['_id'])))
        node.setText(0, i['title'])
        if 'begin' in i:
            node.setText(1, i['begin'].strftime('%Y-%m-%d %H:%M'))
            now = datetime.today()
            if (i['cycle']['type'] != 1 and i['begin'] > now
                    or i['cycle']['type'] == 1 and i['cycle']['total_times'] == 0):
                self.treeWidget.blockSignals(True)
                node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
                self.treeWidget.blockSignals(False)
                node.setForeground(1, QtGui.QBrush(QtGui.QColor('gray')))
                node.setForeground(2, QtGui.QBrush(QtGui.QColor('gray')))
                node.setForeground(3, QtGui.QBrush(QtGui.QColor('gray')))
        else:
            node.setText(1, '')
        if 'end' in i:
            node.setText(2, i['end'].strftime('%Y-%m-%d %H:%M'))
        else:
            node.setText(2, '')
        self.set_priority(node, i['priority'])
        no_all_finish = False
        if 'subtask' in i and len(i['subtask']) > 0:
            # son = mysql.get_son(i['id'])
            son = i['subtask']
            all_no_finish = True
            for j in son:
                j = todolist.find_one({'_id': j})
                state1, state2 = self.create_node(j, node)
                no_all_finish = no_all_finish or state1
                all_no_finish = all_no_finish and state2
            if not all_no_finish:
                node.setCheckState(0, Qt.PartiallyChecked)
            else:
                node.setCheckState(0, Qt.Unchecked)
            if i['is_finish'] == 1:
                self.finish_node(str(i['_id']), False)
            if i['expend'] == 1 or (i['expend'] == 0 and no_all_finish):
                self.treeWidget.expandItem(node)
        else:
            if i['is_finish'] == 1:
                self.finish_node(str(i['_id']), False)
            elif i['is_finish'] == 0:
                self.set_gray(node, False)
            elif i['is_finish'] == -1:
                if 0 <= i['cycle']['type'] <= 1 and i['cycle']['finish_times'] > 0:
                    node.setCheckState(0, Qt.PartiallyChecked)
                else:
                    node.setCheckState(0, Qt.Unchecked)
                if node.foreground(1) != QtGui.QBrush(QtGui.QColor('gray')):
                    no_all_finish = True
        return no_all_finish, node.checkState(0) == Qt.Unchecked

    def show_menu(self):
        item = self.treeWidget.currentItem()
        menu = QMenu()
        id = get_id(item)
        result = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0})
        if result is None or result['is_finish'] != 1 and result['cycle']['type'] < 0:
            action = menu.addAction('添加子任务')
            action.triggered.connect(self.add_node)
        if item != self.root and result['is_finish'] != 1:
            action = menu.addAction('修改任务')
            action.triggered.connect(self.edit_node)
            if (result['cycle']['type'] == 2 and result['is_finish'] == -1
                    or 0 <= result['cycle']['type'] <= 1 and result['is_finish'] == -1 and result['cycle'][
                        'total_times'] > 0):
                action = menu.addAction('完成一次')
                action.triggered.connect(self.finish_once)
        if item != self.root:
            action = menu.addAction('删除任务')
            action.triggered.connect(self.delete_node)
            if 2 > result['cycle']['type'] >= 0 and result['cycle']['finish_times'] > 0:
                action = menu.addAction('取消完成一次')
                action.triggered.connect(self.un_finish_once)
        if item != self.root and item.childCount() != 0:
            action = menu.addAction('自动展开')
            action.triggered.connect(lambda: self.set_auto(True))
            action = menu.addAction('手动展开')
            action.triggered.connect(lambda: self.set_auto(False))
        menu.exec_(QCursor.pos())

    def set_item(self, dic):
        if dic != {}:
            self.item = dic
        else:
            self.item = None

    def add_node(self):
        item = self.treeWidget.currentItem()
        parent_id = get_id(item)
        parent = todolist.find_one({'_id': ObjectId(parent_id)},
                                   {'_id': 0, 'begin': 1, 'end': 1, 'cycle.type': 1, 'cycle.cyclicality': 1})
        ui1 = todo.Ui_todo(self.app, None, True, parent)
        ui1.show()
        self.windows.append(ui1)
        ui1.child_signal.connect(self.set_item)
        ui1.exec_()
        if self.item is not None:
            if 'is_finish' not in self.item:
                self.item['is_finish'] = -1
            if item != self.root:
                parent_id = get_id(item)
                self.item["parent_task"] = ObjectId(parent_id)
            self.item = self.new_day(self.item)
            node = CustomTreeWidgetItem(item)
            self.treeWidget.blockSignals(True)
            node.setText(0, self.item['title'])
            self.treeWidget.blockSignals(False)
            self.item['expend'] = 0
            if 'begin' in self.item:
                node.setText(1, self.item['begin'].strftime('%Y-%m-%d %H:%M'))
                now = datetime.today()
                if (self.item['cycle']['type'] != 1 and self.item['begin'] > now
                        or self.item['cycle']['type'] == 1 and self.item['cycle']['total_times'] == 0):
                    self.treeWidget.blockSignals(True)
                    node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
                    self.treeWidget.blockSignals(False)
                    node.setForeground(1, QtGui.QBrush(QtGui.QColor('gray')))
                    node.setForeground(2, QtGui.QBrush(QtGui.QColor('gray')))
                    node.setForeground(3, QtGui.QBrush(QtGui.QColor('gray')))
            else:
                node.setText(1, '')
            if 'end' in self.item:
                node.setText(2, self.item['end'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(2, '')
            self.set_priority(node, self.item['priority'])
            id = todolist.insert_one(self.item).inserted_id
            item_id.append((node, str(id)))
            if self.item['is_finish'] == 0:
                self.set_gray(node, False)
            elif self.item['is_finish'] == 1:
                self.finish_node(get_id(node), True)
            else:
                self.treeWidget.blockSignals(True)
                node.setCheckState(0, Qt.Unchecked)
                self.treeWidget.blockSignals(False)
            if item != self.root:
                parent_id = get_id(item)
                subtask = todolist.find_one({'_id': ObjectId(parent_id)}, {'_id': 0, 'subtask': 1})
                if 'subtask' in subtask and len(subtask['subtask']) > 0:
                    todolist.update_one({'_id': ObjectId(parent_id)}, {'$addToSet': {'subtask': id}})
                else:
                    todolist.update_one({'_id': ObjectId(parent_id)}, {'$set': {'subtask': [id]}})
                parent = item
                while parent != self.root:
                    self.set_state(parent)
                    parent = parent.parent()
            self.item = None

    def edit_node(self):
        node = self.treeWidget.currentItem()
        old = get_id(node)
        item = self.treeWidget.currentItem().parent()
        item = get_id(item)
        parent = todolist.find_one({'_id': ObjectId(item)},
                                   {'_id': 0, 'begin': 1, 'end': 1, 'cycle.type': 1, 'cycle.cyclicality': 1})
        ui1 = todo.Ui_todo(self.app, old, True, parent)
        ui1.show()
        self.windows.append(ui1)
        ui1.child_signal.connect(self.set_item)
        ui1.exec_()
        if self.item is not None:
            self.treeWidget.blockSignals(True)
            node.setText(0, self.item['title'])
            self.treeWidget.blockSignals(False)
            if 'is_finish' not in self.item:
                self.item['is_finish'] = -1
            self.item['parent_task'] = ObjectId(item)
            self.item = self.new_day(self.item)
            del self.item['parent_task']
            if 'begin' in self.item:
                node.setText(1, self.item['begin'].strftime('%Y-%m-%d %H:%M'))
                now = datetime.today()
                if (self.item['cycle']['type'] != 1 and self.item['begin'] > now
                        or self.item['cycle']['type'] == 1 and self.item['cycle']['total_times'] == 0):
                    self.treeWidget.blockSignals(True)
                    node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
                    self.treeWidget.blockSignals(False)
                    node.setForeground(1, QtGui.QBrush(QtGui.QColor('gray')))
                    node.setForeground(2, QtGui.QBrush(QtGui.QColor('gray')))
                    node.setForeground(3, QtGui.QBrush(QtGui.QColor('gray')))
                else:
                    self.treeWidget.blockSignals(True)
                    node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
                    self.treeWidget.blockSignals(False)
                    node.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
                    node.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
                    node.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))
            else:
                node.setText(1, '')
            if 'end' in self.item:
                node.setText(2, self.item['end'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(2, '')
            self.set_priority(node, self.item['priority'])
            if self.item['is_finish'] == 0:
                self.set_gray(node, False)
            elif self.item['is_finish'] == 1:
                self.finish_node(get_id(node), True)
            id = get_id(self.treeWidget.currentItem())
            # mysql.edit_point(id, self.item['title'], self.item['content'], self.item['time'], self.item['priority'], self.item['count'])
            if 'begin' not in self.item:
                todolist.update_one({'_id': ObjectId(id)}, {'$unset': {'begin': ""}})
            if 'end' not in self.item:
                todolist.update_one({'_id': ObjectId(id)}, {'$unset': {'end': ""}})
            todolist.update_one({'_id': ObjectId(id)}, {'$unset': {'cycle': ""}})
            todolist.update_one({'_id': ObjectId(id)}, {'$set': self.item})
            self.item = None

    def delete_node(self):
        node = self.treeWidget.currentItem()
        id = get_id(node)
        parent = get_id(node.parent())
        # mysql.delete_point(id)
        todolist.delete_many({'parent_task': ObjectId(id)})
        todolist.delete_one({'_id': ObjectId(id)})
        if parent:
            parent_id = ObjectId(parent)
            todolist.update_one({'_id': parent_id}, {'$pull': {'subtask': ObjectId(id)}})
            subtask = todolist.find_one({'_id': parent_id}, {'_id': 0, 'subtask': 1})
            if len(subtask['subtask']) == 0:
                todolist.update_one({'_id': parent_id}, {'$unset': {'subtask': ""}})
        item = self.treeWidget.currentItem()
        parent = item.parent()
        parent.removeChild(item)
        while parent != self.root:
            self.set_state(parent)
            parent = parent.parent()

    def finish_node(self, id, flag):
        node = get_node(id)
        self.set_gray(node, True)
        if flag:
            # mysql.finish(id)
            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 1}})
            # son = mysql.get_son(id)
            result = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'subtask': 1})
            if 'subtask' in result and len(result['subtask']) > 0:
                son = result['subtask']
                for j in son:
                    self.finish_node(str(j), True)
        parent = node.parent()
        if parent != self.root and parent.checkState(0) != Qt.Checked:
            self.set_state(parent)
        self.treeWidget.sortItems(3, Qt.DescendingOrder)

    def set_gray(self, node, flag):
        self.treeWidget.blockSignals(True)
        node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
        if flag:
            node.setCheckState(0, Qt.Checked)
        else:
            node.setCheckState(0, Qt.PartiallyChecked)
        self.treeWidget.blockSignals(False)
        node.setForeground(1, QtGui.QBrush(QtGui.QColor('gray')))
        node.setForeground(2, QtGui.QBrush(QtGui.QColor('gray')))
        node.setForeground(3, QtGui.QBrush(QtGui.QColor('gray')))
        node.setText(3, '已完成')

    def check(self, node, column):
        if column == 0:
            self.treeWidget.setCurrentItem(node)
            id = get_id(node)
            if node.checkState(column) == Qt.Checked:
                self.finish_node(id, True)
            elif node.checkState(column) == Qt.Unchecked:
                self.treeWidget.blockSignals(True)
                node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
                self.treeWidget.blockSignals(False)
                node.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))
                self.set_state(node)
                # priority = mysql.get_priority(id)
                result = todolist.find_one({'_id': ObjectId(id)})
                self.set_priority(node, result['priority'])
                # mysql.set_priority(id, 0)
                if 0 <= result['cycle']['type'] < 2:
                    if result['cycle']['finish_times'] > 0:
                        self.treeWidget.blockSignals(True)
                        node.setCheckState(0, Qt.PartiallyChecked)
                        self.treeWidget.blockSignals(False)
                        if result['cycle']['total_times'] != 0 and result['cycle']['finish_times'] == result['cycle'][
                            'total_times']:
                            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 0}})
                            self.set_gray(node, False)
                else:
                    todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': -1}})
            parent = node.parent()
            while parent != self.root:
                self.set_state(parent)
                parent = parent.parent()

    @staticmethod
    def set_priority(node, value):
        if value == 1:
            text = "没空不做"
        elif value == 2:
            text = "有空再做"
        elif value == 3:
            text = "早做早超生"
        elif value == 4:
            text = "不可忘记"
        elif value == 5:
            text = "急急急"
        elif value == 0:
            text = "已完成"
        node.setText(3, text)

    def show_assi(self):
        old = get_id(self.treeWidget.currentItem())
        ui1 = todo.Ui_todo(self.app, old, False, None)
        ui1.show()
        self.windows.append(ui1)
        ui1.exec_()

    def set_state(self, parent):
        count = parent.childCount()
        son = [parent.child(i) for i in range(count)]
        son_num = False
        for j in son:
            state = j.checkState(0)
            if state in {Qt.Checked, Qt.PartiallyChecked}:
                son_num = True
                break
        self.treeWidget.blockSignals(True)
        if son_num:
            parent.setCheckState(0, Qt.PartiallyChecked)
        else:
            parent.setCheckState(0, Qt.Unchecked)
        self.treeWidget.blockSignals(False)

    def finish_once(self):
        node = self.treeWidget.currentItem()
        id = get_id(node)
        cycle = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'cycle': 1})['cycle']
        if cycle['type'] < 2:
            if cycle['finish_times'] + 1 > cycle['total_times']:
                msg_box = QMessageBox(QMessageBox.Critical, 'error', '完成次数不能超过总次数')
                msg_box.exec_()
                return
            elif cycle['finish_times'] + 1 == cycle['total_times']:
                if cycle['type'] == 0:
                    self.finish_node(id, True)
                elif 'end_times' in cycle and cycle['total_times'] == cycle['end_times'] != 0:
                    todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 1}})
                    self.finish_node(id, True)
                else:
                    todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 0}})
                    self.set_gray(node, False)
            else:
                node.setCheckState(0, Qt.PartiallyChecked)
        else:
            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 0}})
            self.set_gray(node, False)
        todolist.update_one({'_id': ObjectId(id)}, {'$inc': {'cycle.finish_times': 1}})

    def new_day(self, result):
        if result['is_finish'] == 1 or result['cycle']['type'] < 1:
            return result
        now = datetime.today()
        parent = None
        if "_id" in result:
            parent_id = todolist.find_one({'_id': ObjectId(result['_id'])}, {'parent_task': 1})
            if 'parent_task' in parent_id:
                parent = todolist.find_one({'_id': ObjectId(parent_id['parent_task'])}, {'end': 1})
        elif 'parent_task' in result:
            parent = todolist.find_one({'_id': ObjectId(result['parent_task'])}, {'end': 1})
        if ((parent is None or 'end' not in parent or now < parent['end'])
                and ('end_times' not in result['cycle'] or result['cycle']['end_times'] == 0
                     or result['cycle']['type'] == 1 and result['cycle']['total_times'] < result['cycle']['end_times']
                     or result['cycle']['type'] == 2 and result['cycle']['finish_times'] < result['cycle']['end_times']
                )):
            if result['cycle']['type'] == 1:
                if result['begin'] < now:
                    last = result['begin']
                    if result['cycle']['cyclicality'] == 3:
                        result['begin'] = last + relativedelta(years=1)
                    elif result['cycle']['cyclicality'] == 2:
                        result['begin'] = last + relativedelta(months=1)
                    elif result['cycle']['cyclicality'] == 0:
                        result['begin'] = last + timedelta(days=1)
                    elif result['cycle']['cyclicality'] == 1:
                        result['begin'] = last + timedelta(days=7)
                    result['cycle']['total_times'] += 1
                    result['is_finish'] = -1
                    if "_id" in result:
                        todolist.update_one({'_id': ObjectId(result['_id'])}, {'$set': result})
            elif result['cycle']['type'] == 2:
                if result['end'] < now:
                    result['begin'] = result['end'] + relativedelta(seconds=1)
                    if result['cycle']['cyclicality'] == 3:
                        result['end'] = result['end'] + relativedelta(years=1)
                    elif result['cycle']['cyclicality'] == 2:
                        result['end'] = result['end'] + relativedelta(months=1)
                    elif result['cycle']['cyclicality'] == 0:
                        result['end'] = result['end'] + timedelta(days=1)
                    elif result['cycle']['cyclicality'] == 1:
                        result['end'] = result['end'] + timedelta(days=7)
                    if result['is_finish'] == -1:
                        result['cycle']['finish_times'] = 0
                    else:
                        result['cycle']['finish_times'] += 1
                    result['is_finish'] = -1
                    if "_id" in result:
                        todolist.update_one({'_id': ObjectId(result['_id'])}, {'$set': result})
        return result

    def un_finish_once(self):
        node = self.treeWidget.currentItem()
        id = get_id(node)
        result = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'priority': 1, 'cycle': 1})
        if result['cycle']['finish_times'] <= 1:
            result['cycle']['finish_times'] = 0
            self.treeWidget.blockSignals(True)
            node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
            node.setCheckState(0, Qt.Unchecked)
            self.treeWidget.blockSignals(False)
        elif result['cycle']['finish_times'] == result['cycle']['total_times']:
            result['cycle']['finish_times'] -= 1
            self.set_priority(node, result['priority'])
            self.treeWidget.blockSignals(True)
            node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
            node.setCheckState(0, Qt.PartiallyChecked)
            self.treeWidget.blockSignals(False)
        else:
            result['cycle']['finish_times'] -= 1
        result['is_finish'] = -1
        node.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
        node.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
        node.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))
        todolist.update_one({'_id': ObjectId(id)}, {'$set': result})

    def set_auto(self, flag):
        node = self.treeWidget.currentItem()
        id = get_id(node)
        if flag:
            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'expend': 0}})
        else:
            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'expend': 1}})


class MyWidget(QMainWindow):
    def closeEvent(self, event):
        for (node, id) in item_id:
            if node.isExpanded():
                todolist.update_one({'_id': ObjectId(id), 'expend': {'$ne': 0}}, {'$set': {'expend': 1}})
            else:
                todolist.update_one({'_id': ObjectId(id), 'expend': {'$ne': 0}}, {'$set': {'expend': -1}})
        event.accept()
