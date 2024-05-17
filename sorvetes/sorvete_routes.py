from flask import Blueprint, jsonify, request, Response, render_template, redirect, url_for
from .sorvete_model import (
    sorvete_por_id, 
    SorveteNaoEncontrado, 
    lista_sorvete, 
    adiciona_sorvete, 
    edita_sorvete, 
    apaga_sorvete, 
    Categoria, 
    categorias, 
    categoria_por_id
)

sorvete_blueprint = Blueprint('sorvetes', __name__)

@sorvete_blueprint.route('/sorvetes', methods=['GET'])
def get_sorvetes():
    sorvetes = lista_sorvete()
    return render_template('sorvetes.html', sorvetes=sorvetes)

@sorvete_blueprint.route('/sorvetes/<int:nSorvete>', methods=['GET'])
def get_sorvete(nSorvete):
    try:
        sorvete = sorvete_por_id(nSorvete)
        return jsonify(sorvete)  
    except SorveteNaoEncontrado:
        return {'erro': 'Sorvete não encontrado'}, 404

@sorvete_blueprint.route('/sorvetes/adicionar', methods=['GET'])
def adicionar_sorvete_page():
    return render_template('add_sorvete.html')

@sorvete_blueprint.route('/sorvetes', methods=['POST'])
def add_sorvete():
    if request.content_type != 'application/json':
        return jsonify({'erro': 'Tipo de Mídia Não Suportado'}), 415

    sorvete_data = request.get_json()
    try:
        adiciona_sorvete(sorvete_data)
        return redirect(url_for('sorvete_blueprint.get_sorvetes')), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@sorvete_blueprint.route('/sorvetes/editar', methods=['GET'])
def atualizar_sorvete_page():
    return render_template('atl_sorvete.html')

@sorvete_blueprint.route('/sorvetes/<int:nSorvete>', methods=['PUT'])
def update_sorvete(nSorvete):
    if request.content_type != 'application/json':
        return jsonify({'erro': 'Tipo de Mídia Não Suportado'}), 415

    sorvete_data = request.get_json()
    try:
        edita_sorvete(nSorvete, sorvete_data)
        return redirect(url_for('sorvete_blueprint.get_sorvete', nSorvete=nSorvete))
    except (SorveteNaoEncontrado, ValueError) as e:
        return jsonify({'erro': str(e)}), 404

@sorvete_blueprint.route('/sorvetes/excluir', methods=['GET'])
def excluir_sorvete_page():
    return render_template('ex_sorvete.html')

@sorvete_blueprint.route('/sorvetes/<int:nSorvete>', methods=['DELETE'])
def delete_sorvete(nSorvete):
    try:
        apaga_sorvete(nSorvete)
        return '', 204  
    except SorveteNaoEncontrado:
        return jsonify({'erro': 'Sorvete não encontrado'}), 404
    

@sorvete_blueprint.route('/categorias', methods=['GET'])
def get_categorias():
    categorias_list = categorias()
    return render_template('categorias.html', categorias=categorias_list)

@sorvete_blueprint.route('/categorias/<int:nCategoria>', methods=['GET'])
def get_categoria(nCategoria):
    try:
        categoria = categoria_por_id(nCategoria)
        return jsonify(categoria.to_dict())
    except SorveteNaoEncontrado:
        return {'erro': 'Categoria não encontrada'}, 404

@sorvete_blueprint.route('/sorvetes/categorias/<int:nCategoria>', methods=['GET'])
def get_sorvetes_por_categoria(nCategoria):
    try:
        sorvetes = get_sorvetes_por_categoria(nCategoria)
        if not sorvetes:
            return jsonify({'erro': 'Não há sorvetes nesta categoria'}), 404
        return jsonify([sorvete.to_dict() for sorvete in sorvetes])
    except Exception as e:
        return {'erro': str(e)}, 500
