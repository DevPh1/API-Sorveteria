
from config import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }

class Sorvete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)

    categoria = db.relationship('Categoria', backref=db.backref('sorvetes', lazy=True))

    def to_dict(self):
        return {
            "nome": self.nome,
            "preco": self.preco,
            "categoria_id": self.categoria_id,
            "categoria": self.categoria.nome if self.categoria else None,
            "quantidade_estoque": self.quantidade_estoque
        }

class SorveteNaoEncontrado(Exception):
    pass

def sorvete_por_id(id):
    sorvete = Sorvete.query.get(id)
    if not sorvete:
        raise SorveteNaoEncontrado
    return sorvete

def adiciona_sorvete(sorvete_data):
    nome_categoria = sorvete_data.get("categoria")
    if not nome_categoria:
        raise ValueError("Categoria não especificada")
    
    categoria = Categoria.query.filter_by(nome=nome_categoria).first()
    
    if not categoria:
        categoria = Categoria(nome=nome_categoria)
        db.session.add(categoria)
        db.session.commit()
    
    nome_sorvete = sorvete_data.get("nome")
    if not nome_sorvete:
        raise ValueError("Nome do sorvete não especificado")
    
    preco = sorvete_data.get("preco")
    if preco is None or preco <= 0:
        raise ValueError("Preço do sorvete inválido")
    
    quantidade_estoque = sorvete_data.get("quantidade_estoque")
    if quantidade_estoque is None or quantidade_estoque < 0:
        raise ValueError("Quantidade em estoque do sorvete inválida")
    
    novo_sorvete = Sorvete(
        nome=nome_sorvete,
        preco=preco,
        categoria_id=categoria.id,
        quantidade_estoque=quantidade_estoque
    )
    db.session.add(novo_sorvete)
    db.session.commit()

def lista_sorvete():
    sorvetes = Sorvete.query.all()
    return [sorvete.to_dict() for sorvete in sorvetes]

def apaga_sorvete(id_sorvete):
    sorvete = sorvete_por_id(id_sorvete)
    db.session.delete(sorvete)
    db.session.commit()

def edita_sorvete(id_sorvete, novos_dados):
    sorvete = sorvete_por_id(id_sorvete)
    for campo, valor in novos_dados.items():
        if hasattr(sorvete, campo):
            setattr(sorvete, campo, valor)
    db.session.commit()

def categorias():
    categorias = Categoria.query.all()
    return [categoria.to_dict() for categoria in categorias]

def categoria_por_id(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        raise SorveteNaoEncontrado
    return categoria

def get_sorvetes_por_categoria(id):
    sorvetes = Sorvete.query.filter_by(categoria_id=id).all()
    return sorvetes

        