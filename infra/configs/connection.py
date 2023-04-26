from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = 'mysql+pymysql://root:Senac2021@localhost:3306/notas'
        self.__engine = self.__create_data_base_engine()
        self.session = None
        self.__create_database()

    def create_database(self):
        engine = create_engine(self.__connection_string, echo=True)
        try:
            engine.connect()
        except Exception as e:
            if '1049' in str(e):
                engine = create_engine(self.__connection_string.rsplit("/", 1)[0], echo=True)
                conn = engine.connect()
                conn.execute(f'CREATE DATABASE IF NOT EXISTS {(self.__connection_string.rsplit("/", 1)[1])}')
                conn.close()
                print('Banco Criado!')
            else:
                raise e

    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine