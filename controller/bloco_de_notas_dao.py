import sqlite3

from model.bloco_de_notas import Bloco_De_Notas


class DataBase:
    def __init__(self, nome='notas.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_bloco_de_notas(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS BLOCO_DE_NOTAS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME_NOTA TEXT,
            DATA_NOTA TEXT,
            TEXTO_NOTA TEXT
            );
            """)
        self.close_connection()

    def criar_nota(self, bloco = Bloco_De_Notas):
        self.connect()
        cursor = self.connection.cursor()
        campos_bloco = ('NOME_NOTA', 'DATA_NOTA', 'TEXTO_NOTA')

        valores_bloco = f" '{bloco.nome_nota}', '{bloco.data_nota}', " \
                  f" '{bloco.texto_nota}' "

        try:
            cursor.execute(f""" INSERT INTO BLOCO_DE_NOTAS {campos_bloco} VALUES ({valores_bloco})""")
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def ler_nota(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT * FROM BLOCO_DE_NOTAS WHERE ID = '{int(id)}' """)
            return cursor.fetchone()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()

    def editar_nota(self, nota = Bloco_De_Notas):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" UPDATE BLOCO_DE_NOTAS SET
                 NOME_NOTA = '{nota.nome_nota}',
                 DATA_NOTA = '{nota.data_nota}',
                 TEXTO_NOTA = '{nota.texto_nota}' 
                 WHERE ID = {nota.id} """)
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def excluir_nota(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" DELETE FROM BLOCO_DE_NOTAS WHERE ID = '{id}' """)
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def consulta_todas_notas(self):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT * FROM BLOCO_DE_NOTAS""")
            clientes = cursor.fetchall()
            return clientes
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()