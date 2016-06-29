from functools import partial
from collections import OrderedDict

from PyQt4 import QtGui, QtCore

from lixdc.widgets import icons
from lixdc.widgets.plate import Plate

import lixdc.db.sample as db_sample
import lixdc.state.general as state_general

class WindowlessSetup(QtGui.QWidget):

    def __init__(self):
        super(WindowlessSetup, self).__init__()
        self.filter_sample_table = True
        self.currentPlate = None
        self.plate = None
        self.table = None
        self.table_items = OrderedDict()
        self.plate_docking = []
        self.init_ui()

    def init_ui(self):
        font = QtGui.QFont()
        font.setBold(True)
        # font.setPointSize(20)

        lbl = QtGui.QLabel(self)
        lbl.move(20, 0)
        lbl.setFont(font)
        lbl.setText("Current Plate:")

        self.currentPlate = QtGui.QLabel(self)
        self.currentPlate.move(110, 0)
        self.currentPlate.setText("Select or Create a Plate")

        self.create_plate()
        self.create_table()
        self.create_sample_docking()

    def create_plate(self):
        self.plate = Plate(self)
        self.plate.move(20, 20)
        self.plate.clicked_callback(self.well_clicked)

    def create_table(self):
        font = QtGui.QFont()
        font.setPointSize(20)

        self.table = QtGui.QTableWidget(self)
        self.table.setFont(font)
        self.table.setColumnCount(1)  # Sample Name
        self.table.setColumnWidth(0, 400)
        self.table.setRowCount(96)  # 96 wells plate
        self.table.setHorizontalHeaderLabels(['Sample'])

        vertical_header_labels = []

        for col in range(1, 13):  # From 1 to 12
            for row in range(ord('A'), ord('I')):  # From A to H
                idx = (row-ord('A'))+(col-1)*(ord('I')-ord('A'))
                position_id = str(col-1)+"-"+str(row-ord('A'))  # 0-0, 0-1... internal identifier
                position_text = str(col)+"-"+chr(row)  # 1-A, 1-B, 1-C... user-friendly identifier
                vertical_header_labels.append(position_text)

                self.table_items[position_id] = QtGui.QTableWidgetItem()
                self.table_items[position_id].setTextAlignment(QtCore.Qt.AlignLeft+QtCore.Qt.AlignVCenter)
                self.table.setItem(idx, 0, self.table_items[position_id])

        self.table.setVerticalHeaderLabels(vertical_header_labels)
        self.table.move(600, 20)
        #self.table.setMinimumHeight(990)
        self.table.setMinimumHeight(700)
        self.table.setMinimumWidth(500)

    def _fill_sample_table(self, samples):
        for s in samples:
            print("Sample: ", s)
            position_id = str(s["position"]["y"]-1)+"-"+str(s["position"]["x"]-1)
            sample_name = s["name"]
            self.table_items[position_id].setText(sample_name)

    def _update_screen_with_plate_info(self, plate):
        self.currentPlate.setText(plate["name"])
        self._fill_sample_table(plate["content"])

    def create_sample_docking(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(20)

        lbl = QtGui.QLabel(self)
        lbl.move(20, 20+self.plate.size[1]+50)
        lbl.setFont(font)
        lbl.setText("Sample Docking Station")

        position_x = lbl.pos().x()
        position_y = lbl.pos().y()

        for i in range(0, 5):
            self.plate_docking.append(self._create_plate_docking(i, position_x, position_y+50*(i+1)))

    def _create_plate_docking(self, idx, pos_x, pos_y):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(20)

        lbl = QtGui.QLabel(self)
        lbl.move(pos_x, pos_y)
        lbl.setText(str(idx+1))
        lbl.setFont(font)

        DOCKING_EMPTY = "background-color: #FAFAFA; border: 2px dashed #484848; "  # border-radius: 15px;"
        DOCKING_MEASURING = "background-color: #58FAAC; border: 2px solid #484848; "  # border-radius: 15px;"
        DOCKING_SAVE_PENDING = "background-color: #F2F5A9; border: 2px solid #484848; "  # border-radius: 15px;"
        DOCKING_NORMAL = "background-color:#6E6E6E; border: 2px solid #484848; "

        style = [DOCKING_MEASURING, DOCKING_NORMAL, DOCKING_SAVE_PENDING, DOCKING_EMPTY, DOCKING_EMPTY]

        lbl_plate = QtGui.QLabel(self)
        lbl_plate.setStyleSheet(style[idx])
        lbl_plate.setMinimumSize(300, 40)
        lbl_plate.move(pos_x+20, pos_y-10)

        btn_add = QtGui.QPushButton(self)
        #btn_add.move(pos_x+320, pos_y-8)
        btn_add.move(pos_x+330, pos_y-18)
        btn_add.setMinimumSize(40, 40)
        btn_add.connect(btn_add, QtCore.SIGNAL('clicked()'), partial(self._handle_add_dock_click, idx))
        btn_add.setIcon(QtGui.QIcon(icons.ADD))
        btn_add_hint = "Add a new plate to the docking station #"+str(idx+1)
        btn_add.setStatusTip(btn_add_hint)

        btn_load = QtGui.QPushButton(self)
        #btn_load.move(pos_x+375, pos_y-8)
        btn_load.move(pos_x+405, pos_y-18)
        btn_load.setMinimumSize(40, 40)
        btn_load.connect(btn_load, QtCore.SIGNAL('clicked()'), partial(self._handle_load_dock_click, idx))
        btn_load.setIcon(QtGui.QIcon(icons.FIND))
        btn_load_hint = "Load a existing plate to the docking station #"+str(idx+1)
        btn_load.setStatusTip(btn_load_hint)
        
        btn_import = QtGui.QPushButton(self)
        #btn_import.move(pos_x+430, pos_y-8)
        btn_import.move(pos_x+480, pos_y-18)
        btn_import.setMinimumSize(40, 40)
        btn_import.connect(btn_import, QtCore.SIGNAL('clicked()'), partial(self._handle_import_dock_click, idx))
        btn_import.setIcon(QtGui.QIcon(icons.IMPORT))
        btn_import_hint = "Import a new plate to the docking station #"+str(idx+1)
        btn_import.setStatusTip(btn_import_hint)

        return lbl_plate

    def _handle_add_dock_click(self, idx):
        # TODO: Finish method implementation
        print("Adding new plate to Dock Station #", idx)

    def _handle_load_dock_click(self, idx):
        # TODO: Finish method implementation
        print("Loading existing plate to Dock Station #", idx)
        barcode, ok = QtGui.QInputDialog.getText(self, 'Loading plate', 'Enter your plate barcode:')
        if ok:
            barcode = barcode.zfill(13)
            plate_info = db_sample.find_plate_by_barcode(state_general.owner, state_general.project, state_general.beamline_id, barcode, fill=True)
            if plate_info is None:
                QtGui.QMessageBox.critical(self, "Not Found", "Plate not found with barcode: {}!".format(barcode))
            else:
                self._update_screen_with_plate_info(plate_info)


    def _handle_import_dock_click(self, idx):
        # TODO: Finish method implementation
        print("Importing new plate to Dock Station #", idx)
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select File to import', '~')
        if fname != "":
            plate_info = db_sample.import_plate_from_excel(fname, state_general.owner, state_general.project, state_general.beamline_id, "96wp")
            self._update_screen_with_plate_info(plate_info)



    def well_clicked(self, selected_items):
        scroll = True

        for item_name, item in self.table_items.items():
            item.setSelected(False)

        for item in selected_items:
            table_item = self.table_items[item[0]+"-"+item[1]]
            table_item.setSelected(True)

            if scroll:
                self.table.scrollToItem(table_item)
                scroll = False

        if self.filter_sample_table:
            for item_name, item in self.table_items.items():
                if len(selected_items) > 0:
                    self.table.setRowHidden(item.row(), not item.isSelected())
                else:
                    self.table.setRowHidden(item.row(), False)
