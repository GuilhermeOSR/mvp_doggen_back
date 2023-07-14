from sqlalchemy import Column, String, Integer, DateTime, Date
from datetime import datetime, date
from typing import Union

from model import Base

class Cachorro(Base):
    __tablename__ = 'cachorro'

    id = Column("pk_cachorro", Integer, primary_key=True)
    nome = Column(String(140), unique=False)
    raca = Column(String(30), unique=False)
    idade = Column(Date)
    tutor = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, raca:str, tutor:str, idade:date,data_insercao:Union[DateTime, None] = None):
        """
        Cria um Cachorro

        Arguments:
            nome: nome do cachorro.
            raca: raça do cachorro.
            idade: idade do cachorro
            data_insercao: data de quando o cachorro foi inserido à base
        """
        self.nome = nome
        self.raca = raca
        self.idade = idade
        self.tutor = tutor

        #Caso não seja informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
