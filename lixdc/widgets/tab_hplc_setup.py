import time
from PyQt4 import QtGui, QtCore
from lixdc.widgets.finder import ContainerFinder
from lixdc.db import sample as sample_db, request as request_db
import lixdc.utils as utils

class HPLCSetup(QtGui.QWidget):

    def __init__(self, parent, app_state=None):
        super(HPLCSetup, self).__init__(parent)
        self.app_state = app_state
        self.init_ui()

    def init_ui(self):
        self.layout = QtGui.QVBoxLayout()
        frame = QtGui.QFrame(self)
        frame.setFrameShape(QtGui.QFrame.StyledPanel)
        frame.setFrameShadow(QtGui.QFrame.Sunken)
        frame_layout = QtGui.QFormLayout(frame)

        lbl_cont = QtGui.QLabel(frame)
        lbl_cont.setText('Container Info:')

        lbl_cont_uid = QtGui.QLabel(frame)
        lbl_cont_uid.setText('UID: ')
        self.txt_cont_uid = QtGui.QLineEdit()
        self.txt_cont_uid.setDisabled(True)

        lbl_cont_name = QtGui.QLabel(frame)
        lbl_cont_name.setText('Name: ')
        self.txt_cont_name = QtGui.QLineEdit()
        self.txt_cont_name.setDisabled(True)

        lbl_cont_barcode = QtGui.QLabel(frame)
        lbl_cont_barcode.setText('Barcode: ')
        self.txt_cont_barcode = QtGui.QLineEdit()
        self.txt_cont_barcode.setDisabled(True)

        frame_layout.addRow(lbl_cont, None)
        frame_layout.addRow(lbl_cont_uid, self.txt_cont_uid)
        frame_layout.addRow(lbl_cont_name, self.txt_cont_name)
        frame_layout.addRow(lbl_cont_barcode, self.txt_cont_barcode)

        self.btn_lookup_plate = QtGui.QPushButton(parent=self)
        self.btn_lookup_plate.setText('Lookup Plate')
        self.btn_lookup_plate.connect(self.btn_lookup_plate, QtCore.SIGNAL('clicked()'), self.lookup_plate)

        self.btn_gen_batch = QtGui.QPushButton(parent=self)
        self.btn_gen_batch.setText('Generate Batch File')
        self.btn_gen_batch.connect(self.btn_gen_batch, QtCore.SIGNAL('clicked()'), self.gen_batch)
        self.btn_gen_batch.setDisabled(True)

        frame_def = QtGui.QFrame(self)
        frame_def.setFrameShape(QtGui.QFrame.StyledPanel)
        frame_def.setFrameShadow(QtGui.QFrame.Sunken)

        frame_def_layout = QtGui.QFormLayout(frame_def)
        lbl_method1 = QtGui.QLabel(frame_def)
        lbl_method1.setText('Method 1: ')
        self.txt_method1 = QtGui.QLineEdit()
        lbl_method2 = QtGui.QLabel(frame_def)
        lbl_method2.setText('Method 2: ')
        self.txt_method2 = QtGui.QLineEdit()

        self.btn_set_def = QtGui.QPushButton(parent=frame_def)
        self.btn_set_def.setText('Set Defaults')
        self.btn_set_def.connect(self.btn_set_def, QtCore.SIGNAL('clicked()'), self.set_default)
        self.btn_set_def.setDisabled(True)

        frame_def_layout.addRow(lbl_method1, self.txt_method1)
        frame_def_layout.addRow(lbl_method2, self.txt_method2)
        frame_def_layout.addRow(self.btn_set_def, None)

        self.hplc_table = QtGui.QTableWidget(self)
        header = ['Pos.', 'Name', 'ID', 'Inj. Volume', 'Method', 'Report?']
        self.hplc_table.setColumnCount(len(header))
        self.hplc_table.setColumnWidth(0, 50) # Position
        self.hplc_table.setColumnWidth(1, 2*80) # Name
        self.hplc_table.setColumnWidth(2, 1*80) # Short Name
        self.hplc_table.setColumnWidth(3, 120) # Volume
        self.hplc_table.setColumnWidth(4, 120) # Method
        self.hplc_table.setColumnWidth(5, 80) # Report?
        self.hplc_table.setHorizontalHeaderLabels(header)

        self.layout.addWidget(self.btn_lookup_plate)
        self.layout.addWidget(frame)
        self.layout.addWidget(frame_def)
        self.layout.addWidget(self.hplc_table)
        self.layout.addWidget(self.btn_gen_batch)

        self.setLayout(self.layout)

    def set_default(self):
        m1 = self.txt_method1.text()
        m2 = self.txt_method2.text()

        for idx, s in enumerate(self.samples):
            m = m1 if idx % 2 == 0 else m2
            self.hplc_table.item(idx, 4).setText(m)

    def lookup_plate(self):
        cf = ContainerFinder(self, self.app_state)
        cf.exec_()
        self.selected_plate = cf.selected_entry
        if self.selected_plate is None:
            return
        self.txt_cont_uid.setText(self.selected_plate['uid'])
        self.txt_cont_name.setText(self.selected_plate['name'])
        self.txt_cont_barcode.setText(self.selected_plate['barcode'])
        self.btn_set_def.setDisabled(False)
        self.btn_gen_batch.setDisabled(False)
        self.fill_hplc_table()

    def fill_hplc_table(self):
        self.cont_info = sample_db.get_container_type_by_id(self.selected_plate['kind'])

        self.samples = sorted(self.selected_plate['content'], key=lambda x: (x['position']['y'],x['position']['x']))

        # fill sample information at table
        self.hplc_table.setRowCount(0)
        self.hplc_table.setRowCount(len(self.samples))

        for idx, s in enumerate(self.samples):
            col, row = s['position']['x'], s['position']['y']
            col_text = chr(ord('@') + col + 1) if self.cont_info["cols_letters"] else col + 1
            row_text = chr(ord('@') + row + 1) if self.cont_info["rows_letters"] else row + 1

            pos_item = QtGui.QTableWidgetItem('{}{}'.format(row_text, col_text))
            pos_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.hplc_table.setItem(idx, 0, pos_item)
            self.hplc_table.setItem(idx, 1, QtGui.QTableWidgetItem(s['name']))
            self.hplc_table.setItem(idx, 2, QtGui.QTableWidgetItem(s['short_name']))
            self.hplc_table.setItem(idx, 3, QtGui.QTableWidgetItem(str(s['volume'])))
            self.hplc_table.setItem(idx, 4, QtGui.QTableWidgetItem(''))
            self.hplc_table.setItem(idx, 5, QtGui.QTableWidgetItem('1'))


            for i in range(0,3):
                self.hplc_table.item(idx, i).setFlags(QtCore.Qt.ItemIsSelectable)

    def validate_hplc_table(self):
        error = False
        text = 'Error validating data collection information'
        title = 'Error'

        for idx, s in enumerate(self.samples):
            vol = self.hplc_table.item(idx, 3).text()
            method = self.hplc_table.item(idx, 4).text()
            report = self.hplc_table.item(idx, 5).text()

            detail = 'Error at line {}: '.format(idx)
            try:
                vol = float(vol)
                if vol == '':
                    detail += '\n- Inj. Volume is required.'
                    error = True
                elif vol < 0:
                    detail += '\n- Inj. Volume needs to be greater than 0.'
                    error = True
                elif vol > float(s['volume']):
                    detail += '\n- Inj. Volume cannot be greater than sample volume ({}).'.format(float(s['volume']))
                    error = True
                if method == '':
                    detail += '\n- Method name is required.'
                    error = True
                if report not in ('0', '1'):
                    detail += '\n- Report? field must be either 0 or 1.'
                    error = True
            except ValueError as ve:
                detail += '\n- Inj. Volume needs to be a float value.'
                error = True
            except Exception as e:
                detail += '\n- Unknown error.\n'+str(e)
                error = True

            if error:
                utils.show_error(text, detail, title)
                return False

        return True

    def gen_batch(self):
        if not self.validate_hplc_table():
            return
        self.create_request()
        fname = self.compose_file()
        utils.show_information('Batch file created.',
         'Now copy the file located at: {} to the HPLC computer and execute the batch.'.format(fname),
         'Success')

    def create_request(self):
        data = []

        for idx, s in enumerate(self.samples):
            vol = self.hplc_table.item(idx, 3).text()
            method = self.hplc_table.item(idx, 4).text()
            report = self.hplc_table.item(idx, 5).text()
            data.append({'sample': s['uid'], 'volume': vol, 'method': method,
                         'report': report})

        payload = dict(
            sample = '',
            container = self.selected_plate['uid'],
            container_barcode = self.selected_plate['barcode'],
            collection_type = 'hplc',
            data = data)

        payload.update(self.app_state.get_default_fields())

        req_uid = request_db.upsert_request(payload)

    def compose_file(self):
        t = time.time()
        plate = self.selected_plate
        samples = self.samples
        cont_info = self.cont_info

        batch_path = 'C:\Batch'
        fname = '{}_{}.txt'.format(time.strftime("%Y%m%d_%H_%M_%S", time.gmtime(t)),
                                    plate['name'])
        prefix = 'TBD'
        sep = '\r\n'
        with open(fname, 'w') as f:
            f.write(''+sep)
            f.write('[Header]'+sep)
            f.write('Batch File Name\t{}\{}'.format(batch_path, fname)+sep)
            f.write('Output Date\t{}'.format(time.strftime("%m/%d/%Y", time.gmtime(t)))+sep)
            f.write('Output Time\t{}'.format(time.strftime("%r", time.gmtime(t)))+sep)
            f.write(''+sep)
            f.write('[File Information]'+sep)
            f.write('Type\tBatch File'+sep)
            f.write('Generated\t{}'.format(time.strftime("%m/%d/%Y %r", time.gmtime(t)))+sep)
            f.write('Generated by\tSystem Administrator'+sep)
            f.write('Modified\t{}'.format(time.strftime("%m/%d/%Y", time.gmtime(t)))+sep)
            f.write('Modified by\tSystem Administrator'+sep)
            f.write(''+sep)
            f.write('[File Description]'+sep)
            f.write(''+sep)
            f.write(''+sep)
            f.write('[Instrument Type]'+sep)
            f.write('Type\t0'+sep)
            f.write(''+sep)
            f.write('[Start Row]'+sep)
            f.write('Mode\t0'+sep)
            f.write('# of Row\t1'+sep)
            f.write('End Mode\t0'+sep)
            f.write('End to #\t1'+sep)
            f.write('Repeat batch run\t0'+sep)
            f.write('Succeed Mode\t0'+sep)
            f.write(''+sep)
            f.write('[Bracket]'+sep)
            f.write('Mode\t0'+sep)
            f.write(''+sep)
            f.write('[Data Filename]'+sep)
            f.write('Mode\t1'+sep)
            f.write('Prefix\t{}'.format(prefix)+sep)
            f.write('Items\t1.7'+sep)
            f.write('Auto-Increment\t3'+sep)
            f.write(''+sep)
            f.write('[Startup]'+sep)
            f.write('Mode\t0'+sep)
            f.write('Prompt Date Time\t1'+sep)
            f.write('Date Time\t1601/01/01 00:00:00'+sep)
            f.write('Use Method File\t0'+sep)
            f.write('File\t'+sep)
            f.write('Warm Up Time\t5'+sep)
            f.write(''+sep)
            f.write('[Shutdown]'+sep)
            f.write('Mode\t0'+sep)
            f.write('Use Method File\t0'+sep)
            f.write('File\t'+sep)
            f.write('Cool Down Time\t0'+sep)
            f.write('ELSD Valve\t0'+sep)
            f.write('MS Settings\t32703'+sep)
            f.write('MS Settings2\t2'+sep)
            f.write(''+sep)
            f.write('[ASCII Convert]'+sep)
            f.write('Mode\t0'+sep)
            f.write('File\tASCIIData.txt'+sep)
            f.write('Auto-Increment\t0'+sep)
            f.write('Items\t1.2.3'+sep)
            f.write('Delimiter\t"\t"'+sep)
            f.write(''+sep)
            f.write('[File Convert]'+sep)
            f.write('Mode\t0'+sep)
            f.write('Auto-Increment\t0'+sep)
            f.write(''+sep)
            f.write('[QA/QC]'+sep)
            f.write('Mode\t0'+sep)
            f.write('File\tQAQCData.txt'+sep)
            f.write('Auto-Increment\t1'+sep)
            f.write('HTML File\t0'+sep)
            f.write('CSV File\t0'+sep)
            f.write(''+sep)
            f.write('[Folder]'+sep)
            f.write('Mode\t0'+sep)
            f.write('Data Folder\t'+sep)
            f.write('Method Folder\t'+sep)
            f.write('Report Folder\t'+sep)
            f.write(''+sep)
            f.write('[Option Items]'+sep)
            f.write('Option1\t'+sep)
            f.write('Option2\t'+sep)
            f.write('Option3\t'+sep)
            f.write('Option4\t'+sep)
            f.write('Option5\t'+sep)
            f.write('Option6\t'+sep)
            f.write('Option7\t'+sep)
            f.write('Option8\t'+sep)
            f.write('Option9\t'+sep)
            f.write('Option10\t'+sep)
            f.write(''+sep)
            f.write('[Extended Column ProgID]'+sep)
            f.write('LSSBatchAddInConc\t'+sep)
            f.write(''+sep)
            f.write('[Batch Table]'+sep)
            f.write('# of Row\t{}'.format(len(samples))+sep)

            f.write('Run Mode\tTray Name\tVial#\tSample Name\tSample ID\tSample Type\tAnalysis Type\tMethod File\tData File\tBackground\tBackground Data File\tLevel#\tInj. Volume\tISTD Amt.\tSample Amt.\tDil. Factor\tystem Check\tReport Output\tReport Format File\tUser Prog.\tAction\tData Comment\tAutoPurge\tBaseline Check\tOption 1\tOption 2\tOption 3\tOption 4\tOption 5\tCustom Parameters\tAuto Tuning\tTuning File\tPsiPort Instrument Method File\tSummary Type\tSummary Report Format File\tOption 6\tOption 7\tOption 8\tOption 9\tOption 10\tSystem Suitability\tMulti Injection\tBarcode\tSampler File\tConc. Overrides'+sep)

            for idx, s in enumerate(samples):
                col, row = s['position']['x'], s['position']['y']
                col_text = chr(ord('@') + col + 1) if cont_info["cols_letters"] else col + 1
                row_text = chr(ord('@') + row + 1) if cont_info["rows_letters"] else row + 1
                inj_vol = float(self.hplc_table.item(idx, 3).text())

                run_mode = 'DL AQ DP'
                tray_name = 1
                sample_type = '0:Unknown'
                analysis_type = ''
                method_file = '{}.lcm'.format(self.hplc_table.item(idx, 4).text())
                data_file = ''
                background = 0
                background_data_file = ''
                level_num = ''
                istd_amt = '(Level1 Conc.)'
                sample_amt = 1
                dil_factor = 1
                system_check = ''
                report_out = int(self.hplc_table.item(idx, 5).text())
                report_format_file = 'DEFAULT.lsr'
                user_prog = ''
                action = ''
                data_comment = ''
                auto_purge = 0
                baseline_check = 0
                option1 = ''
                option2 = ''
                option3 = ''
                option4 = ''
                option5 = ''
                custom_params = ''
                auto_tuning = 0
                tuning_file = ''
                psiport = ''
                summary_type = ''
                summary_format_file = ''
                option6 = ''
                option7 = ''
                option8 = ''
                option9 = ''
                option10 = ''
                system_suit = 0
                multi_injection = 1
                barcode = ''
                sampler_file = ''
                conc_overrides = ''

                line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'+sep
                f.write(
                    line.format(
                        run_mode, tray_name, '{}{}'.format(row_text, col_text),
                        s['name'], s['short_name'], sample_type, analysis_type,
                        method_file, data_file, background, background_data_file,
                        level_num, inj_vol, istd_amt, sample_amt, dil_factor,
                        system_check, report_out, report_format_file, user_prog,
                        action, data_comment, auto_purge, baseline_check, option1,
                        option2, option3, option4, option5, custom_params, auto_tuning,
                        tuning_file, psiport, summary_type, summary_format_file,
                        option6, option7, option8, option9, option10, system_suit,
                        multi_injection, barcode, sampler_file, conc_overrides
                    )
                )
        return fname
