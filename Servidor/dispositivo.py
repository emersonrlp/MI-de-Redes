import socket
import random
import threading

def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Gera um número aleatório entre 20 e 30 com duas casas decimais

def handle_user_input():
    global can_send
    while True:
        user_input = input("Digite 'ligar' para ligar ou 'desligar' para desligar: ")
        if user_input.lower() == 'ligar':
            can_send = 1
            print("Servidor ligando...")
        elif user_input.lower() == 'desligar':
            can_send = 0
            print("Servidor desligando...")

def main():
    global can_send

    # Configurações do servidor TCP
    TCP_HOST = '0.0.0.0'  # Endereço IP do servidor TCP
    TCP_PORT = 65432       # Porta TCP

    # Configurações do servidor UDP
    UDP_HOST = '0.0.0.0'  # Endereço IP do servidor UDP
    UDP_PORT = 65433       # Porta UDP

    # Flag para definir se pode mandar dados de temperatura
    can_send = True

    # Criação do socket TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((TCP_HOST, TCP_PORT))
    tcp_socket.listen()

    # Criação do socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_HOST, UDP_PORT))

    print('Servidor TCP aguardando conexões na porta', TCP_PORT)

    # Iniciar thread para lidar com a entrada do usuário
    input_thread = threading.Thread(target=handle_user_input)
    input_thread.start()

    while True:
        # Aceita a conexão TCP do cliente
        conn, addr = tcp_socket.accept()
        print('Conectado por', addr)

        # Recebe dados do cliente TCP
        data = conn.recv(1024)
        if not data:
            break
        
        
        # Verifica se a mensagem do cliente é para solicitar temperatura
        if data.decode() == "desligar" and can_send:
            # Se o cliente enviar o comando para desligar, não envia nenhum dado de temperatura
            can_send = False
            response = 'Servidor desligando...'
            # Envia a resposta por UDP
            udp_socket.sendto(response.encode(), (addr[0], UDP_PORT))

        elif data.decode() == "ligar" and not can_send:
            # Se o cliente enviar o comando para ligar, o sensor pode enviar dado de temperatura
            can_send = True
            response = 'Servidor ligando...'
            # Envia a resposta por UDP
            udp_socket.sendto(response.encode(), (addr[0], UDP_PORT))
            
        if can_send:
            # Gera temperatura aleatória
            temperature = generate_temperature()
            response = str(temperature) + '°'
            # Envia a resposta por UDP
            udp_socket.sendto(response.encode(), (addr[0], UDP_PORT))
        else:
            # Se o cliente enviar o comando para solicitar_temperatura, não envia nenhum dado de temperatura
            response = 'Servidor desligado'
            # Envia a resposta por UDP
            udp_socket.sendto(response.encode(), (addr[0], UDP_PORT)) 

        # Fecha a conexão TCP com o cliente
        conn.close()

    # Aguardar até que a thread de entrada do usuário termine
    input_thread.join()

# Chamada da função principal
if __name__ == "__main__":
    main()
