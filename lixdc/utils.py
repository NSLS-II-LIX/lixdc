import os
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

# xf16id - 5008, lix - 3009
def makedirs(path, mode=0o777, owner_uid=5008, group=3009):
    '''Recursively make directories and set permissions'''
    # Permissions not working with os.makedirs -
    # See: http://stackoverflow.com/questions/5231901
    if not path or os.path.exists(path):
        return []

    head, tail = os.path.split(path)
    ret = makedirs(head, mode)
    try:
        os.mkdir(path)
    except OSError as ex:
        if 'File exists' not in str(ex):
            raise
    os.chmod(path, mode)
    ret.append(path)
    return ret
