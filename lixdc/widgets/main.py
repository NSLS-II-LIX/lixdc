from PyQt4 import QtGui
from lixdc.widgets import icons
from lixdc.widgets.tab_windowless_setup import WindowlessSetup
from lixdc.widgets.tab_flowcell_setup import FlowCellSetup
from lixdc.widgets.tab_flowmixer_setup import FlowMixerSetup
from lixdc.widgets.tab_hplc_setup import HPLCSetup


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        # self.initCallbacks()

    def init_ui(self):
        self.statusBar()

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)  # Handles OSX issues with MenuBar
        fileMenu = menu_bar.addMenu('&File')
        exitAction = QtGui.QAction(QtGui.QIcon(icons.CLOSE), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the application')
        exitAction.triggered.connect(self.close)

        fileMenu.addAction(exitAction)

        self.create_tabs()

        self.setWindowTitle('LIX Data Collection')
        self.center()
        self.showMaximized()
        self.show()

    def create_tabs(self):
        tab_widget = QtGui.QTabWidget()

        tab1 = WindowlessSetup()
        tab2 = FlowCellSetup()
        tab3 = FlowMixerSetup()
        tab4 = HPLCSetup()

        tab_widget.addTab(tab1, "Windowless Setup")
        tab_widget.addTab(tab2, "Flow Cell Setup")
        tab_widget.addTab(tab3, "Flow Mixer Setup")
        tab_widget.addTab(tab4, "HPLC")
        self.setCentralWidget(tab_widget)


    def center(self):
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(screen).center()
        available_rect = QtGui.QApplication.desktop().availableGeometry(screen)

        x = 0
        y = available_rect.y()
        w = available_rect.width()
        h = available_rect.height()

        w_factor = 0.8
        h_factor = 0.8
        w = int((w - x) * w_factor)
        h = int((h - y) * h_factor)

        self.setGeometry(0, 0, w, h)

        frame_geom = self.frameGeometry()
        frame_geom.moveCenter(center_point)

        self.move(frame_geom.topLeft())
