from PyQt4 import QtGui
from lixdc.widgets import icons
from lixdc.widgets.base import BaseWidget
from lixdc.widgets.tab_windowless_setup import WindowlessSetup
from lixdc.widgets.tab_flowcell_setup import FlowCellSetup
from lixdc.widgets.tab_flowmixer_setup import FlowMixerSetup
from lixdc.widgets.tab_hplc_setup import HPLCSetup


class DataCollection(QtGui.QDialog, BaseWidget):
    def __init__(self, parent, app_state=None):
        super(DataCollection, self).__init__(parent)
        self.app_state = app_state
        self.init_ui()

    def init_ui(self):
        self.create_tabs()

        self.setWindowTitle('LIX Data Collection')
        self.center(w=800, h=600)
        #self.showMaximized()
        self.show()

    def create_tabs(self):
        self.layout = QtGui.QVBoxLayout()
        tab_widget = QtGui.QTabWidget()

        tab1 = WindowlessSetup()
        tab2 = FlowCellSetup()
        tab3 = FlowMixerSetup()
        tab4 = HPLCSetup(parent=self, app_state=self.app_state)

        #tab_widget.addTab(tab1, "Windowless Setup")
        #tab_widget.addTab(tab2, "Flow Cell Setup")
        #tab_widget.addTab(tab3, "Flow Mixer Setup")
        tab_widget.addTab(tab4, "HPLC")
        self.layout.addWidget(tab_widget)
        self.setLayout(self.layout)
