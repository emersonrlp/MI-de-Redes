import threading
from flask import Flask, jsonify, request
import socket
import requests
import time
import os

app = Flask(__name__)

url = "http://127.0.0.1:8081/sensores"

# Lista de sensores e solicitações
sensores = []
solicitacoes = []

#Lista de endereços
enderecos = []

clients = []

conectados = {}

def broker():
    id = 0
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server_tcp.bind(('0.0.0.0', 7777))
        server_tcp.listen()
    except:
        return print('\nNão foi possível iniciar o servidor tcp!\n')

    try:
        server_udp.bind(('0.0.0.0', 7778))
    except:
        return print('\nNão foi possível iniciar o servidor udp!\n')
    
    while True:
        client, addr = server_tcp.accept()
        if addr[0] not in enderecos:
            clients.append(client)
            enderecos.append(addr[0])
            id +=1

            # Dados do novo sensor a serem enviados
            novo_sensor = {"Sensor": addr[0],"id": id, "temperatura": ''}  # Suponha que você está adicionando um novo sensor com ID 4

            # Enviar uma solicitação POST para a API Flask para criar o novo sensor
            response = requests.post(url, json=novo_sensor)

        thread1 = threading.Thread(target=receber_udp, args=[server_udp])
        thread1.start()
        thread = threading.Thread(target=tratamento_mensagens, args=[client, addr[0]])
        thread.start()

def receber_udp(server_udp):
    global enderecos
    while True:
        # Recebe dados do cliente UDP
        data_udp, addr_udp = server_udp.recvfrom(1024)
        # Verificar se o valor desejado está presente em cada dicionário
        for i in enderecos:
            if addr_udp[0] == i:
                temp = data_udp.decode()
                dados_atualizados = {"Sensor": addr_udp[0], "temperatura": temp}
                ID = enderecos.index(i) + 1
                ID = str(ID)
                url_sensor = 'http://127.0.0.1:8081/sensores/'+ ID
                response = requests.put(url_sensor, json=dados_atualizados)
        print('\nConectado por UDP:', addr_udp)
        print('Mensagem recebida do cliente UDP:', data_udp.decode())
        time.sleep(3)
def tratamento_mensagens(client, endereco):
    while True:
        try:
            solicitacoes = obter_lista_sensores()
            if len(solicitacoes) > 0:
                solicitacao = solicitacoes[0]
                num = solicitacao["num"]
                msg = solicitacao["Comando"]

                entrada_bytes = msg.encode('utf-8')
                try:
                    enviar_tcp(entrada_bytes, num, endereco)
                    remover_sensor(1)
                except Exception as e:
                    print("", e)
            time.sleep(3)
        except:
            deleteClient(client)
            enderecos.remove(endereco)
            break

def remover_sensor(solicitacoes_id):
    url = f"http://127.0.0.1:8081/solicitacoes/{solicitacoes_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Sensor removido com sucesso.")
    else:
        print("Erro ao remover o sensor:", response.status_code)

def obter_lista_sensores():
    url_solicitacoes = "http://127.0.0.1:8081/solicitacoes"
    response = requests.get(url_solicitacoes)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter a lista de sensores:", response.status_code)
        return None
    
#Envia mensagem ao cliente escolhido
def enviar_tcp(msg, num, endereco):
    try:
        clients[num - 1].send(msg)
    except:
        deleteClient(clients[num -1])
        enderecos.remove(endereco)

# Deleta o cliente da lista
def deleteClient(client):
    clients.remove(client)

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

def main():
    try:
        # Inicia os servidores TCP e UDP em threads separadas
        tcp_thread = threading.Thread(target=broker)
        tcp_thread.start()

        # Inicia a aplicação Flask
        app.run(host='0.0.0.0', port=8081, debug=True)

    except Exception as e:
        print('Erro:', e)
if __name__ == "__main__":
    main()