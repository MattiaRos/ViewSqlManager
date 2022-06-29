from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys 
from graphic import Window
from worker import Worker

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    thread = QThread()
    # Step 1: Create a worker object
    worker = Worker()
    # Step 2: Move worker to the thread
    worker.sig_send_list_sql_file_and_env.connect(window.slot_receive_list_sql_file_and_env)
    worker.sig_send_log_txt.connect(window.slot_receive_log_txt)
    window.sig_execute_view.connect(worker.slot_execute_view)
    worker.sig_finished.connect(window.slot_finished)
    worker.moveToThread(thread)
    # Step 3: Connect signals and slots
    thread.started.connect(worker.myinit)
    # Step 4: Start the thread
    thread.start()
    worker.sig_git_status.connect(window.slot_git_status)
    
    window.show()
    sys.exit(app.exec()) 