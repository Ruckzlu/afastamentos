from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import ProgrammingError
import hashlib

db = SQLAlchemy()

class Viagens(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    postGrad = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    ida = db.Column(db.String(20), nullable=False)
    volta = db.Column(db.String(20), nullable=False)
    destino = db.Column(db.String(100), nullable=False)

    def __init__(self, postGrad, nome, ida, volta, destino):
        self.postGrad = postGrad
        self.nome = nome
        self.ida = ida
        self.volta = volta
        self.destino = destino
        self.id = self.generate_hash_id()

    def generate_hash_id(self):
        data_to_hash = f"{self.postGrad}{self.nome}{self.ida}{self.volta}{self.destino}"
        return hashlib.md5(data_to_hash.encode()).hexdigest()

def create_tables():
    try:
        db.create_all()
        print("Tabelas criadas com sucesso!")
    except ProgrammingError:
        print("As tabelas já existem no banco de dados.")