from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime

class Nota(Base):
    __tablename__ = 'nota'

    id_nota = Column(Integer, autoincrement=True, primaty_key=True)
    nome_nota = Column(String, nullable=False)
    data_nota = Column(DateTime)
    texto_nota = Column(String, nullable=False)

    def __repr__(self):
        return  f'Título da Nota: {self.nome_nota}, Id: {self.id_nota}'