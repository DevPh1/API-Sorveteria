from flask import Blueprint, jsonify, request
from .sorvete_model import (
    obter_sorvete, 
    listar_sorvetes, 
    adicionar_sorvete, 
    editar_sorvete, 
    apagar_sorvete, 
    listar_categorias, 
    obter_sorvetes_por_categoria, 
    SorveteNaoEncontrado
)

sorvete_blueprint = Blueprint('sorvetes', __name__)

@sorvete_blueprint.route('/sorvetes', methods=['GET'])
def listar_sorvetes_route():
    return jsonify(listar_sorvetes())

@sorvete_blueprint.route('/sorvetes/<int:id>', methods=['GET'])
def obter_sorvete_route(id):
    try:
        return jsonify(obter_sorvete(id).to_dict())
    except SorveteNaoEncontrado:
        return {'erro': 'Sorvete não encontrado'}, 404

@sorvete_blueprint.route('/sorvetes', methods=['POST'])
def adicionar_sorvete_route():
    try:
        adicionar_sorvete(request.json)
        return jsonify(listar_sorvetes()), 201
    except ValueError as e:
        return {'erro': str(e)}, 400

@sorvete_blueprint.route('/sorvetes/<int:id>', methods=['PUT'])
def editar_sorvete_route(id):
    try:
        editar_sorvete(id, request.json)
        return jsonify(obter_sorvete(id).to_dict())
    except SorveteNaoEncontrado:
        return {'erro': 'Sorvete não encontrado'}, 404

@sorvete_blueprint.route('/sorvetes/<int:id>', methods=['DELETE'])
def apagar_sorvete_route(id):
    try:
        apagar_sorvete(id)
        return {'message': 'Sorvete apagado com sucesso'}, 204
    except SorveteNaoEncontrado:
        return {'erro': 'Sorvete não encontrado'}, 404

@sorvete_blueprint.route('/categorias', methods=['GET'])
def listar_categorias_route():
    return jsonify(listar_categorias())

@sorvete_blueprint.route('/categorias/<int:id>/sorvetes', methods=['GET'])
def obter_sorvetes_por_categoria_route(id):
    sorvetes = obter_sorvetes_por_categoria(id)
    if not sorvetes:
        return {'erro': 'Não há sorvetes nesta categoria'}, 404
    return jsonify(sorvetes)
