import time
import pandas
import datetime
import collections
from enum import Enum
from PyQt4 import QtGui, QtCore
from lixdc.widgets.base import BaseWidget
from lixdc.db import sample as sample_db
import lixdc.utils as utils


class ContainerFinder(QtGui.QDialog, BaseWidget):

    def __init__(self, parent, app_state=None):
        super(ContainerFinder, self).__init__(parent)
        self.setModal(True)
        self.selected_entry = None
        self.app_state = app_state
        self.containers_data = []
        self.init_ui()
        self.filter_containers()

    def init_ui(self):
        self.setWindowTitle('Container Finder')
        self.center(w=880, h=600)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # TAB SEARCH

        self.tab_search = QtGui.QWidget()
        self.tab_search_layout = QtGui.QVBoxLayout()
        self.tab_search.setLayout(self.tab_search_layout)
        self.create_search_panel(parent=self.tab_search)
        self.create_action_buttons(parent=self.tab_search)
        self.create_containers_table(parent=self.tab_search)

        layout.addWidget(self.tab_search)


    #####################################
    ###  Container query section
    #####################################

    def create_search_panel(self, parent):
        layout = parent.layout()
        frm_l1 = QtGui.QFormLayout()
        frm_l1.setVerticalSpacing(2)
        frm_l1.setHorizontalSpacing(2)

        lbl_type = QtGui.QLabel(parent=parent)
        lbl_type.setText('Type: ')
        self.cmb_type = QtGui.QComboBox(parent=parent)
        self.cmb_type.addItems(['']+list(sample_db.CONTAINER_TYPES))
        self.cmb_type.setMaximumWidth(300)

        lbl_container_name = QtGui.QLabel(parent=parent)
        lbl_container_name.setText('Name: ')
        self.txt_container_name = QtGui.QLineEdit(parent=parent)
        self.txt_container_name.setMaximumWidth(400)

        lbl_container_barcode = QtGui.QLabel(parent=parent)
        lbl_container_barcode.setText('Barcode: ')
        self.txt_container_barcode = QtGui.QLineEdit(parent=parent)
        self.txt_container_barcode.setMaximumWidth(200)

        frm_l1.addRow(lbl_type, self.cmb_type)
        frm_l1.addRow(lbl_container_name, self.txt_container_name)
        frm_l1.addRow(lbl_container_barcode, self.txt_container_barcode)

        layout.addItem(frm_l1)

    def create_action_buttons(self, parent):
        layout = parent.layout()
        horz_l1 = QtGui.QHBoxLayout()

        self.btn_search = QtGui.QPushButton(parent=parent)
        self.btn_search.setText('Search')
        self.btn_search.connect(self.btn_search, QtCore.SIGNAL('clicked()'), self.filter_containers)

        horz_l1.addWidget(self.btn_search)

        layout.addItem(horz_l1)

    def create_containers_table(self, parent):
        layout = parent.layout()
        horz_l2 = QtGui.QHBoxLayout()

        self.containers_table = QtGui.QTableWidget(parent=parent)
        self.containers_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.containers_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        header = ['Type', 'Name', 'Barcode', 'Last Modified']
        self.containers_table.setColumnCount(len(header))
        self.containers_table.setColumnWidth(0, 80)
        self.containers_table.setColumnWidth(1, 4*80)
        self.containers_table.setColumnWidth(2, 2*80)
        self.containers_table.setColumnWidth(3, 2*80)
        self.containers_table.setHorizontalHeaderLabels(header)
        self.containers_table.doubleClicked.connect(self.handle_table_click)

        horz_l2.addWidget(self.containers_table)
        layout.addItem(horz_l2)

    def filter_containers(self):
        params = dict()

        params['owner'] = self.app_state.user
        params['project'] = self.app_state.project
        params['beamline_id'] = self.app_state.beamline_id

        if self.cmb_type.currentText() != '':
            params['kind'] = sample_db.CONTAINER_TYPES[self.cmb_type.currentText()]['id']
        if self.txt_container_name.text() != '':
            params['name'] = {"$regex": self.txt_container_name.text()}
        if self.txt_container_barcode.text() != '':
            params['barcode'] = {"$regex": self.txt_container_barcode.text()}

        results = list(sample_db.find_containers(**params))
        self.update_containers_table(results)

    def update_containers_table(self, data):
        self.containers_data = data
        self.containers_table.setRowCount(0)
        self.containers_table.setRowCount(len(data))
        for idx, c in enumerate(data):
            self.containers_table.setItem(idx, 0, QtGui.QTableWidgetItem(c['kind']))
            self.containers_table.setItem(idx, 1, QtGui.QTableWidgetItem(c['name']))
            self.containers_table.setItem(idx, 2, QtGui.QTableWidgetItem(c['barcode']))
            tstr = datetime.datetime.fromtimestamp(c['time']).strftime("%D %H:%M:%S")
            self.containers_table.setItem(idx, 3, QtGui.QTableWidgetItem(tstr))


    def handle_table_click(self, mi):
        data = self.containers_data[mi.row()]
        sample_db.fill_container(data)
        self.selected_entry = data
        self.close()
