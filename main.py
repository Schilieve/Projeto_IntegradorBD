
#imports para trabalhar com o json
import json 
#Flask é um aferramenta 
from flask  import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

#Aplicação do tipo flask 
app = Flask('carros')
#Havera modificações 


# Por padrao em  aplicações de produção o valor fica em False.
app.config['SQLALCHEMY_TRACK_MODIFICAION'] = True 



# A Configuração da rota da nossa base de dados 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'
# Na senha sempre que tiver @ colocar %40 para tornar o caracter legivel 

#-->  1 o nome do banco
#-->  2 o usuario
#-->  3 a senha 
#-->  4 o projeto 

# variavel que vai representar o banco 

mybd= SQLAlchemy(app)


# Definimos a estruturada nossa primeira tabela
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id = mybd.Column(mybd.Integer, primary_key = True)
    marca = mybd.Column(mybd.String(100)) 
    modelo = mybd.Column(mybd.String(100))
    valor  = mybd.Column(mybd.Float)
    cor  = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))

# Depois Convertemos a tabela em Json 
    def to_json(self):
        return {
        "id":self.id,
        "marca":self.marca,
        "modelo":self.modelo,
        "valor":self.valor,
        "cor":self.cor,
        "numero_vendas":self.numero_vendas,
        "ano":self.ano
                }


#***************** API *********************

#Selecionar Tudo (GET)
@app.route("/carros", methods=["GET"])
def selecionar_carros():
    #Executa um aocnsulta no banco de dados para obter todos os registros da tabela carros 
    # o metodo query.all retorna uma lista de objetos 'carros'
    carro_objetos = Carros.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200,"caros", carro_json)

#Selecionar por id individual 

@app.route("/carros/<id>", methods =["GET"])

def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json= carro_objetos.to_json()
    return gera_response(200,"carros",carro_json)



#Cadastrar 

@app.route("/carros", methods = ["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo=body["modelo"], valor= body["valor"], cor=body["cor"],numero_vendas=body["numero_vendas"],ano=body["ano"])
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201,"carros",carro.to_json(), "Criado com Sucesso!!!")
    
    except Exception as e:
        print('Erro!!',e)

        return gera_response(400,"carros",{},"Erro ao Cadastrar!!")
    


# Atualizar 

@app.route("/carros/<id>",  methods = ["PUT"])
def atualizar_carro(id):
    #Consulta por id
    carro_objetos = Carros.query.filter_by(id=id).first()
    #Corpo da requisicao
    body= request.get_json()

    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('modelo' in body):
            carro_objetos.cor = body['cor']
        if('valor' in body):
            carro_objetos.modelo = body['modelo']
        if('cor' in body):
            carro_objetos.valor = body['valor']
        if('numero_vendas' in body):
            carro_objetos.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objetos.ano = body['ano']

        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, 'carros', carro_objetos.to_json(),'Atualizado com sucesso!!!')
    

    except Exception as e:
        print('Erro',e)
        return gera_response(400,{},'Erro ao atualizar!!')





# Delete

@app.route("/carros/<id>", methods=['DELETE'])
def deletar(id):
    carro_objetos = Carros.query.filter_by(id=id).first()

    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()

        return gera_response(200, 'carros', carro_objetos.to_json(),'Deletado com sucesso' )
    except Exception as e:
        print('Erro',e)
        return gera_response(400,"carro",{}, "Erro ao deletar")
    




def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo 

    if(mensagem):
        body["mensagem"] = mensagem
    
    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run(port=5000, host='localhost',debug=True)