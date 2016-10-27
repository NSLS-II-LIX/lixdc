import time
import pandas
import datetime
import collections
from enum import Enum
from PyQt4 import QtGui, QtCore
from lixdc.widgets.base import BaseWidget
from lixdc.db import sample as sample_db
import lixdc.utils as utils

class ScreenMode(str, Enum):
    search = "search"
    new = "new"
    edit = "edit"


class SampleManager(QtGui.QDialog, BaseWidget):

    def __init__(self, parent, app_state=None):
        super(SampleManager, self).__init__(parent)
        self.app_state = app_state
        self.containers_data = []
        self.edit_data = None
        self.init_ui()
        self.filter_containers()
        self.mode = ScreenMode.search
        self.type_selection = None

    def init_ui(self):
        self.setWindowTitle('Sample Manager')
        self.center(1080, 600)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QtGui.QStackedWidget()

        # TAB SEARCH

        self.tab_search = QtGui.QWidget()
        self.tab_search_layout = QtGui.QVBoxLayout()
        self.tab_search.setLayout(self.tab_search_layout)

        self.create_search_panel(parent=self.tab_search)
        self.create_action_buttons(parent=self.tab_search)
        self.create_containers_table(parent=self.tab_search)

        # TAB EDIT

        self.tab_edit = QtGui.QWidget()
        self.tab_edit_layout = QtGui.QVBoxLayout()
        self.tab_edit.setLayout(self.tab_edit_layout)

        self.create_new_edit_panel(parent=self.tab_edit)

        self.tabs.addWidget(self.tab_search)
        self.tabs.addWidget(self.tab_edit)
        self.tabs.setCurrentIndex(0)

        layout.addWidget(self.tabs)

        self.show()


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

        self.btn_new = QtGui.QPushButton(parent=parent)
        self.btn_new.setText('Add New')
        self.btn_new.connect(self.btn_new, QtCore.SIGNAL('clicked()'), self.handle_new)

        self.btn_import = QtGui.QPushButton(parent=parent)
        self.btn_import.setText('Import from File')
        self.btn_import.connect(self.btn_import, QtCore.SIGNAL('clicked()'), self.handle_import)

        horz_l1.addWidget(self.btn_search)
        horz_l1.addWidget(self.btn_new)
        horz_l1.addWidget(self.btn_import)

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
        self.containers_table.doubleClicked.connect(self.handle_table_edit)

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


    #####################################
    ###  Container modification section
    #####################################

    def create_new_edit_panel(self, parent):
        layout_outer = parent.layout()
        layout_top = QtGui.QHBoxLayout()

        layout_cont_form = QtGui.QFormLayout()
        layout_cont_form.setVerticalSpacing(2)
        layout_cont_form.setHorizontalSpacing(2)
        layout_actions = QtGui.QHBoxLayout()

        self.lbl_picture = QtGui.QLabel(parent=parent)
        self.lbl_picture.setPixmap(QtGui.QPixmap("96wp.png"))

        self.cmb_type_ins = QtGui.QComboBox(parent=parent)
        for idx, tp in enumerate(sample_db.CONTAINER_TYPES):
            self.cmb_type_ins.insertItem(idx, tp)
            type_id = sample_db.CONTAINER_TYPES[tp]['id']
            self.cmb_type_ins.setItemData(idx, type_id)
        self.cmb_type_ins.setMaximumWidth(300)
        self.cmb_type_ins.connect(self.cmb_type_ins, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_picture)
        self.cmb_type_ins.connect(self.cmb_type_ins, QtCore.SIGNAL("currentIndexChanged(int)"), self.secure_type_change)
        self.change_picture(-1)

        self.txt_name_ins = QtGui.QLineEdit(parent=parent)
        self.txt_name_ins.setMaximumWidth(400)

        self.txt_barcode_ins = QtGui.QLineEdit(parent=parent)
        self.txt_barcode_ins.setMaximumWidth(200)

        layout_cont_form.addRow(QtGui.QLabel("Type: ", parent=parent), self.cmb_type_ins)
        layout_cont_form.addRow(QtGui.QLabel("Name: ", parent=parent), self.txt_name_ins)
        layout_cont_form.addRow(QtGui.QLabel("Barcode: ", parent=parent), self.txt_barcode_ins)

        self.samples_table = QtGui.QTableWidget(parent=parent)
        header = ['UID', 'Pos.', 'Name', 'Short Name', 'Conc. (mg/ml)', 'Vol. (ul)', 'Temp. (C)']
        self.samples_table.setColumnCount(len(header))
        self.samples_table.setColumnWidth(0, 350) # UID
        self.samples_table.setColumnWidth(1, 50) # Pos.
        self.samples_table.setColumnWidth(2, 2*80) # Name
        self.samples_table.setColumnWidth(3, 1*80) # Short Name
        self.samples_table.setColumnWidth(4, 80) # Conc.
        self.samples_table.setColumnWidth(5, 80) # Volume
        self.samples_table.setColumnWidth(6, 80) # Temperature

        self.samples_table.setHorizontalHeaderLabels(header)

        self.btn_save_ins = QtGui.QPushButton(parent=parent)
        self.btn_save_ins.setText("Save")
        self.btn_save_ins.connect(self.btn_save_ins, QtCore.SIGNAL('clicked()'), self.save_changes)

        self.btn_cancel_ins = QtGui.QPushButton(parent=parent)
        self.btn_cancel_ins.setText("Cancel")
        self.btn_cancel_ins.connect(self.btn_cancel_ins, QtCore.SIGNAL('clicked()'), self.cancel_changes)

        layout_actions.addWidget(self.btn_save_ins)
        layout_actions.addWidget(self.btn_cancel_ins)

        layout_top.addItem(layout_cont_form)
        layout_top.addWidget(self.lbl_picture)

        layout_outer.addItem(layout_top)
        layout_outer.addWidget(self.samples_table)
        layout_outer.addItem(layout_actions)

        parent.setLayout(layout_outer)

    def change_picture(self, idx):
        pmap = sample_db.CONTAINER_TYPES[self.cmb_type_ins.currentText()]['image']
        self.lbl_picture.setPixmap(QtGui.QPixmap(pmap))

    def save_changes(self):
        # TODO: Persist the data and return...
        # Before anything, if mode == 'Edit':
        # Check if last_modified_date > in_memory_one
        # If it is, someone also changed this entry and we need to alert the user
        # Maybe suggest a diff?
        # Initially just present a confirmation message.

        cont_info = sample_db.CONTAINER_TYPES[self.cmb_type_ins.currentText()]
        sample_payload = []

        for col in range(cont_info['cols']):
            for row in range(cont_info['rows']):
                idx = row + col*cont_info['rows']
                col_text = chr(ord('@') + col + 1) if cont_info["cols_letters"] else col + 1
                row_text = chr(ord('@') + row + 1) if cont_info["rows_letters"] else row + 1
                try:
                    s_uid = self.samples_table.item(idx, 0).text()
                    s_pos = {'x': col, 'y': row}
                    s_name = self.samples_table.item(idx, 2).text()
                    s_sname = self.samples_table.item(idx, 3).text()

                    # We will ignore if all string fields are empty
                    if s_uid == "" and s_name == "" and s_sname == "":
                        continue

                    s_conc = float(self.samples_table.item(idx, 4).text())
                    s_vol = float(self.samples_table.item(idx, 5).text())
                    s_temp = float(self.samples_table.item(idx, 6).text())
                    datum = {
                         'uid': s_uid,
                         'name': s_name,
                         'short_name': s_sname,
                         'position': s_pos,
                         'concentration': s_conc,
                         'volume': s_vol,
                         'temperature': s_temp
                        }
                    datum.update(self.app_state.get_default_fields())
                    sample_payload.append(datum)
                    ret, msg = sample_db.validate_sample(sample_payload[-1])
                    if not ret:
                        e_txt = 'Error at sample: {}-{}'.format(row_text, col_text)
                        e_detail = msg
                        e_title = 'Error validating sample information'
                        utils.show_error(e_txt, e_detail, e_title)
                        return

                except Exception as e:
                    e_txt = "Error parsing sample information"
                    e_detail = "Please check the content of the table.\n{}".format(str(e))
                    e_title = "Error"
                    utils.show_error(e_txt, e_detail, e_title)
                    return

        try:
            # Update the container info, and set content to be the list of sample_uids
            content = sample_db.upsert_sample_list(sample_payload)

            if self.mode == ScreenMode.edit:
                cont = self.edit_data[0]
            else:
                cont = {}

            cont['kind'] = self.cmb_type_ins.itemData(self.cmb_type_ins.currentIndex())
            cont['name'] = self.txt_name_ins.text()
            cont['barcode'] = self.txt_barcode_ins.text()
            cont['content'] = content
            cont['time'] = time.time()
            cont.update(self.app_state.get_default_fields())

            sample_db.upsert_container(cont)
        except Exception as e:
            e_txt = "Error saving data"
            e_detail = "Please check the error.\n{}".format(str(e))
            e_title = "Error"
            utils.show_error(e_txt, e_detail, e_title)
            return

        self.cleanup_new_edit()

    def cancel_changes(self):
        self.mode = ScreenMode.search
        self.edit_data = None
        self.cleanup_new_edit()

    def cleanup_new_edit(self):
        self.txt_name_ins.setText("")
        self.txt_barcode_ins.setText("")
        self.samples_table.setRowCount(0)
        self.tabs.setCurrentIndex(0)
        self.filter_containers()

    def handle_table_edit(self, mi):
        data = self.containers_data[mi.row()]
        sample_db.fill_container(data)
        self.edit_data = data, data['content']

        # Fill the fields and the samples table in here.
        self.fill_screen()

        # Set mode to 'Edit'
        self.mode = ScreenMode.edit
        # Switch to the other tab
        self.tabs.setCurrentIndex(1)

    def handle_new(self):
        # Set mode to 'New'
        self.mode = ScreenMode.new

        self.edit_data = None

        # Switch to the other tab
        self.type_selection = 0
        self.fill_samples_table_header()
        self.tabs.setCurrentIndex(1)

    def handle_import(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Import Container", "",
                                            "Container Files (*.xls *.xlsx *.csv)")

        if fname != "":
            # Fill the fields and the sample table in here
            self.edit_data = self.read_import_file(fname)
            self.fill_screen()
            # Set mode to 'New'
            self.mode = ScreenMode.new
            # Switch to the other tab
            self.tabs.setCurrentIndex(1)

    def secure_type_change(self, idx):
        if self.type_selection != idx:
            r = utils.show_question('Are you sure you want to change the container type?', 'WARNING: If you choose to proceed, all data will be wiped from the table.', 'Confirmation')
            if r == utils.ANSWER_OK:
                # Need to refil the samples table...
                self.type_selection = idx
                self.fill_samples_table_header()
            else:
                # Need to revert the selection...
                self.cmb_type_ins.blockSignals(True)
                self.cmb_type_ins.setCurrentIndex(self.type_selection)
                self.change_picture(idx=idx)
                self.cmb_type_ins.blockSignals(False)

    def fill_samples_table_header(self):
        cont_info = sample_db.CONTAINER_TYPES[self.cmb_type_ins.currentText()]

        # fill sample information at table
        self.samples_table.setRowCount(0)
        sample_items = cont_info['cols']*cont_info['rows']
        self.samples_table.setRowCount(sample_items)

        for col in range(cont_info['cols']):
            for row in range(cont_info['rows']):
                idx = row + col*cont_info['rows']
                col_text = chr(ord('@') + col + 1) if cont_info["cols_letters"] else col + 1
                row_text = chr(ord('@') + row + 1) if cont_info["rows_letters"] else row + 1
                pos_item = QtGui.QTableWidgetItem('{}-{}'.format(row_text, col_text))
                pos_item.setTextAlignment(QtCore.Qt.AlignCenter)
                pos_item.setFlags(QtCore.Qt.ItemIsSelectable)
                self.samples_table.setItem(idx, 1, pos_item)
                self.samples_table.setItem(idx, 0, QtGui.QTableWidgetItem(""))
                self.samples_table.setItem(idx, 2, QtGui.QTableWidgetItem(""))
                self.samples_table.setItem(idx, 3, QtGui.QTableWidgetItem(""))
                self.samples_table.setItem(idx, 4, QtGui.QTableWidgetItem(""))
                self.samples_table.setItem(idx, 5, QtGui.QTableWidgetItem(""))
                self.samples_table.setItem(idx, 6, QtGui.QTableWidgetItem(""))


    def fill_screen(self):
        container, samples = self.edit_data

        # fill container information
        type_idx = self.cmb_type_ins.findData(container['kind'])
        self.type_selection = type_idx
        self.cmb_type_ins.setCurrentIndex(type_idx)

        self.fill_samples_table_header()
        self.txt_name_ins.setText(container['name'])
        self.txt_barcode_ins.setText(container['barcode'])

        cont_info = sample_db.CONTAINER_TYPES[self.cmb_type_ins.currentText()]


        for s in samples:
            col, row = s['position']['x'], s['position']['y']
            idx = row + col*cont_info['rows']


            self.samples_table.item(idx, 0).setText(s['uid'] if s['uid'] is not None else "")
            self.samples_table.item(idx, 2).setText(s['name'])
            self.samples_table.item(idx, 3).setText(s['short_name'] if 'short_name' in s else "")
            self.samples_table.item(idx, 4).setText(str(s['concentration']))
            self.samples_table.item(idx, 5).setText(str(s['volume']))
            self.samples_table.item(idx, 6).setText(str(s['temperature']))

    def read_import_file(self, fname):
        samples = collections.deque()
        excel_data = pandas.read_excel(fname,header=1)

        for line in excel_data.iterrows():
            if line[0] == 0:
                name = line[1][0]
                kind = line[1][1]
                barcode = str(int(line[1][2])).zfill(13)
                plate_info = {
                    "uid": None,
                    "owner": self.app_state.user,
                    "project": self.app_state.project,
                    "beamline_id": self.app_state.beamline_id,
                    "kind": kind,
                    "name": name,
                    "barcode": barcode,
                }
            s_y = int(line[1][3])-1
            s_x = int(line[1][4])-1
            s_name = line[1][5]
            s_shortname = line[1][6]
            s_conc = line[1][7]
            s_volume = line[1][8]
            s_temperature = line[1][9]
            sample_info = {
                    "uid": None,
                    "project": self.app_state.project,
                    "beamline_id": self.app_state.beamline_id,
                    "owner": self.app_state.user,
                    "name": s_name,
                    "short_name": s_shortname,
                    "position": {"x": s_x, "y": s_y},
                    "concentration": s_conc,
                    "volume": s_volume,
                    "temperature": s_temperature
                }
            samples.append(sample_info)


        return plate_info, samples
