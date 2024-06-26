# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'todo.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from datetime import timedelta, datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QDate, QTime
from PyQt5.QtWidgets import QDialog, QMessageBox
from bson import ObjectId
from dateutil.relativedelta import relativedelta

import mongodb

from enum import Enum
class GROUP(Enum):
    END = 1
    CYCLE = 2
    FINISH = 3
    TOTAL = 4
    BEGIN = 5
    END_TIMES = 6

class Ui_todo(QDialog):
    child_signal = pyqtSignal(dict)

    def __init__(self, app, old, is_edit, parent):
        super(Ui_todo, self).__init__()
        self.app = app
        self.old = old
        self.is_edit = is_edit
        self.parent = parent  # begin, end, type
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 510)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 4, 1, 4)
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 7, 0, 1, 3)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 3, 0, 1, 8)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 6, 3, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 9, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 9, 4, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 7, 4, 1, 3)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 5, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 9, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 4, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 9, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 4, 1, 3)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 3)
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 6, 7, 1, 1)
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 7, 3, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 9, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 9, 5, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout.addWidget(self.comboBox_3, 5, 4, 1, 4)
        self.timeEdit_2 = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.gridLayout.addWidget(self.timeEdit_2, 7, 7, 1, 1)
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 8, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 8)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 6, 1, 2)
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 9, 6, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 9, 7, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.label_5.setBuddy(self.comboBox_3)
        self.label_7.setBuddy(self.comboBox)
        self.label.setBuddy(self.lineEdit)
        self.label_6.setBuddy(self.spinBox)
        self.label_9.setBuddy(self.comboBox_2)
        self.label_2.setBuddy(self.textEdit)
        self.label_4.setBuddy(self.dateEdit_2)
        self.label_3.setBuddy(self.dateEdit)
        self.label_10.setBuddy(self.spinBox_3)
        self.label_8.setBuddy(self.spinBox_2)

        if not self.is_edit:
            self.buttonBox.hide()
            self.checkBox_2.hide()
            self.checkBox.hide()
        self.timeEdit.setVisible(False)
        self.timeEdit_2.setVisible(False)

        self.retranslateUi(Dialog)
        self.cycle()
        if self.is_edit:
            self.buttonBox.accepted.connect(self.send)
            self.buttonBox.rejected.connect(self.cancel)
        self.checkBox.toggled['bool'].connect(self.timeEdit.setVisible)  # type: ignore
        self.checkBox_2.toggled['bool'].connect(self.timeEdit_2.setVisible)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox.activated['int'].connect(self.cycle)

        if self.old is not None:
            todolist = mongodb.MongoDBPool.get_mongodb_pool()
            old = todolist.find_one({'_id': ObjectId(self.old)})
            if 'subtask' in old and len(old['subtask']) > 0:
                self.comboBox.setDisabled(True)
            self.lineEdit.setText(old['title'])
            self.textEdit.setText(old['content'])
            self.comboBox_3.setCurrentIndex(old['priority'] - 1)
            self.comboBox.setCurrentIndex(old['cycle']['type'] + 1)
            self.cycle()
            if old['cycle']['type'] >= 0:
                self.spinBox.setValue(int(old['cycle']['finish_times']))
            if old['cycle']['type'] > 0:
                self.comboBox_2.setCurrentIndex(old['cycle']['cyclicality'])
                if 'end_times' in old['cycle']:
                    self.spinBox_3.setValue(int(old['cycle']['end_times']))
                elif not self.is_edit:
                    self.show_or_hide(False, GROUP.END_TIMES)
            if 1 >= old['cycle']['type'] >= 0:
                self.spinBox_2.setValue(int(old['cycle']['total_times']))
            if 'begin' in old:
                self.dateEdit.setDate(QDate.fromString(old['begin'].strftime('%Y-%m-%d'), 'yyyy-MM-dd'))
                self.timeEdit.setTime(QTime.fromString(old['begin'].strftime('%H:%M'), 'hh:mm'))
                self.checkBox.setCheckState(Qt.Checked)
            else:
                if not self.is_edit:
                    self.show_or_hide(False, GROUP.BEGIN)
                else:
                    self.show_or_hide(True, GROUP.BEGIN)
            if 'end' in old:
                self.dateEdit_2.setDate(QDate.fromString(old['end'].strftime('%Y-%m-%d'), 'yyyy-MM-dd'))
                self.timeEdit_2.setTime(QTime.fromString(old['end'].strftime('%H:%M'), 'hh:mm'))
                self.checkBox_2.setCheckState(Qt.Checked)
            else:
                if self.is_edit and old['cycle']['type'] != 1:
                    self.show_or_hide(True, GROUP.END)
                else:
                    self.show_or_hide(False, GROUP.END)
            if old['cycle']['type'] == 2:
                self.timeEdit_2.setDisabled(True)
                self.dateEdit_2.setDisabled(True)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "优先级："))
        self.label_7.setText(_translate("Dialog", "类型："))
        self.label.setText(_translate("Dialog", "概要："))
        self.checkBox.setText(_translate("Dialog", "具体时间"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "天"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "周"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "月"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "年"))
        self.comboBox.setItemText(0, _translate("Dialog", "一次性"))
        self.comboBox.setItemText(1, _translate("Dialog", "重复"))
        self.comboBox.setItemText(2, _translate("Dialog", "定期"))
        self.comboBox.setItemText(3, _translate("Dialog", "阶段"))
        self.label_6.setText(_translate("Dialog", "完成次数："))
        self.label_9.setText(_translate("Dialog", "周期："))
        self.label_2.setText(_translate("Dialog", "内容："))
        self.label_4.setText(_translate("Dialog", "结束时间："))
        self.label_3.setText(_translate("Dialog", "开始时间："))
        self.checkBox_2.setText(_translate("Dialog", "具体时间"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "没空不做"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "有空再做"))
        self.comboBox_3.setItemText(2, _translate("Dialog", "早做早超生"))
        self.comboBox_3.setItemText(3, _translate("Dialog", "不可忘记"))
        self.comboBox_3.setItemText(4, _translate("Dialog", "急急急"))
        self.label_10.setText(_translate("Dialog", "总次数："))
        self.label_8.setText(_translate("Dialog", "当前总次数："))

    def send(self):
        dic = dict()
        dic['title'] = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        dic['content'] = text
        dic['priority'] = self.comboBox_3.currentIndex() + 1
        type = self.comboBox.currentIndex() - 1
        dic['cycle'] = {"type": type}
        begin_date = self.dateEdit.dateTime().toString('yyyy-MM-dd')
        if self.checkBox.checkState() == Qt.Checked:
            begin_time = self.timeEdit.dateTime().toString('hh:mm')
        else:
            begin_time = '00:00'
        if type > 0 and self.spinBox_3.value() > 0:
            dic['cycle']['end_times'] = self.spinBox_3.value()
        if type <= 0:
            begin_time = begin_date + ' ' + begin_time
            begin_time = datetime.strptime(begin_time, '%Y-%m-%d %H:%M')
            if begin_date != '2000-01-01':
                if self.parent is None or 'begin' not in self.parent or begin_time >= self.parent['begin']:
                    dic['begin'] = begin_time
                else:
                    msg_box = QMessageBox(QMessageBox.Critical, 'error', '开始时间需比父任务晚或相同')
                    msg_box.exec_()
                    return
            end_date = self.dateEdit_2.dateTime().toString('yyyy-MM-dd')
            if self.checkBox_2.checkState() == Qt.Checked:
                end_time = self.timeEdit_2.dateTime().toString('hh:mm')
            else:
                end_time = '00:00'
            end_time = end_date + ' ' + end_time
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            if end_date != '2000-01-01':
                if self.parent is None or 'end' not in self.parent or end_time <= self.parent['end']:
                    if end_time > begin_time:
                        dic['end'] = end_time
                    else:
                        msg_box = QMessageBox(QMessageBox.Critical, 'error', '结束时间需比开始时间早')
                        msg_box.exec_()
                        return
                else:
                    msg_box = QMessageBox(QMessageBox.Critical, 'error', '结束时间需比父任务早或相同')
                    msg_box.exec_()
                    return
        else:
            slot = self.comboBox_2.currentIndex()
            dic['cycle']['cyclicality'] = slot
            flag = False
            if begin_date == '2000-01-01':
                if self.parent and 'begin' in self.parent:
                    begin_date = self.parent['begin']
                else:
                    begin_date = datetime.today()
                if begin_date.strftime("%H:%M") > begin_time:
                    begin_date += timedelta(days=1)
                flag = True
            else:
                begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
            if (self.parent is None or 'begin' not in self.parent or
                    begin_date.strftime('%Y-%m-%d') + ' ' + begin_time >= self.parent['begin'].strftime('%Y-%m-%d %H:%M')):
                if type == 2:
                    if slot == 3:
                        begin_date = datetime(begin_date.year, 1, 1)
                    elif slot == 2:
                        begin_date = datetime(begin_date.year, begin_date.month, 1)
                    elif slot == 1:
                        begin_date = begin_date - timedelta(days=begin_date.weekday())
                dic['begin'] = begin_date.strftime('%Y-%m-%d') + ' ' + begin_time
                dic['begin'] = datetime.strptime(dic['begin'], '%Y-%m-%d %H:%M')
            else:
                msg_box = QMessageBox(QMessageBox.Critical, 'error', '开始时间需比父任务晚或相同')
                msg_box.exec_()
                return
            if slot == 3:
                end_date = begin_date + relativedelta(years=1)
            elif slot == 2:
                end_date = begin_date + relativedelta(months=1)
            elif slot == 0:
                end_date = begin_date + timedelta(days=1)
            elif slot == 1:
                end_date = begin_date + timedelta(days=7)
            dic['end'] = end_date.strftime('%Y-%m-%d') + ' ' + begin_time
            dic['end'] = datetime.strptime(dic['end'], '%Y-%m-%d %H:%M')
            if type == 1:
                if flag:
                    dic['begin'] = dic['end']
                dic.pop('end')
        if type >= 0:
            dic['cycle']['finish_times'] = self.spinBox.value()
        if 1 >= type >= 0:
            dic['cycle']['total_times'] = self.spinBox_2.value()
            if dic['cycle']['finish_times'] > dic['cycle']['total_times']:
                msg_box = QMessageBox(QMessageBox.Critical, 'error', '完成次数不能超过总次数')
                msg_box.exec_()
                return
            elif dic['cycle']['total_times'] != 0 and dic['cycle']['finish_times'] == dic['cycle']['total_times']:
                if type == 1:
                    dic['is_finish'] = 0
                elif type == 0:
                    dic['is_finish'] = 1
        self.child_signal.emit(dic)
        self.close()

    def cancel(self):
        self.child_signal.emit(dict())
        self.close()

    def cycle(self):
        type = self.comboBox.currentIndex() - 1
        if type == 0 or type == 1:
            self.show_or_hide(True, GROUP.TOTAL)
        else:
            self.show_or_hide(False, GROUP.TOTAL)
        if type >= 0:
            self.show_or_hide(True, GROUP.FINISH)
        else:
            self.show_or_hide(False, GROUP.FINISH)
        if type <= 0 or (type == 2 and self.is_edit):
            self.show_or_hide(True, GROUP.END)
            if type == 2:
                self.timeEdit_2.setDisabled(True)
                self.dateEdit_2.setDisabled(True)
            else:
                self.timeEdit_2.setDisabled(False)
                self.dateEdit_2.setDisabled(False)
        else:
            self.show_or_hide(False, GROUP.END)
        if type > 0:
            self.show_or_hide(True, GROUP.CYCLE)
            self.show_or_hide(True, GROUP.END_TIMES)
        else:
            self.show_or_hide(False, GROUP.CYCLE)
            self.show_or_hide(False, GROUP.END_TIMES)
        if type == 1:
            self.label_3.setText("更新时间：")
        else:
            self.label_3.setText("开始时间：")
        if type == 0:
            self.label_8.setText("总次数")
        else:
            self.label_8.setText("当前总次数")

    def show_or_hide(self, is_show, g):
        if is_show:
            if g == GROUP.CYCLE:
                self.label_9.show()
                self.comboBox_2.show()
            elif g == GROUP.END:
                self.label_4.show()
                self.dateEdit_2.show()
                self.checkBox_2.show()
                # self.timeEdit_2.show()
            elif g == GROUP.FINISH:
                self.label_6.show()
                self.spinBox.show()
            elif g == GROUP.TOTAL:
                self.label_8.show()
                self.spinBox_2.show()
            elif g == GROUP.BEGIN:
                self.label_3.show()
                self.dateEdit.show()
                self.checkBox.show()
                # self.timeEdit.show()
            elif g == GROUP.END_TIMES:
                self.label_10.show()
                self.spinBox_3.show()
        else:
            if g == GROUP.CYCLE:
                self.label_9.hide()
                self.comboBox_2.hide()
            elif g == GROUP.END:
                self.label_4.hide()
                self.dateEdit_2.hide()
                self.checkBox_2.hide()
                self.timeEdit_2.hide()
            elif g == GROUP.FINISH:
                self.label_6.hide()
                self.spinBox.hide()
            elif g == GROUP.TOTAL:
                self.label_8.hide()
                self.spinBox_2.hide()
            elif g == GROUP.BEGIN:
                self.label_3.hide()
                self.dateEdit.hide()
                self.checkBox.hide()
                self.timeEdit.hide()
            elif g == GROUP.END_TIMES:
                self.label_10.hide()
                self.spinBox_3.hide()
