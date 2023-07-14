from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Cachorro
from schemas import *
from flask_cors import CORS
from flask import jsonify


info = Info(title="DogGen", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo Tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cachorro_tag = Tag(name="Cachorro", description="Adição, visualização e remoção de cachorros à base")
listar_cachorro = Tag(name="Listar", description="Listagem de cachorros da base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo da documentação."""
    return redirect('/openapi')


@app.post('/cachorro', tags=[cachorro_tag], 
            responses={"200": CachorroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cachorro(form: CachorroSchema):
    """Adiciona um novo Cachorro à base de dados
    Retorna uma representação dos cachorros.
    """
    cachorro = Cachorro(
        nome=form.nome,
        raca=form.raca,
        idade=form.idade,
        tutor=form.tutor
        )
    try:
        #Cria conexão com a base.
        session = Session()
        #Adicionando Cachorro.
        session.add(cachorro)
        #Efetivando o comando de adição de novo item na tabela.
        session.commit()
        return apresenta_cachorro(cachorro), 200
    except IntegrityError as e:
        #Caso tenha dois tutores com nomes iguais.
        error_msg = "Tutor de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 400
    except Exception as e:
        #Caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo cachorro :/"
        return {"message": error_msg}, 400
@app.get('/cachorros', tags=[listar_cachorro],
         responses={"200": ListagemCachorrosSchema, "404": ErrorSchema, "400": ErrorSchema})
def get_cachorros():
    """Faz a busca por todos os Cachorros cadastrados."""
    session = Session()
    cachorros = session.query(Cachorro).all()

    if not cachorros:
        return {"cachorros": []}, 200
    else:
        print(cachorros)
        return apresenta_cachorros(cachorros), 200
    

@app.get('/cachorro', tags=[cachorro_tag],
        responses={"200": CachorroViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def get_cachorro(query: CachorroBuscaSchema):
    """Faz a busca por todos os cachorros com um nome especifico."""
    cachorro_nome = query.nome
    session = Session()
    cachorros = session.query(Cachorro).filter(Cachorro.nome == cachorro_nome).all()

    if not cachorros:
        error_msg = "Cachorro não encontrado"
        return {"message": error_msg}, 404
    else:
        cachorros_repr = [apresenta_cachorro(cachorro) for cachorro in cachorros]
        return jsonify({"cachorros": cachorros_repr}), 200
    
@app.delete('/cachorro', tags=[cachorro_tag],
        responses={"200": CachorroDelSchema, "404": ErrorSchema})
def del_cachorro(query: CachorroBuscaSchema):
    """Faz a remoção de um cachorro."""
    cachorro_nome = unquote(unquote(query.nome))
    print(cachorro_nome)
    session = Session()
    count = session.query(Cachorro).filter(Cachorro.nome == cachorro_nome).delete()
    session.commit()

    if count:
        return {"message": "Cachorro removido", "id":  cachorro_nome}
    else:
        error_msg = "Cachorro não encontrado"
        return {"message": error_msg}, 404