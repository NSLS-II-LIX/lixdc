from datetime import datetime
from PyQt4 import QtGui


class BaseWidget:
    def __init__(self, app_state=None):
        self.app_state = app_state
        self.init_ui()

    def init_ui(self):
        pass

    def center(self, w=None, h=None, w_factor=0.2, h_factor=0.2):
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(screen).center()
        available_rect = QtGui.QApplication.desktop().availableGeometry(screen)

        x = 0
        y = available_rect.y()

        if w is None:
            w = available_rect.width()
            w = int((w - x) * w_factor)

        if h is None:
            h = available_rect.height()
            h = int((h - y) * h_factor)

        self.setGeometry(0, 0, w, h)

        frame_geom = self.frameGeometry()
        frame_geom.moveCenter(center_point)

        self.move(frame_geom.topLeft())
