import threading
from api import app
import socket
import requests
import time
import os
import datetime

url = "http://127.0.0.1:8081/sensores"
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
        if addr[0] in enderecos:
            indice = enderecos.index(addr[0])
            clients[indice] = client
            
        else:
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
        threading.Thread(target=atualizar_dado, args=[data_udp, addr_udp]).start()

def data_atual():
    agora = datetime.datetime.now()
    ano = agora.year
    mes = agora.month
    dia = agora.day
    hora = agora.hour
    minutos = agora.minute
    segundos = agora.second
    
    horario= {
        "ano": ano,
        "mes": mes,
        "dia": dia,
        "hora": hora,
        "minutos": minutos,
        "segundos": segundos
    }
    
    return horario

def atualizar_dado(data_udp, addr_udp):
    # Verificar se o valor desejado está presente em cada dicionário
    for i in enderecos:
        if addr_udp[0] == i:
            temp = data_udp.decode()
            dados_atualizados = {"Sensor": addr_udp[0], "temperatura": temp, "data": data_atual()}
            ID = enderecos.index(i) + 1
            ID = str(ID)
            url_sensor = 'http://127.0.0.1:8081/sensores/'+ ID
            response = requests.put(url_sensor, json=dados_atualizados)
    print('\nConectado por UDP:', addr_udp)
    print('Mensagem recebida do cliente UDP:', data_udp.decode())
    time.sleep(0.5)
def tratamento_mensagens(client, endereco):
    while True:
        try:
            solicitacoes = obter_lista_solicitacoes()
            if len(solicitacoes) > 0:
                solicitacao = solicitacoes[0]
                num = solicitacao["num"]
                msg = solicitacao["Comando"]

                entrada_bytes = msg.encode('utf-8')
                try:
                    enviar_tcp(entrada_bytes, num, endereco)
                    remover_solicitacao(1)
                except Exception as e:
                    remover_solicitacao(1)
                    print("", e)
            time.sleep(0.5)
        except:
            deleteCliente(client)
            enderecos.remove(endereco)
            break

def remover_solicitacao(solicitacoes_id):
    url = f"http://127.0.0.1:8081/solicitacoes/{solicitacoes_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Sensor removido com sucesso.")
    else:
        print("Erro ao remover o sensor:", response.status_code)

def obter_lista_solicitacoes():
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
        deleteCliente(clients[num -1])
        enderecos.remove(endereco)

# Deleta o cliente da lista
def deleteCliente(client):
    clients.remove(client)

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