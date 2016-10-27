from datetime import datetime
from PyQt4 import QtGui, QtCore
from . import icons
from .base import BaseWidget
from .sample_manager import SampleManager
from .data_collection import DataCollection


class MainWindow(QtGui.QMainWindow, BaseWidget):
    def __init__(self, app_state=None):
        super(MainWindow, self).__init__()
        self.app_state = app_state
        self.main_widget = QtGui.QWidget(self)
        self.init_ui()
        self.setFixedSize(350, 350)
        # self.initCallbacks()

    def init_ui(self):
        self.status_bar = QtGui.QStatusBar()
        self.setStatusBar(self.status_bar)

        self.lbl_user_data = QtGui.QLabel()
        user_data_str = "Logged in at: {} as {} | Project: {}"
        fmt_date = datetime.fromtimestamp(self.app_state.login_timestamp)
        fmt_date = fmt_date.strftime("%D %H:%M:%S")
        self.lbl_user_data.text = user_data_str.format(fmt_date,
                                                       self.app_state.user,
                                                       self.app_state.project)
        self.status_bar.addWidget(self.lbl_user_data,1)


        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)  # Handles OSX issues with MenuBar
        fileMenu = menu_bar.addMenu('&File')
        exitAction = QtGui.QAction(QtGui.QIcon(icons.CLOSE), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        self.create_buttons()

        self.setWindowTitle('LIX Data Collection')
        self.center()
        #self.showMaximized()
        self.show()

    def create_buttons(self):

        layout = QtGui.QGridLayout()
        self.main_widget.setLayout(layout)

        btn_size = ((40, 40), (200, 200))  # Min and Max

        btn_sample = QtGui.QPushButton()
        btn_sample.setMinimumSize(btn_size[0][0], btn_size[0][1])
        btn_sample.setMaximumSize(btn_size[1][0], btn_size[1][1])
        btn_sample.connect(btn_sample, QtCore.SIGNAL('clicked()'), self.handle_open_sample)
        btn_sample.setIcon(QtGui.QIcon(icons.SAMPLE))
        btn_sample_hint = "Sample Manager"
        btn_sample.setText(btn_sample_hint)
        btn_sample.setStatusTip(btn_sample_hint)

        btn_dc = QtGui.QPushButton()
        btn_dc.setMinimumSize(btn_size[0][0], btn_size[0][1])
        btn_dc.setMaximumSize(btn_size[1][0], btn_size[1][1])
        btn_dc.connect(btn_dc, QtCore.SIGNAL('clicked()'), self.handle_open_dc)
        btn_dc.setIcon(QtGui.QIcon(icons.DATA_COLLECTION))
        btn_dc_hint = "Data Collection"
        btn_dc.setText(btn_dc_hint)
        btn_dc.setStatusTip(btn_dc_hint)

        btn_dp = QtGui.QPushButton()
        btn_dp.setMinimumSize(btn_size[0][0], btn_size[0][1])
        btn_dp.setMaximumSize(btn_size[1][0], btn_size[1][1])
        btn_dp.connect(btn_dp, QtCore.SIGNAL('clicked()'), self.handle_open_dp)
        btn_dp.setIcon(QtGui.QIcon(icons.DATA_PROCESSING))
        btn_dp_hint = "Data Processing"
        btn_dp.setText(btn_dp_hint)
        btn_dp.setStatusTip(btn_dp_hint)
        btn_dp.setDisabled(True) # TODO: Remove when implemented

        btn_dv = QtGui.QPushButton()
        btn_dv.setMinimumSize(btn_size[0][0], btn_size[0][1])
        btn_dv.setMaximumSize(btn_size[1][0], btn_size[1][1])
        btn_dv.connect(btn_dv, QtCore.SIGNAL('clicked()'), self.handle_open_dv)
        btn_dv.setIcon(QtGui.QIcon(icons.DATA_VIEWER))
        btn_dv_hint = "Data Viewer"
        btn_dv.setText(btn_dv_hint)
        btn_dv.setStatusTip(btn_dv_hint)
        btn_dv.setDisabled(True) # TODO: Remove when implemented

        layout.addWidget(btn_sample, 1, 1)
        layout.addWidget(btn_dc, 1, 3)
        layout.addWidget(btn_dp, 3, 1)
        layout.addWidget(btn_dv, 3, 3)

        layout.sizeConstraint = QtGui.QLayout.SetDefaultConstraint
        self.setCentralWidget(self.main_widget)

    def handle_open_sample(self):
        s_manager = SampleManager(parent=self, app_state=self.app_state)

    def handle_open_dc(self):
        s_collection = DataCollection(parent=self, app_state=self.app_state)

    def handle_open_dp(self):
        pass

    def handle_open_dv(self):
        pass
