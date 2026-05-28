from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from datetime import date, datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

api_users = Blueprint('users', __name__)


@api_users.route("/users", methods = ['POST'])
def cadastrar_usuario():
    # Dados da requisição
    data = request.json
    
    nome = data["nome"]
    #username = data["username"]
    email = data["email"]
    #cpf = data["cpf"]
    #dt_nasc = datetime.strptime(data["dt_nasc"], '%Y-%m-%d').date()
    password = data["password"]

    #Tratamento de dados inexistentes
    if not nome or not email or not password:
        return jsonify({'message': "Erro! Dados inexistentes!"}), 400
    
    #Tratamento de nome
    for caractere in nome:
        if caractere.isdigit():
            return jsonify({'message': 'Erro! Nome não pode conter dígitos!'}), 400

    #Tratamento de cpf
    #for caractere in cpf:
    #    if not caractere.isdigit():
    #        return jsonify({'message': 'Erro! CPF deve conter somente dígitos!'}), 400
        
    #if len(cpf) != 11:
    #    return jsonify({'message': 'Erro! CPF está incompleto'}), 400
    
    #Tratamento de data de nascimento
    #data_atual = date.today()
    #idade = data_atual.year - dt_nasc.year

    #if dt_nasc > data_atual or idade > 110:
    #    return jsonify({'message': 'Erro! Data inválida!'}), 400
    
    #Tratamento de senha
    if len(password) < 8:
        return jsonify({'message': 'Erro! Senha deve conter 8 dígitos ou mais!'}), 400
    
    
    elif len(password) > 255:
        return jsonify({'message': 'Erro! Senha deve conter 255 dígitos ou menos'}), 400

    #Tratamento de integridade
    #user_existente = User.query.filter_by(cpf = cpf).first()
    #if user_existente:
    #    return jsonify({'message': 'Erro! CPF já cadastrado'}), 400
     
    user_existente = User.query.filter_by(email = email).first()
    if user_existente:
        return jsonify({'message': 'Erro! Email já cadastrado'}), 400
    
    #user_existente = User.query.filter_by(username = username).first()
    #if user_existente:
    #    return jsonify({'message': 'Erro! Nome de usuário já cadastrado'}), 400

    new_user = User(nome = nome,
                    email = email,
                    #username = username,
                    #cpf = cpf,
                    #dt_nasc = dt_nasc,
                    password = generate_password_hash(password))
    
    #Último teste de integridade
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erro! Possível duplicação de dados! Verifique seu campo de email'}), 400
    
    return jsonify({
            'message': 'Novo usuário cadastrado com sucesso!',
            'id': new_user.id
        }), 201

@api_users.route("/users/me", methods = ["GET"])
@jwt_required()
def obter_usuario():
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    user_data = {
        "id": user.id,
        "nome": user.nome,
        #"username": user.username,
        "email": user.email
        #"cpf": user.cpf,
        #"dt_nasc": user.dt_nasc.isoformat(),
    }

    return jsonify(user_data)

@api_users.route("/users/admin/<int:user_id>", methods = ["GET"])
def obter_usuario_admin(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    user_data = {
        "id": user.id,
        "nome": user.nome,
        #"username": user.username,
        "email": user.email,
        #"cpf": user.cpf,
        #"dt_nasc": user.dt_nasc.isoformat(),
        "password": user.password
    }

    return jsonify(user_data)

@api_users.route("/users/me", methods = ["DELETE"])
@jwt_required()
def deletar_usuario():
    user_id = int(get_jwt_identity()) 
    
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário deletado"})

@api_users.route("/users/admin/<int:user_id>", methods = ["DELETE"])
def deletar_usuario_admin(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário deletado"})


    



    
