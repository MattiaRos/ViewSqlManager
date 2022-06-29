import os
import pyodbc
from settings import Settings
from datetime import datetime
from replacer import Replacer

class ViewSqlManager:
    def __init__(self, s: Settings, r: Replacer) :
        self.setup = s
        self.replacer = r

    def split_statements_go(self, raw: str):
        statements = []
        sql = ''
        for line in raw.splitlines():
            if line.strip().upper() == 'GO':
                statements.append(sql)
                sql = ''
            else:
                sql += line + '\r\n'
        if not sql.isspace():
            statements.append(sql)
        return statements

    #########################################################################
    #List all the existing sql file
    
    def get_list_sql_file(self):
        self.entry = list()
        for x in os.listdir(self.setup.sql_path):
            self.entry.append(x)
        return self.entry

    #########################################################################
    #Logic to sql script execution

    def execute_script(self, env_id, sql_file_name):

        sql_full_path = os.path.join(self.setup.sql_path, sql_file_name)

        #error check
        x = self.setup.envs[env_id] if env_id in self.setup.envs else None
        if x is None: 
            raise Exception('Env not found')
            #return sql_full_path
        #connection to db by config.ini file
        conn_string = x.conn_
        cnxn = pyodbc.connect(conn_string)
        cursor = cnxn.cursor()
        with open(sql_full_path, mode="r", encoding="utf-8") as f:
            query = f.read()
        
        sql = self.replacer.replace(env_id, query)

        #Execution of sql code
        statements_count = 0
        #for s in sql.split('GO'):
        if self.setup.debug is False:
            for s in self.split_statements_go(sql):
                try:
                    cursor.execute(s)
                    statements_count += 1
                except pyodbc.Error as e:
                    message = str(e)
                    cnxn.rollback()
                    cursor.close()
                    cnxn.close()
                    self._execute_log(sql_file_name, False, message)
                    raise Exception(message)
            cnxn.commit()
            cursor.close()
            cnxn.close()
        else:
            with open('debug.txt', 'a') as s:
                 s.write(sql)
            

        

        self._execute_log(sql_file_name, True, f'DONE {statements_count} scripts')

        return True, statements_count

    #########################################################################
    #Logic to print in log.txt the results of the sql view execution

    def _execute_log(self, sql_view_path, success, message):

        date = datetime.now().strftime("%Y_%m_%d-%H:%M:%S")
        k = '+' if success is True else '-'
        sql_file = os.path.basename(sql_view_path)
        
        with open('log.txt', 'a') as s:
            s.write(f'[{k}] {sql_file} [{date}] {message}\n\n')
