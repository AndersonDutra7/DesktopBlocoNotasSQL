from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota
import traceback


class NotasRepository:

    # Método para realizar a consulta de todas as notas
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    # Método para inserir nota no banco de dados
    def insert(self, nota):
        with DBConnectionHandler() as db:
            try:
                db.session.add(nota)
                db.session.commit()
                return 'Ok'
            except Exception as e:
                db.session.rollback()
                traceback.print_exc()  # Imprimir detalhes da exceção
                return str(e)  # Retornar mensagem de erro como string


    # Método para realizar a consulta das notas por id
    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).filter(Nota.id_nota == id).first()
            return data

    # Mètodo para realizar a remoção de uma nota do banco de dados
    def delete(self, nota):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Nota).filter(Nota.id_nota == nota).delete()
                db.session.commit()
                return "Ok"
            except Exception as e:
                db.session.rollback()
                return e

    # Método para atualizar uma nota
    def update(self, id, nome, texto):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Nota).filter(Nota.id_nota == id).update({Nota.nome_nota: nome, Nota.texto_nota: texto})
                db.session.commit()
                return "Ok"
            except Exception as e:
                db.session.rollback()
                return e
