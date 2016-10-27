from __future__ import absolute_import

import sys
import time
from PyQt4 import QtGui, QtCore

from .state.general import State
from .widgets.main import MainWindow
from .widgets.login import Login
from .conf import load_configuration

config_params = {k: v for k, v in load_configuration('lixdc', 'LIXDC',
                                                     [
                                                      'amostra_host',
                                                      'amostra_port',
                                                      'base_path'
                                                      ]
                                                     ).items() if v is not None}

def run():
    app_state = State()
    app_state.configs = config_params
    app = QtGui.QApplication(sys.argv)
    #print("Styles: ", QtGui.QStyleFactory.keys())
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    ### TURNS ON LOGIN SCREEN
    login = Login(app_state=app_state)
    if login.exec_() == QtGui.QDialog.Accepted:
        main = MainWindow(app_state=app_state)
        sys.exit(app.exec_())

def run_ipython(username, proposal, run):
    if username == '' or proposal == '' or run == '':
        raise Exception('Illegal username, proposal or run. Please check.')
    app_state = State()
    app_state.configs = config_params
    app_state.user = username
    app_state.proposal_id = proposal
    app_state.run_id = run
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
