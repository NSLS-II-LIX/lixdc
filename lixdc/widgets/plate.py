from PyQt4 import QtGui, QtCore


class Well(QtGui.QLabel):
    COLOR_EMPTY = "rgb(255, 255, 255)"
    COLOR_SELECTED = "rgb(0, 255, 0)"
    STYLE = "background-color: {}; border: 2px solid black; border-radius: 15px;"

    def __init__(self, parent=None, name=""):
        super(Well, self).__init__(parent)
        self.name = name
        self.selected = False
        self.setFixedSize(30, 30)
        self.setStyleSheet(Well.STYLE.format(Well.COLOR_EMPTY))

    def __str__(self):
        return "Well: {}".format(self.name)

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.emit(QtCore.SIGNAL("clicked()"))
        elif ev.button() == QtCore.Qt.RightButton:
            self.emit(QtCore.SIGNAL("right-clicked()"))
        else:
            print("Not implemented")

    def select(self):
        self.setStyleSheet(Well.STYLE.format(Well.COLOR_SELECTED))
        self.selected = True

    def deselect(self):
        self.setStyleSheet(Well.STYLE.format(Well.COLOR_EMPTY))
        self.selected = False


class Plate(QtGui.QFrame):
    def __init__(self, parent=None):
        super(Plate, self).__init__(parent)
        self.wells = []

        self.setStyleSheet("background-color:#6E6E6E;")
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Raised)
        self.setLineWidth(3)
        self.size = (540, 370)
        self.resize(self.size[0], self.size[1])
        self.setMaximumSize(self.size[0], self.size[1])

        self.init_legend()
        self.init_wells()

        self.previous_col = None
        self.previous_row = None

    def __str__(self):
        return "Plate"

    def clicked_callback(self, cb):
        self.clicked_cb = cb

    def init_legend(self):
        space = 10
        size = 30

        label_font = QtGui.QFont()
        label_font.setBold(True)
        label_font.setPointSize(20)

        idx = 1
        for row in range(ord('A'), ord('I')):  # From A to H
            label = QtGui.QLabel(self)
            label.setFont(label_font)
            label.setStyleSheet("color: #A4A4A4;")
            label.setText(chr(row))
            label.move(space, idx*(size+space)+space/2)
            idx += 1

        for col in range(1, 13):  # From 1 to 12
            label = QtGui.QLabel(self)
            label.setFont(label_font)
            label.setStyleSheet("color: #A4A4A4;")
            label.setText(str(col))
            label.move(col*(size+space)+space/2, space)

    def init_wells(self):
        space = 10
        size = 30

        for row in range(1, 9):
            line = []
            for col in range(1, 13):
                sample = Well(self, name=str(col-1)+"-"+str(row-1))
                sample.move(col*(size+space), row*(size+space))
                self.connect(sample, QtCore.SIGNAL('clicked()'), self.well_clicked)
                line.append(sample)
            self.wells.append(line)

    def deselect_all(self):
        for line in self.wells:
            for well in line:
                well.deselect()

    def get_selected(self):
        selected = []
        for line in self.wells:
            for well in line:
                if well.selected:
                    col, row = well.name.split("-")
                    selected.append((col, row))

        return selected

    def well_clicked(self):
        #print("Clicked @ Well: ", self.sender().name)
        col, row = self.sender().name.split("-")
        col = int(col)
        row = int(row)

        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ShiftModifier:
            # print('Shift+Click')

            c_start = self.previous_col if self.previous_col < col else col
            c_end = col if self.previous_col < col else self.previous_col
            r_start = self.previous_row if self.previous_row < row else row
            r_end = row if self.previous_row < row else self.previous_row

            for c in range(c_start, c_end+1):
                for r in range(r_start, r_end+1):
                    self.wells[r][c].select()
        elif modifiers == QtCore.Qt.ControlModifier:
            # print('Control+Click')
            self.sender().select()
        else:
            # print('Click')
            previous_selected = self.sender().selected
            self.deselect_all()
            if not previous_selected:
                self.sender().select()

        self.previous_col = col
        self.previous_row = row

        if self.clicked_cb is not None:
            self.clicked_cb(self.get_selected())

