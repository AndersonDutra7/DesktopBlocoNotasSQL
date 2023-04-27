from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota

class NotasRepository:

    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    def insert(self, nome_nota, data_nota, texto_nota):
        with DBConnectionHandler() as db:
            data_insert = Nota(nome_nota = nome_nota, data_nota = data_nota, texto_nota = texto_nota)
            db.session.add(data_insert)
            db.session.commit()

    def delete(self):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id_nota == id).delete()
            db.session.commit()

    def update(self, id_nota, nome_nota, data_nota, texto_nota):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id_nota == id).update({nome_nota : nome_nota}, {texto_nota : texto_nota})
            db.session.commit()

