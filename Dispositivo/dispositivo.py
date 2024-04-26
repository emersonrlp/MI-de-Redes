import socket
import time
import random
import threading
import os

# Configurações do servidor
HOST = '192.168.1.106'  # Endereço IP do servidor
PORT = 7777             # Porta a ser usada
UDP_PORT = 7778         # Porta UDP
MESSAGE = b'Hello, TCP Server!'
can_send = True

def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Gera um número aleatório entre 20 e 30 com duas casas decimais

def receber_mensagem_tcp():
    global can_send
    global MESSAGE
    while True:
        try:
            
                # Criação do socket TCP
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # Conecta ao servidor
                    s.connect((HOST, PORT))
                    # Recebe mensagem do servidor
                    while True:
                        data = s.recv(1024)
                        print('Mensagem recebida do servidor:', data.decode())
                        if data.decode() == 'desligar' and can_send == True:
                            MESSAGE = b'Sensor desligado'
                            can_send = False
                        elif data.decode() == 'ligar' and can_send == False:
                            MESSAGE = b'Sensor ligando'
                            can_send = True
                        # Envia mensagem para o servidor
                        s.sendall(MESSAGE)
                        time.sleep(0.5)
                        limpar_terminal()
                        print("Digite 'ligar' para ligar ou 'desligar' para desligar: ")
        except Exception as e:
            time.sleep(2)
            print('Erro : ', e)
            limpar_terminal()

def enviar_mensagem_udp():
    global can_send
    try:
        # Criação do socket UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            while True:
                if can_send == True:
                    temperature = generate_temperature()
                    MESSAGE = str(temperature) + '°'
                else:
                    MESSAGE = 'Sensor desligado'
                
                # Envia mensagem para o servidor
                udp_socket.sendto(MESSAGE.encode(), (HOST, UDP_PORT))
                #print('Mensagem enviada com sucesso via UDP')
                time.sleep(0.5)
    except Exception as e:
        print('Erro ao enviar mensagem UDP:', e)
        time.sleep(3)
        limpar_terminal()

def entrada():
    global can_send
    while True:
        user_input = input("Digite 'ligar' para ligar ou 'desligar' para desligar: \n")
        while user_input != 'ligar' and user_input != 'desligar':
            limpar_terminal()
            user_input = input("Digite 'ligar' para ligar ou 'desligar' para desligar: \n")
        if user_input.lower() == 'ligar':
            can_send = True
            print("Servidor ligando...")
            time.sleep(3)
            
        elif user_input.lower() == 'desligar':
            can_send = False
            print("Servidor desligando...")
            time.sleep(3)
        limpar_terminal()

def limpar_terminal():
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')
    else:
        os.system('clear')

def main():
    udp_thread = threading.Thread(target=enviar_mensagem_udp)
    entrada_thread = threading.Thread(target=entrada)
    receber_mensagem = threading.Thread(target=receber_mensagem_tcp)  
    
    udp_thread.start()
    entrada_thread.start()
    receber_mensagem.start()    

if __name__ == "__main__":
    main()
