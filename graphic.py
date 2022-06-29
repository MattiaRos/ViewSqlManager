from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from datetime import datetime
import sys 

class Window(QMainWindow):

    sig_execute_view = pyqtSignal(bool, int, str)

    ##################################################################
    #Graphic template creation

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL View Deployer")
        self.setGeometry(500,200, 500,400)

        ##############################################################
        # Right upper grid

        #Set the environment selector module
        self.l_env_box = QVBoxLayout()
        self.w_env_box= QGroupBox('Environment')
        self.w_env_box.setLayout(self.l_env_box)
        
        self.env_group = QButtonGroup()
        #Fill l_env_box and env_group in slot_receive_list_sql_file_and_env 

        #Set the selection mode module 
        l_type_box = QVBoxLayout()
        self.w_type_box= QGroupBox('Mode')
        self.w_type_box.setLayout(l_type_box)

        self.rad_single_sql_file = QRadioButton("Single view")
        self.rad_single_sql_file.setChecked(True)
        l_type_box.addWidget(self.rad_single_sql_file) 
        self.rad_all_sql_file = QRadioButton("All view")
        l_type_box.addWidget(self.rad_all_sql_file)

        #Set the submit module
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setGeometry(QRect(140, 30, 100, 100))
        self.btn_submit.setObjectName("Submit")
        self.btn_submit.clicked.connect(self.on_submit_button_clicked)

        #Make the widget to collect the modules
        btn_grid =  QGridLayout()
        w_controller = QWidget()
        w_controller.setLayout(btn_grid)
        
        #Add the previous 3 modules to a Widget
        btn_grid.addWidget(self.w_env_box, 0, 0,)
        btn_grid.addWidget(self.w_type_box, 1, 0)
        btn_grid.addWidget(self.btn_submit, 0, 1, 2, 1)

        ##############################################################
        # Left upper box

        self.w_list_sql_file = QListView()
        self.w_list_sql_file.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sql_file_model= QStringListModel()
        self.w_list_sql_file.setModel(self.sql_file_model)

        ##############################################################
        # Bottom log

        self.w_log = QPlainTextEdit()

        ###############################################################
        # Grid organization

        full_grid = QGridLayout()

        full_grid.addWidget(self.w_list_sql_file, 0, 0)
        full_grid.addWidget(w_controller, 0, 1)
        full_grid.addWidget(self.w_log, 1, 0, 1, 2)
        
        #self.setLayout(full_grid)
        self.w_=QWidget()
        self.w_.setEnabled(False)
        self.w_.setLayout(full_grid)
        self.setCentralWidget(self.w_)

    ##################################################################
    #Populate left upper box and reight upper box(environment selection)
    @pyqtSlot(list, dict)
    def slot_receive_list_sql_file_and_env(self, ll, d_env_name):
        self.sql_file_model.setStringList(ll)
        
        c = 0
        for k, v in d_env_name.items():
            rad = QRadioButton(v)
            self.l_env_box.addWidget(rad)
            self.env_group.addButton(rad, k)
            c += 1
            if c==1:
                rad.setChecked(True)

    ##################################################################
    #Populate Bottom log
    @pyqtSlot(bool, str, str)
    def slot_receive_log_txt(self, success, sql_file, additional_message):
        if success is True:
            self.w_log.appendHtml(f"<span style=\"color:green;\" > {sql_file} </span>")
        else:
           self.w_log.appendHtml(f"<span style=\"color:red;\" > {sql_file} </span> <span style=\"color:black;\" > {additional_message} </span>") 

    ##################################################################
    #Read Gui for pushButton signal
    @pyqtSlot()
    def on_submit_button_clicked(self):
        
        env_id = self.env_group.checkedId()

        if self.rad_single_sql_file.isChecked() is True:
            idx = self.w_list_sql_file.selectedIndexes()

            if len(idx) == 1:
                sql_view = idx[0].data(Qt.ItemDataRole.DisplayRole)
                self.btn_submit.setEnabled(False)
                self.sig_execute_view.emit(True, env_id, sql_view)
        else:
            self.btn_submit.setEnabled(False)
            self.sig_execute_view.emit(False, env_id, None)

    #################################################################
    #Reactivate the submit button
    @pyqtSlot()
    def slot_finished(self):

        self.btn_submit.setEnabled(True)

    #################################################################
    #Update source file
    @pyqtSlot(bool)
    def slot_git_status(self, status):

        self.last_update=''

        if status is True:
            QMessageBox.information(self, 'Update', 'I file sorgente sono stati aggiornati, l\'applicazione verrà terminata.')
            QApplication.quit()
        else:
            self.last_update= str(datetime.now().strftime("%Y_%m_%d-%H:%M:%S"))
            self.statusBar().showMessage(f"Updated last time on : {self.last_update}")
            self.w_.setEnabled(True)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())