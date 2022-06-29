from itertools import count
from settings import Settings
import configparser
import re

class Replacer:

    def __init__(self, s:Settings, path_ini: str):
        self.path_ini = path_ini
        self.setup = s
        self.sql_path = self.setup.sql_path
        self.env_dict = dict()
        config= configparser.ConfigParser()
        config.read(self.path_ini)


        for i in range(self.setup.num_env):
            group = f'env_{i}'
            d = dict(config.items(group))
            self.env_dict [i] = d


    def replace(self, env_id, sql: str) -> str:
        
        d = self.env_dict[env_id] if env_id in self.env_dict else None
        if d is None:
            raise Exception('Env not found')
            return False
        
        reg = '\{\{(.*?)\}\}'
        l_key = list(set(re.findall(reg, sql)))

        for x in l_key:
            if x not in d:
                raise Exception('Key not found')
            value = d[x]
            sql = sql.replace(f'{{{{{x}}}}}', value)

        return sql
