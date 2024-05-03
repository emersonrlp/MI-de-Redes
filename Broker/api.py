from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de sensores e solicitações
sensores = []
solicitacoes = []

# Rotas para sensores
@app.route('/sensores', methods=['GET'])
def get_sensores():
    return jsonify(sensores)

@app.route('/sensores/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = next((sensor for sensor in sensores if sensor['id'] == sensor_id), None)
    if sensor:
        return jsonify(sensor)
    return jsonify({'message': 'Sensor não encontrado'}), 404

@app.route('/sensores', methods=['POST'])
def criar_sensor():
    novo_sensor = request.json
    novo_sensor['id'] = len(sensores) + 1
    sensores.append(novo_sensor)
    return jsonify(novo_sensor), 201

@app.route('/sensores/<int:sensor_id>', methods=['PUT'])
def atualizar_sensor(sensor_id):
    sensor = next((sensor for sensor in sensores if sensor['id'] == sensor_id), None)
    if not sensor:
        return jsonify({'message': 'Sensor não encontrado'}), 404
    dados_atualizados = request.json
    sensor.update(dados_atualizados)
    return jsonify(sensor)

@app.route('/sensores/<int:sensor_id>', methods=['DELETE'])
def excluir_sensor(sensor_id):
    global sensores
    sensores = [sensor for sensor in sensores if sensor['id'] != sensor_id]
    return jsonify({'message': 'Sensor excluído com sucesso'})

# Rotas para solicitações
@app.route('/solicitacoes', methods=['GET'])
def get_solicitacoes():
    return jsonify(solicitacoes)

@app.route('/solicitacoes/<int:solicitacao_id>', methods=['GET'])
def get_solicitacao(solicitacao_id):
    solicitacao = next((solicitacao for solicitacao in solicitacoes if solicitacao['id'] == solicitacao_id), None)
    if solicitacao:
        return jsonify(solicitacao)
    return jsonify({'message': 'Solicitação não encontrada'}), 404

@app.route('/solicitacoes', methods=['POST'])
def criar_solicitacao():
    nova_solicitacao = request.json
    nova_solicitacao['id'] = len(solicitacoes) + 1
    solicitacoes.append(nova_solicitacao)
    return jsonify(nova_solicitacao), 201

@app.route('/solicitacoes/<int:solicitacao_id>', methods=['PUT'])
def atualizar_solicitacao(solicitacao_id):
    solicitacao = next((solicitacao for solicitacao in solicitacoes if solicitacao['id'] == solicitacao_id), None)
    if not solicitacao:
        return jsonify({'message': 'Solicitação não encontrada'}), 404
    dados_atualizados = request.json
    solicitacao.update(dados_atualizados)
    return jsonify(solicitacao)

@app.route('/solicitacoes/<int:solicitacao_id>', methods=['DELETE'])
def excluir_solicitacao(solicitacao_id):
    global solicitacoes
    solicitacoes = [solicitacao for solicitacao in solicitacoes if solicitacao['id'] != solicitacao_id]
    return jsonify({'message': 'Solicitação excluída com sucesso'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)