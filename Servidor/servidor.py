import socket
import random

def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Gera um número aleatório entre 20 e 30 com duas casas decimais

def main():
    # Configurações do servidor
    HOST = '0.0.0.0'  # Endereço IP do servidor
    PORT = 65432        # Porta a ser usada

    # Flag para definir se pode mandar dados de temperatura
    can_send = 1

    # Criação do socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao endereço e porta
    s.bind((HOST, PORT))

    # Habilita o servidor para aceitar conexões
    s.listen()
    print('Aguardando conexões...')

    while True:
        # Aceita a conexão do cliente
        conn, addr = s.accept()
        print('Conectado por', addr)

        # Recebe dados do cliente
        data = conn.recv(1024)
        if not data:
            break
        # Verifica se a mensagem do cliente é para solicitar temperatura
        if data.decode() == "solicitar_temperatura" and can_send == 1:
            # Exemplo de uso:
            data = str(generate_temperature())
            # Decodifica para uma sequência de bytes
            data = bytes(data + '°', 'utf-8')
        elif data.decode() == "desligar" and can_send == 1:
            # Se o cliente enviar o comando para desligar, não envia nenhum dado de temperatura
            can_send = 0
            data = b'Servidor desligando...'
        elif data.decode() == "ligar" and can_send == 0:
            # Se o cliente enviar o comando para ligar, o sensor pode enviar dado de temperatura
            can_send = 1
            data = b'Servidor ligando...'
        else:
            # Caso contrário, envia uma mensagem informando que o comando é inválido
            data = b'Comando invalido...'
            
        # Envia dados de volta para o cliente
        conn.sendall(data)

    # Fecha a conexão com o cliente
    conn.close()

# Chamada da função principal
if __name__ == "__main__":
    main()