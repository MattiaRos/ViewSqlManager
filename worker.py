from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
from settings import Settings
from viewSqlManager import ViewSqlManager
from replacer import Replacer
from gitUpdateManager import GitUpdateManager

#generate the logic and transform it in qt language
class Worker(QObject):

    sig_send_list_sql_file_and_env=pyqtSignal(list, dict)
    sig_send_log_txt = pyqtSignal(bool, str, str)
    sig_finished= pyqtSignal()
    sig_git_status= pyqtSignal(bool)

    
    @pyqtSlot()
    def myinit(self):
        
        sys.stdout.flush()
        settings = Settings('config.ini')
        r = Replacer(settings, 'replace.ini')

        self.manager = ViewSqlManager(settings, r)
        self.file_list = self.manager.get_list_sql_file()
        d_env_name=settings.simple_env_dict()
        #Send settings to populate graphic
        self.sig_send_list_sql_file_and_env.emit(self.file_list, d_env_name)

        git_manager = GitUpdateManager()

        if git_manager.need_update() is True:            
            git_manager.updater()
            self.sig_git_status.emit(True)
        else:
            self.sig_git_status.emit(False)
        

        # git manager.check
        # emette un bool sempre 

    ##########################################################################
    #Execute single or multiple view based on mode selection in graphic.py
    @pyqtSlot(bool, int, str)
    def slot_execute_view(self, single_view, env_id, sql_file_name):

        if single_view is True:
            self.run( env_id, sql_file_name)
        else :
            for i in self.file_list:
                self.run(env_id, i)
        #emit finished
        self.sig_finished.emit()

    ##########################################################################
    #Execute view and graphic result logic

    def run(self, env_id, sql_file_name):
        try:
            success, statements_count = self.manager.execute_script(env_id, sql_file_name)
            self.sig_send_log_txt.emit(success, f'{sql_file_name} [{statements_count}]', None)
        except Exception as e:
            self.sig_send_log_txt.emit(False, sql_file_name, str(e))