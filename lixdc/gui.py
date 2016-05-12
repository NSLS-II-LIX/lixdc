import sys
from PyQt4 import QtGui

from lixdc.widgets.main import MainWindow


def run():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
