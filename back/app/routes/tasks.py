from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date

api_tasks = Blueprint('tasks', __name__)

@api_tasks.route("/tasks/me", methods = ["POST"])
@jwt_required()
def criar_tarefa():
    data = request.json

    user_id = int(get_jwt_identity())
    title = data["title"]
    description = data["description"]
    prazo = datetime.strptime(data["prazo"], "%Y-%m-%d").date()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if not title or not description:
        return jsonify({"message": "Erro! Campos obrigatórios em branco"}), 400
    
    #Tratamento de título
    if len(title) > 100:
        return jsonify({"message": "O título deve ter até 100 caracteres"}), 400
    
    #Tratamento de descrição
    if len(description) > 300:
        return jsonify({"message": "A descrição deve ter até 300 caracteres"}), 400
    
    #Tratamento de prazo limite
    if prazo < date.today():
        return jsonify({"message": "Erro! Data inválida"}), 400

    new_task = Task(id_user = user_id,
                    title = title,
                    description = description,
                    prazo = prazo,
                    status = "pendente")

    #Tratamento de integridade
    try:
        db.session.add(new_task)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Erro! Esse título já existe!"}), 400
    
    return jsonify({"message": "Tarefa criada com sucesso!",
                    "id": new_task.id}), 201

@api_tasks.route("/tasks/admin/<int:id_user>", methods = ["POST"])
def criar_tarefa_admin(id_user):
    data = request.json

    title = data["title"]
    description = data["description"]
    prazo = datetime.strptime(data["prazo"], "%Y-%m-%d").date()

    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if not title or not description:
        return jsonify({"message": "Erro! Campos obrigatórios em branco"}), 400
    
    #Tratamento de título
    if len(title) > 100:
        return jsonify({"message": "O título deve ter até 100 caracteres"}), 400
    
    #Tratamento de descrição
    if len(description) > 300:
        return jsonify({"message": "A descrição deve ter até 300 caracteres"}), 400
    
    #Tratamento de prazo limite
    if prazo < date.today():
        return jsonify({"message": "Erro! Data inválida"}), 400

    new_task = Task(id_user = id_user,
                    title = title,
                    description = description,
                    prazo = prazo,
                    status = "pendente")

    #Tratamento de integridade
    try:
        db.session.add(new_task)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Erro! Esse título já existe!"}), 400
    
    return jsonify({"message": "Tarefa criada com sucesso!",
                    "id": new_task.id}), 201

@api_tasks.route("/tasks/me", methods=["GET"])
@jwt_required()
def listar_tasks_usuario():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    status = request.args.get("status")
    fora_do_prazo = request.args.get("fora_do_prazo")

    tasks = user.tasks

    result = []
    for task in tasks:
        if status and task.status != status:
            continue

        if fora_do_prazo == "true" and not task.fora_do_prazo:
            continue

        result.append({"id": task.id,
                       "id_user": task.id_user,
                       "title": task.title,
                       "description": task.description,
                       "prazo": task.prazo.isoformat(),
                       "status": task.status,
                       "fora_do_prazo": task.fora_do_prazo})

    return jsonify(result), 200

@api_tasks.route("/tasks/admin/<int:user_id>", methods=["GET"])
def listar_tasks_usuario_admin(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    status = request.args.get("status")
    fora_do_prazo = request.args.get("fora_do_prazo")

    tasks = user.tasks

    result = []
    for task in tasks:
        if status and task.status != status:
            continue

        if fora_do_prazo == "true" and not task.fora_do_prazo:
            continue

        result.append({"id": task.id,
                       "id_user": task.id_user,
                       "title": task.title,
                       "description": task.description,
                       "prazo": task.prazo.isoformat(),
                       "status": task.status,
                       "fora_do_prazo": task.fora_do_prazo})

    return jsonify(result), 200

@api_tasks.route("/tasks/me/<int:task_id>", methods = ["PUT"])
@jwt_required()
def alterar_dados(task_id):
    data = request.json
    user_id = int(get_jwt_identity())
    
    title = data["title"]
    description = data["description"]
    prazo = datetime.strptime(data["prazo"], "%Y-%m-%d").date()
    
    if not title or not description or not prazo:
        return jsonify({"message": "Erro! Campos obrigatórios em branco"}), 400
    
    #Tratamento de título
    if len(title) > 100:
        return jsonify({"message": "O título deve ter até 100 caracteres"}), 400
    
    #Tratamento de descrição
    if len(description) > 300:
        return jsonify({"message": "A descrição deve ter até 300 caracteres"}), 400
    
    #Tratamento de prazo limite
    if prazo < date.today():
        return jsonify({"message": "Erro! Data inválida"}), 400

    result = Task.query.filter_by(id = task_id, id_user = user_id).first()
    
    if not result:
        return jsonify({"message": "Tarefa não encontrado!"}), 404

    result.title = title
    result.description = description
    result.prazo = prazo

    #Tratamento de integridade
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Erro! Esse título já existe!"}), 400
    
    return jsonify({"message": "Tarefa editada com sucesso!"}), 200

@api_tasks.route("/tasks/admin/<int:user_id>/<int:task_id>", methods = ["PUT"])
def alterar_dados_admin(user_id, task_id):
    data = request.json
    
    title = data["title"]
    description = data["description"]
    prazo = datetime.strptime(data["prazo"], "%Y-%m-%d").date()
    
    if not title or not description or not prazo:
        return jsonify({"message": "Erro! Campos obrigatórios em branco"}), 400
    
    #Tratamento de título
    if len(title) > 100:
        return jsonify({"message": "O título deve ter até 100 caracteres"}), 400
    
    #Tratamento de descrição
    if len(description) > 300:
        return jsonify({"message": "A descrição deve ter até 300 caracteres"}), 400
    
    #Tratamento de prazo limite
    if prazo < date.today():
        return jsonify({"message": "Erro! Data inválida"}), 400

    result = Task.query.filter_by(id = task_id, id_user = user_id).first()
    
    if not result:
        return jsonify({"message": "Tarefa não encontrado!"}), 404

    result.title = title
    result.description = description
    result.prazo = prazo

    #Tratamento de integridade
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Erro! Esse título já existe!"}), 400
    
    return jsonify({"message": "Tarefa editada com sucesso!"}), 200

@api_tasks.route("/tasks/me/<int:task_id>/status", methods = ["PATCH"])
@jwt_required()
def alterar_status(task_id):
    data = request.json

    user_id = int(get_jwt_identity())
    status = data["status"]

    if status != "concluido":
        return jsonify({"message": "Status requerido não suportado!"}), 400
    
    result = Task.query.filter_by(id = task_id, id_user = user_id).first()
    
    if not result:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    
    result.status = status
    db.session.commit()

    return jsonify({"message": "Status atualizado!"}), 200

@api_tasks.route("/tasks/admin/<int:user_id>/<int:task_id>/status", methods = ["PATCH"])
def alterar_status_admin(user_id, task_id):
    data = request.json

    result = Task.query.filter_by(id = task_id, id_user = user_id).first()
    
    if not result:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    
    status = data["status"]
    
    if status != "concluido":
        return jsonify({"message": "Status requerido não suportado!"}), 400
    
    result.status = status
    db.session.commit()

    return jsonify({"message": "Status atualizado!"}), 200

@api_tasks.route("/tasks/me/<int:task_id>", methods = ["DELETE"])
@jwt_required()
def deletar_tarefa(task_id):
    user_id = int(get_jwt_identity())
    result = Task.query.filter_by(id = task_id, id_user = user_id).first()

    if not result:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    db.session.delete(result)
    db.session.commit()

    return jsonify({"message": "Tarefa deletada com sucesso!"}), 200

@api_tasks.route("/tasks/admin/<int:user_id>/<int:task_id>", methods = ["DELETE"])
def deletar_tarefa_admin(user_id, task_id):
    result = Task.query.filter_by(id = task_id, id_user = user_id).first()

    if not result:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    db.session.delete(result)
    db.session.commit()

    return jsonify({"message": "Tarefa deletada com sucesso!"}), 200