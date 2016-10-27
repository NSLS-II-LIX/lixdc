import time
from PyQt4 import QtGui


class Login(QtGui.QDialog):
    def __init__(self, parent=None, app_state=None):
        super(Login, self).__init__(parent)
        self.app_state = app_state
        self.init_ui()
        self.setFixedSize(300,200)

    def init_ui(self):
        self.labelName = QtGui.QLabel(self)
        self.labelName.setText("Username: ")
        self.textName = QtGui.QLineEdit(self)
        self.textName.setText("")

        self.labelPass = QtGui.QLabel(self)
        self.labelPass.setText("Password: ")
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.textPass.setText("lix")

        self.labelProject = QtGui.QLabel(self)
        self.labelProject.setText("Project: ")
        self.textProject = QtGui.QLineEdit(self)
        self.textProject.setText("")

        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)

        vbox_layout = QtGui.QVBoxLayout(self)
        form_layout = QtGui.QFormLayout()
        form_layout.addRow(self.labelName, self.textName)
        form_layout.addRow(self.labelPass, self.textPass)
        form_layout.addRow(self.labelProject, self.textProject)
        vbox_layout.addLayout(form_layout)
        vbox_layout.addWidget(self.buttonLogin)

    def handle_login(self):
        # TODO: Implement real authentication
        if self.textProject.text() == '':
            QtGui.QMessageBox.warning(self, 'Error', 'Project is required.')
            return

        if self.textName.text() != '' and self.textPass.text() == 'lix':
            self.app_state.user = self.textName.text()
            self.app_state.project = self.textProject.text()
            self.app_state.login_timestamp = time.time()
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')
