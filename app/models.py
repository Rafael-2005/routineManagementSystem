from .database import db
from datetime import date, datetime


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # relacionamento: 1 usuário -> N rotinas
    rotinas = db.relationship('Rotina', backref='usuario', lazy=True)

    # relacionamento: 1 usuário -> N logs
    logs = db.relationship('Log', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Rotina(db.Model):
    __tablename__ = 'rotinas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ativa = db.Column(db.Boolean, default=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # relacionamento: 1 rotina -> N execuções
    execucoes = db.relationship('Execucao', backref='rotina', lazy=True)

    def __repr__(self):
        return f"<Rotina {self.nome}>"

class Execucao(db.Model):
    __tablename__ = 'execucoes'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=date.today, nullable=False)

    rotina_id = db.Column(db.Integer, db.ForeignKey('rotinas.id'), nullable=False)

    def __repr__(self):
        return f"<Execucao {self.data}>"


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __repr__(self):
        return f"<Log {self.acao}>"