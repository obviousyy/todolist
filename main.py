import sys
from PyQt5 import QtWidgets
import list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = list.MyWidget()
    ui = list.Ui_MainWindow(app)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
