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

        self.labelProposal = QtGui.QLabel(self)
        self.labelProposal.setText("Proposal ID: ")
        self.textProposal = QtGui.QLineEdit(self)
        self.textProposal.setText("")

        self.labelRun = QtGui.QLabel(self)
        self.labelRun.setText("Run #: ")
        self.textRun = QtGui.QLineEdit(self)
        self.textRun.setText("{}".format(
                            time.strftime("%Y%m%d")))

        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)

        vbox_layout = QtGui.QVBoxLayout(self)
        form_layout = QtGui.QFormLayout()
        form_layout.addRow(self.labelName, self.textName)
        form_layout.addRow(self.labelPass, self.textPass)
        form_layout.addRow(self.labelProposal, self.textProposal)
        form_layout.addRow(self.labelRun, self.textRun)
        vbox_layout.addLayout(form_layout)
        vbox_layout.addWidget(self.buttonLogin)

    def handle_login(self):
        # TODO: Implement real authentication
        if self.textProposal.text() == '' or self.textRun.text() == '':
            QtGui.QMessageBox.warning(self, 'Error', 'Proposal and Run Number are required.')
            return

        if self.textName.text() != '' and self.textPass.text() == 'lix':
            self.app_state.user = self.textName.text()
            self.app_state.login_timestamp = time.time()
            self.app_state.proposal_id = self.textProposal.text()
            self.app_state.run_id = self.textRun.text()
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')
