from pydantic import BaseModel
from typing import List
from model.cachorro import Cachorro
from datetime import date

class CachorroSchema(BaseModel):
    """ Define como um novo cachorro a ser inserido deve ser representado.
    """
    nome: str = "Thor"
    raca: str = "Husky"
    idade: date = date(2016, 11, 16)
    tutor: str = "Caroline"

class CachorroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será 
        feita apenas com base no nome do cachorro.
    """
    nome: str = "Thor"

class ListagemCachorrosSchema(BaseModel):
    """ Define como uma listagem de cachorros será retornada.
    """
    cachorros:List[CachorroSchema]

def apresenta_cachorros(cachorros: List[Cachorro]):
    """ Retorna uma representação do cachorro seguindo o schema definido em 
        CachorroViewSchema.
    """
    result = []
    for cachorro in cachorros:
        result.append({
            "nome": cachorro.nome,
            "raca": cachorro.raca,
            "idade": cachorro.idade,
            "tutor": cachorro.tutor,
        })
        
    return {"cachorros": result}

class CachorroViewSchema(BaseModel):
    """ Define como um cachorro será retornado: cachorro.
    """
    id: int = 1
    nome: str = "Thor"
    raca: str = "Husky"
    idade: date = date(2016, 11, 16)
    tutor: str = "Caroline"

class CachorroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    message: str
    nome: str

def apresenta_cachorro(cachorro: Cachorro):
    """Retorna uma apresentação do produto seguindo o schema definido em 
    CachorroViewSchema.
    """
    return {
        "id": cachorro.id,
        "nome": cachorro.nome,
        "raca": cachorro.raca,
        "idade": cachorro.idade,
        "tutor": cachorro.tutor,
    }

