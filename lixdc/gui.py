from __future__ import absolute_import

import sys
import time
from PyQt4 import QtGui, QtCore

from .state.general import State
from .widgets.main import MainWindow
from .widgets.login import Login


def run():
    app_state = State()
    app = QtGui.QApplication(sys.argv)
    #print("Styles: ", QtGui.QStyleFactory.keys())
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    ### TURNS ON LOGIN SCREEN
    login = Login(app_state=app_state)
    if login.exec_() == QtGui.QDialog.Accepted:
        #if True:
        print("After Login App State: ", app_state)
        main = MainWindow(app_state=app_state)
        sys.exit(app.exec_())

def run_ipython(username, project):
    if username == '' or project == '':
        raise Exception('Illegal username or project. Please check.')
    app_state = State()
    app_state.user = username
    app_state.project = project
    app_state.login_timestamp = time.time()
    params = {'app_state': app_state}
    main = create_window(MainWindow, **params)

def create_window(window_class, **kwargs):
    app_created = False
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
        app_created = True
    app.references = set()
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    window = window_class(**kwargs)
    app.references.add(window)
    window.show()
    if app_created:
        app.exec_()
    return window

if __name__ == "__main__":
    run()
