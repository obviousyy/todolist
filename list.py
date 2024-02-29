# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QMessageBox, QTreeWidgetItem, QHeaderView
from bson import ObjectId
from dateutil.relativedelta import relativedelta

import mongodb
import todo

todolist = mongodb.MongoDBPool.get_mongodb_pool()


class CustomTreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        value1 = self.text(column)
        value2 = other.text(column)
        if column == 3:
            if value1 == value2:
                return self.text(1) > other.text(1)
            else:
                order = {'没空不做': 1, '有空再做': 2, '早做早超生': 3, '一定要记得……': 4, '急急急': 5, '已完成': 0}
                return order[value1] < order[value2]
        elif column == 1:
            if value1 == value2:
                order = {'没空不做': 1, '有空再做': 2, '早做早超生': 3, '一定要记得……': 4, '急急急': 5, '已完成': 0}
                value1 = self.text(2)
                value2 = other.text(2)
                return order[value1] > order[value2]
            else:
                return self.text(1) < other.text(1)
        else:
            return self.text(column) < other.text(column)


class Ui_MainWindow(object):
    def __init__(self, app):
        super(Ui_MainWindow, self).__init__()
        self.item_id = list()
        self.app = app
        self.windows = list()
        self.root = None
        self.item = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setText(0, 'self')
        self.root = item_0
        self.treeWidget.setHeaderLabels(['概要', '开始时间', '结束时间', '优先级'])
        MainWindow.setCentralWidget(self.centralwidget)
        header = self.treeWidget.header()  # 获取表头
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.treeWidget.itemDoubleClicked.connect(self.show_assi)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_menu)
        self.treeWidget.expandItem(item_0)  # 展开添加的节点
        # self.treeWidget.setSortingEnabled(True)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.treeWidget.itemChanged.connect(self.check)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "任务列表"))
        self.show()

    def show(self):
        # db = mysql.MysqlUtil()
        # sql = "SELECT * FROM todo WHERE parent_id is null"
        # roots = db.fetchall(sql)
        roots = todolist.find({'parent_task': None})
        for i in roots:
            self.create_node(i, self.root)
        self.treeWidget.sortItems(2, Qt.DescendingOrder)

    def create_node(self, i, root):
        node = CustomTreeWidgetItem(root)
        self.item_id.append((node, str(i['_id'])))
        node.setText(0, i['title'])
        if i['cycle']['type'] > 0:
            i = self.new_day(i)
        if 'begin' in i:
            node.setText(1, i['begin'].strftime('%Y-%m-%d %H:%M'))
        else:
            node.setText(1, '')
        if 'end' in i:
            node.setText(2, i['end'].strftime('%Y-%m-%d %H:%M'))
        else:
            node.setText(2, '')
        self.set_priority(node, i['priority'])
        if 'subtask' in i:
            # son = mysql.get_son(i['id'])
            son = i['subtask']
            son_num = 0
            son_flag = False
            for j in son:
                j = todolist.find_one({'_id': j})
                state = self.create_node(j, node)
                if state == Qt.Checked:
                    son_num += 1
                    son_flag = True
                if state == Qt.PartiallyChecked:
                    son_flag = True
            if son_flag:
                node.setCheckState(0, Qt.PartiallyChecked)
            else:
                node.setCheckState(0, Qt.Unchecked)
            if i['is_finish'] == 1:
                self.finish_node(str(i['_id']))
            if son_num != len(son):
                self.treeWidget.expandItem(node)
        else:
            if i['is_finish'] == 1:
                self.finish_node(str(i['_id']))
            elif i['is_finish'] == 0:
                node.setCheckState(0, Qt.PartiallyChecked)
            elif i['is_finish'] == -1:
                node.setCheckState(0, Qt.Unchecked)
        return node.checkState(0)

    def show_menu(self):
        item = self.treeWidget.currentItem()
        menu = QMenu()
        id = self.get_id(item)
        result = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'cycle.type': 1, 'is_finish': 1})
        if item.text(3) != '已完成' and (result is None or result['cycle']['type'] < 0):
            action = menu.addAction('添加子任务')
            action.triggered.connect(self.add_node)
        if item != self.root and item.text(3) != '已完成':
            action = menu.addAction('修改任务')
            action.triggered.connect(self.edit_node)
            if result['cycle']['type'] >= 0 > result['is_finish']:
                action = menu.addAction('完成一次')
                action.triggered.connect(self.finish_once)
        if item != self.root:
            action = menu.addAction('删除任务')
            action.triggered.connect(self.delete_node)
        menu.exec_(QCursor.pos())

    def set_item(self, dic):
        if dic != {}:
            self.item = dic
        else:
            self.item = None

    def add_node(self):
        if self.treeWidget.currentItem().text(3) == '已完成':
            msg_box = QMessageBox(QMessageBox.Warning, 'warning', '已完成的任务不能添加子任务')
            msg_box.exec_()
            return
        item = self.treeWidget.currentItem()
        parent_id = self.get_id(item)
        parent = todolist.find_one({'_id': ObjectId(parent_id)},
                                   {'_id': 0, 'begin': 1, 'end': 1, 'cycle.type': 1, 'cycle.cyclicality': 1})
        ui1 = todo.Ui_todo(self.app, None, True, parent)
        ui1.show()
        self.windows.append(ui1)
        ui1.child_signal.connect(self.set_item)
        ui1.exec_()
        if self.item is not None:
            node = CustomTreeWidgetItem(item)
            self.treeWidget.blockSignals(True)
            node.setText(0, self.item['title'])
            self.treeWidget.blockSignals(False)
            if 'begin' in self.item:
                node.setText(1, self.item['begin'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(1, '')
            if 'end' in self.item:
                node.setText(2, self.item['end'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(2, '')
            self.set_priority(node, self.item['priority'])
            if 'is_finish' not in self.item or self.item['is_finish'] != 0:
                self.item['is_finish'] = -1
            id = todolist.insert_one(self.item).inserted_id
            if item != self.root:
                parent_id = self.get_id(item)
                subtask = todolist.find_one({'_id': ObjectId(parent_id)}, {'_id': 0, 'subtask': 1})
                if 'subtask' in subtask:
                    todolist.update_one({'_id': ObjectId(parent_id)}, {'$addToSet': {'subtask': id}})
                else:
                    todolist.update_one({'_id': ObjectId(parent_id)}, {'$set': {'subtask': [id]}})
                todolist.update_one({'_id': ObjectId(id)}, {'$set': {'parent_task': ObjectId(parent_id)}})
            self.item_id.append((node, str(id)))
            if self.item['is_finish'] == 0:
                self.treeWidget.blockSignals(True)
                node.setCheckState(0, Qt.PartiallyChecked)
                self.treeWidget.blockSignals(False)
            else:
                self.treeWidget.blockSignals(True)
                node.setCheckState(0, Qt.Unchecked)
                self.treeWidget.blockSignals(False)
            self.item = None

    def edit_node(self):
        node = self.treeWidget.currentItem()
        old = self.get_id(node)
        item = self.treeWidget.currentItem().parent()
        item = self.get_id(item)
        parent = todolist.find_one({'_id': ObjectId(item)},
                                   {'_id': 0, 'begin': 1, 'end': 1, 'cycle.type': 1, 'cycle.cyclicality': 1})
        ui1 = todo.Ui_todo(self.app, old, True, parent)
        ui1.show()
        self.windows.append(ui1)
        ui1.child_signal.connect(self.set_item)
        ui1.exec_()
        if self.item is not None:
            node = self.treeWidget.currentItem()
            if node.text(3) == '已完成':
                self.treeWidget.blockSignals(True)
                node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
                self.treeWidget.blockSignals(False)
                node.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))
            self.treeWidget.blockSignals(True)
            node.setText(0, self.item['title'])
            self.treeWidget.blockSignals(False)
            if 'begin' in self.item:
                node.setText(1, self.item['begin'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(1, '')
            if 'end' in self.item:
                node.setText(2, self.item['end'].strftime('%Y-%m-%d %H:%M'))
            else:
                node.setText(2, '')
            self.set_priority(node, self.item['priority'])
            id = self.get_id(self.treeWidget.currentItem())
            # mysql.edit_point(id, self.item['title'], self.item['content'], self.item['time'], self.item['priority'], self.item['count'])
            todolist.update_one({'_id': ObjectId(id)}, {'$set': self.item})
            self.item = None

    def delete_node(self):
        node = self.treeWidget.currentItem()
        id = self.get_id(node)
        parent = self.get_id(node.parent())
        # mysql.delete_point(id)
        todolist.delete_one({'_id': ObjectId(id)})
        todolist.update_one({'_id': ObjectId(parent)}, {'$pull': {'subtask': ObjectId(id)}})
        item = self.treeWidget.currentItem()
        parent = item.parent()
        parent.removeChild(item)
        if parent != self.root and parent.checkState(0) != Qt.Checked:
            self.set_state(parent)

    def finish_node(self, id):
        node = self.get_node(id)
        # mysql.finish(id)
        todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 1}})
        self.treeWidget.blockSignals(True)
        node.setForeground(0, QtGui.QBrush(QtGui.QColor('gray')))
        self.treeWidget.blockSignals(False)
        node.setForeground(1, QtGui.QBrush(QtGui.QColor('gray')))
        node.setForeground(2, QtGui.QBrush(QtGui.QColor('gray')))
        node.setForeground(3, QtGui.QBrush(QtGui.QColor('gray')))
        node.setText(3, '已完成')
        # son = mysql.get_son(id)
        result = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'subtask': 1})
        if 'subtask' in result:
            son = result['subtask']
            for j in son:
                self.finish_node(str(j))
        self.treeWidget.blockSignals(True)
        node.setCheckState(0, Qt.Checked)
        self.treeWidget.blockSignals(False)
        parent = node.parent()
        if parent != self.root:
            self.set_state(parent)

    def check(self, node, column):
        if column == 0:
            self.treeWidget.setCurrentItem(node)
            id = self.get_id(node)
            if node.checkState(column) == Qt.Checked:
                self.finish_node(id)
            elif node.checkState(column) == Qt.Unchecked:
                self.treeWidget.blockSignals(True)
                node.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
                self.treeWidget.blockSignals(False)
                node.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
                node.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))
                self.set_state(node)
                # priority = mysql.get_priority(id)
                priority = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'priority': 1})['priority']
                self.set_priority(node, priority)
                # mysql.set_priority(id, 0)
                todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': -1}})
                parent = node.parent()
                if parent != self.root:
                    self.set_state(parent)
                    if parent.text(2) == '已完成':
                        id = self.get_id(parent)
                        # priority = mysql.get_priority(id)
                        priority = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'priority': 1})['priority']
                        self.set_priority(parent, priority)
                        # mysql.set_priority(id, 0)
                        todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': -1}})
                        self.treeWidget.blockSignals(True)
                        parent.setForeground(0, QtGui.QBrush(QtGui.QColor('black')))
                        self.treeWidget.blockSignals(False)
                        parent.setForeground(1, QtGui.QBrush(QtGui.QColor('black')))
                        parent.setForeground(2, QtGui.QBrush(QtGui.QColor('black')))
                        parent.setForeground(3, QtGui.QBrush(QtGui.QColor('black')))

    def set_priority(self, node, value):
        if value == 1:
            text = "没空不做"
        elif value == 2:
            text = "有空再做"
        elif value == 3:
            text = "早做早超生"
        elif value == 4:
            text = "一定要记得……"
        elif value == 5:
            text = "急急急"
        elif value == 0:
            text = "已完成"
        node.setText(3, text)

    def get_id(self, node):
        for i in self.item_id:
            if i[0] == node:
                return i[1]

    def get_node(self, id):
        for i in self.item_id:
            if i[1] == id:
                return i[0]

    def show_assi(self):
        old = self.get_id(self.treeWidget.currentItem())
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
        id = self.get_id(node)
        cycle = todolist.find_one({'_id': ObjectId(id)}, {'_id': 0, 'cycle': 1})['cycle']
        if cycle['type'] < 2:
            if cycle['finish_times'] + 1 > cycle['total_times']:
                msg_box = QMessageBox(QMessageBox.Critical, 'error', '完成次数不能超过总次数')
                msg_box.exec_()
                return
            elif cycle['finish_times'] + 1 == cycle['total_times']:
                if cycle['type'] == 0:
                    self.finish_node(id)
                else:
                    todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 0}})
                    self.treeWidget.blockSignals(True)
                    node.setCheckState(0, Qt.PartiallyChecked)
                    self.treeWidget.blockSignals(False)
        else:
            todolist.update_one({'_id': ObjectId(id)}, {'$set': {'is_finish': 0}})
            self.treeWidget.blockSignals(True)
            node.setCheckState(0, Qt.PartiallyChecked)
            self.treeWidget.blockSignals(False)
        todolist.update_one({'_id': ObjectId(id)}, {'$inc': {'cycle.finish_times': 1}})

    def new_day(self, result):
        now = datetime.today()
        if result['end'] < now and result['is_finish'] < 1:
            result['begin'] = result['end']
            if result['cycle']['cyclicality'] == 3:
                result['end'] = result['begin'] + relativedelta(years=1)
            elif result['cycle']['cyclicality'] == 2:
                result['end'] = result['begin'] + relativedelta(months=1)
            elif result['cycle']['cyclicality'] == 0:
                result['end'] = result['begin'] + timedelta(days=1)
            elif result['cycle']['cyclicality'] == 1:
                result['end'] = result['begin'] + timedelta(days=7)
            if result['cycle']['type'] == 2:
                if result['is_finish'] < 0:
                    result['cycle']['finish_times'] = 0
                else:
                    result['cycle']['finish_times'] += 1
            elif result['cycle']['type'] == 1:
                result['cycle']['total_times'] += 1
            result['is_finish'] = -1
        todolist.update_one({'_id': ObjectId(result['_id'])}, {'$set': result})
        return result
