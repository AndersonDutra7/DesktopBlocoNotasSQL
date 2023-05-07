from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime

class Nota(Base):
    # Nome da tabela criada
    __tablename__ = 'nota'

    # Colunas da tabela que serão criadas na tabela
    id_nota = Column(Integer, autoincrement=True, primary_key=True)
    nome_nota = Column(String(length=100), nullable=False)
    data_nota = Column(DateTime)
    texto_nota = Column(String(length=100), nullable=False)

    def __repr__(self):
        return  f'Título da Nota: {self.nome_nota}, Id: {self.id_nota}'