from config import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {"nome": self.nome, "id": self.id}

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
            "categoria": self.categoria.nome if self.categoria else None,
            "quantidade_estoque": self.quantidade_estoque,
             "id": self.id
        }

class SorveteNaoEncontrado(Exception):
    pass

def obter_sorvete(id):
    sorvete = Sorvete.query.get(id)
    if not sorvete:
        raise SorveteNaoEncontrado
    return sorvete

def listar_sorvetes():
    return [sorvete.to_dict() for sorvete in Sorvete.query.all()]

def adicionar_sorvete(dados_sorvete):
    nome_categoria = dados_sorvete.get("categoria")
    if not nome_categoria:
        raise ValueError("Categoria não especificada")
    
    categoria = Categoria.query.filter_by(nome=nome_categoria).first()
    if not categoria:
        categoria = Categoria(nome=nome_categoria)
        db.session.add(categoria)
        db.session.commit()
    
    novo_sorvete = Sorvete(
        nome=dados_sorvete.get("nome"),
        preco=dados_sorvete.get("preco"),
        categoria_id=categoria.id,
        quantidade_estoque=dados_sorvete.get("quantidade_estoque")
    )
    db.session.add(novo_sorvete)
    db.session.commit()

def editar_sorvete(id, dados_atualizados):
    sorvete = obter_sorvete(id)
    for campo, valor in dados_atualizados.items():
        if hasattr(sorvete, campo):
            setattr(sorvete, campo, valor)
    db.session.commit()

def apagar_sorvete(id):
    sorvete = obter_sorvete(id)
    db.session.delete(sorvete)
    db.session.commit()

def listar_categorias():
    return [categoria.to_dict() for categoria in Categoria.query.all()]

def obter_sorvetes_por_categoria(id):
    return [sorvete.to_dict() for sorvete in Sorvete.query.filter_by(categoria_id=id).all()]
