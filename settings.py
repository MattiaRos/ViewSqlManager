import configparser

class Setting_env:
    def __init__(self, id_,  name, conn) -> None:
        self.id_ = id_
        self.name_ = name
        self.conn_ = conn

    def __repr__(self) -> str:
        return f'{self.id_= } {self.name_= } {self.conn_= }'

class Settings:
    def __init__(self, path_ini: str) -> None:
        self.path_ini = path_ini
        self.debug = False
        self.num_env = 0
        self.sql_path = ''
        self.envs = dict()
        config = configparser.ConfigParser()
        config.read(self.path_ini)

        self.debug = bool(config['main']['debug'])

        self.num_env = int(config['main']['num_env'])

        self.sql_path = config['main']['sql_path']

        for i in range(self.num_env):
            group = f'env_{i}'

            name = config[group]['name']
            conn = config[group]['conn_string']
            se = Setting_env (i, name, conn)
            self.envs [i]=se

    def simple_env_dict(self) -> dict:
        #Serve per il dizionario per la grafica
        return {key:value.name_ for (key,value) in self.envs.items()}
        #example= dict()
        #for key in self.envs:
        #    example [key]= self.envs[key].name_
        #dict_variable = {key:self.envs[key].name_ for key in self.envs}