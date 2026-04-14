from flask import Blueprint, request, jsonify
from datetime import date, datetime

from .database import db
from .models import Usuario, Rotina, Execucao, Log

main = Blueprint('main', __name__)


def registrar_log(usuario_id, acao):
    log = Log(
        usuario_id=usuario_id,
        acao=acao,
        data=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()


# =========================
# USUÁRIOS
# =========================
@main.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()

    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    email_existente = Usuario.query.filter_by(email=data['email']).first()
    if email_existente:
        return jsonify({"erro": "Email já cadastrado"}), 400

    usuario = Usuario(
        nome=data['nome'],
        email=data['email']
    )

    db.session.add(usuario)
    db.session.commit()

    registrar_log(usuario.id, "Usuário criado")

    return jsonify({"msg": "Usuário criado com sucesso"}), 201


@main.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()

    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "nome": u.nome,
            "email": u.email
        })

    return jsonify(resultado), 200


# =========================
# ROTINAS
# =========================
@main.route('/rotinas', methods=['POST'])
def criar_rotina():
    data = request.get_json()

    if not data or 'nome' not in data or 'usuario_id' not in data:
        return jsonify({"erro": "Nome e usuario_id são obrigatórios"}), 400

    usuario = Usuario.query.get(data['usuario_id'])
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    rotina = Rotina(
        nome=data['nome'],
        usuario_id=data['usuario_id'],
        ativa=True
    )

    db.session.add(rotina)
    db.session.commit()

    registrar_log(usuario.id, f"Rotina '{rotina.nome}' criada")

    return jsonify({"msg": "Rotina criada com sucesso"}), 201


@main.route('/rotinas', methods=['GET'])
def listar_rotinas():
    rotinas = Rotina.query.all()

    resultado = []
    for r in rotinas:
        resultado.append({
            "id": r.id,
            "nome": r.nome,
            "ativa": r.ativa,
            "usuario_id": r.usuario_id
        })

    return jsonify(resultado), 200


@main.route('/rotinas/<int:id>', methods=['PUT'])
def atualizar_rotina(id):
    rotina = Rotina.query.get(id)

    if not rotina:
        return jsonify({"erro": "Rotina não encontrada"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400

    if 'nome' in data:
        rotina.nome = data['nome']

    if 'ativa' in data:
        rotina.ativa = data['ativa']

    db.session.commit()

    registrar_log(rotina.usuario_id, f"Rotina '{rotina.nome}' atualizada")

    return jsonify({"msg": "Rotina atualizada com sucesso"}), 200


@main.route('/rotinas/<int:id>', methods=['DELETE'])
def deletar_rotina(id):
    rotina = Rotina.query.get(id)

    if not rotina:
        return jsonify({"erro": "Rotina não encontrada"}), 404

    nome_rotina = rotina.nome
    usuario_id = rotina.usuario_id

    db.session.delete(rotina)
    db.session.commit()

    registrar_log(usuario_id, f"Rotina '{nome_rotina}' removida")

    return jsonify({"msg": "Rotina removida com sucesso"}), 200


# =========================
# EXECUÇÕES
# =========================
@main.route('/executar', methods=['POST'])
def executar_rotina():
    data = request.get_json()

    if not data or 'rotina_id' not in data:
        return jsonify({"erro": "rotina_id é obrigatório"}), 400

    rotina = Rotina.query.get(data['rotina_id'])

    if not rotina:
        return jsonify({"erro": "Rotina não encontrada"}), 404

    if not rotina.ativa:
        return jsonify({"erro": "Rotina está inativa"}), 400

    hoje = date.today()

    execucao_existente = Execucao.query.filter_by(
        rotina_id=rotina.id,
        data=hoje
    ).first()

    if execucao_existente:
        return jsonify({"erro": "Rotina já executada hoje"}), 400

    nova_execucao = Execucao(
        rotina_id=rotina.id,
        data=hoje
    )

    db.session.add(nova_execucao)
    db.session.commit()

    registrar_log(rotina.usuario_id, f"Rotina '{rotina.nome}' executada")

    return jsonify({"msg": "Execução registrada com sucesso"}), 201


@main.route('/execucoes', methods=['GET'])
def listar_execucoes():
    execucoes = Execucao.query.all()

    resultado = []
    for e in execucoes:
        resultado.append({
            "id": e.id,
            "data": e.data.strftime('%Y-%m-%d'),
            "rotina_id": e.rotina_id
        })

    return jsonify(resultado), 200


# =========================
# LOGS
# =========================
@main.route('/logs', methods=['GET'])
def listar_logs():
    logs = Log.query.all()

    resultado = []
    for l in logs:
        resultado.append({
            "id": l.id,
            "acao": l.acao,
            "data": l.data.strftime('%Y-%m-%d %H:%M:%S'),
            "usuario_id": l.usuario_id
        })

    return jsonify(resultado), 200