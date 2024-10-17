import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('carros') # ferramentas do python,
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # havera modificacoes no nosso banco
 # permiti a conexao com o banco de dados e modificacoes
# Por padrao, em aplicacaoes em Producao, isso ficaFalse.

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'
# banco que estamos mexendo, usuario, a senha %40 substitui o @ e o IP, ai colocamos @localhost e o nome do seu banco de dados

mybd = SQLAlchemy(app) # faz a conexcao com o banco de dados

# Definimos a estrutura da tabela tb_carros
class Carros(mybd.Model): # Cumunicacao com o banco de dados
    __tablename__ = 'tb_carro'
    id = mybd.Column(mybd.Integer, primary_key = True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))

    def to_json(self): # cumunicacao com a API
        return{"id":self.id, "marca":self.marca, "modelo":self.modelo, "modelo":self.modelo, "valor":self.valor, "cor":self.cor, "numero_vendas":self.numero_vendas, "ano":self.ano}
           
           
#**********API***********
# Selecionar tudo (GET)

@app.route("/carros", methods=["GET"])# VISUALIZAR DADOS, POST(CRIACAO), DELETE(EXCLUSAO)
def selecionar_carros():
    carro_objetos = Carros.query.all() # puxe todos os registros da tabela carros query.all(lista de objetos)

    carro_json = [carro.to_json() for carro in carro_objetos] # Converte em um dicionario no formato json

    return gera_response(200, "carros", carro_json)# gra resposta http 




# Selecionar Individual (Por ID)
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json = carro_objetos.to_json()

    return gera_response(200, "carros", carro_json)

# Cadastrar

@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo=body["modelo"], valor=body["valor"], cor=body["cor"], numero_vendas=body["numero_vendas"], ano=body["ano"])

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso !!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "carros", {}, f"Erro ao cadastrar !! {e}")

# Atualizar
# @app.route("/carros/<id>", methods=["PUT"])
# def atualizar_carro(id): 
#     carro_objetos = Carros.query.filter_by(id=id).first()
#     body = request.get_json() # Corpo da requisicao

#     try:
#         if ('marca' in body):
#             carro_objetos.marca = body['marca']






            
def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run(port=5000,host='localhost',debug=True) # debug significa teste