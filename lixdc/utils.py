from PyQt4 import QtGui, QtCore

ANSWER_OK = QtGui.QMessageBox.Ok
ANSWER_CANCEL = QtGui.QMessageBox.Cancel


def show_error(text, detail, title):
    msg_box = QtGui.QMessageBox()
    msg_box.setIcon(QtGui.QMessageBox.Critical)
    msg_box.setText(text)
    msg_box.setDetailedText(detail)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QtGui.QMessageBox.Ok)
    msg_box.exec_()

def show_question(text, informative, title):
    msg_box = QtGui.QMessageBox()
    msg_box.setIcon(QtGui.QMessageBox.Question)
    msg_box.setText(text)
    msg_box.setInformativeText(informative)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    ret = msg_box.exec_()
    return ret

def show_information(text, informative, title):
    msg_box = QtGui.QMessageBox()
    msg_box.setIcon(QtGui.QMessageBox.Information)
    msg_box.setText(text)
    msg_box.setInformativeText(informative)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QtGui.QMessageBox.Ok)
    ret = msg_box.exec_()

