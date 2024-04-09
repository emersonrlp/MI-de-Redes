import socket
import threading

# Configurações do servidor TCP
TCP_HOST = '192.168.1.106'  # Endereço IP do servidor TCP
TCP_PORT = 65432             # Porta TCP

# Configurações do servidor UDP
UDP_HOST = '192.168.1.106'  # Endereço IP do servidor UDP
UDP_PORT = 65433      # Porta UDP

def send_tcp_message(message):
    try:
        # Criação do socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta ao servidor TCP
            s.connect((TCP_HOST, TCP_PORT))

            # Envia mensagem para o servidor TCP
            s.sendall(message.encode())

    except Exception as e:
        print('Erro ao enviar mensagem TCP:', e)

def receive_udp_response():
    try:
        # Criação do socket UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Associa o socket ao endereço e porta UDP
            s.bind((UDP_HOST, UDP_PORT))
            print('Servidor UDP aguardando mensagens na porta', UDP_PORT)

            # Recebe os dados do cliente UDP
            data, addr = s.recvfrom(1024)
            print('Mensagem recebida de', addr, ':', data.decode())
    except Exception as e:
        print('Erro ao receber mensagem UDP:', e)

def main():
    # Comando a ser enviado em TCP
    command = input('Digite o comando (ligar/desligar/solicitar_temperatura): ')

    # Enviar comando em TCP em uma thread
    tcp_thread = threading.Thread(target=send_tcp_message, args=(command,))
    tcp_thread.start()

    # Receber resposta em UDP na thread principal
    receive_udp_response()

if __name__ == "__main__":
    main()
    
