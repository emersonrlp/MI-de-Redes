import socket

# Configurações do servidor
HOST = '0.0.0.0'  # Endereço IP do servidor
PORT = 65432        # Porta a ser usada

# Criação do socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Associa o socket ao endereço e porta
    s.bind((HOST, PORT))
    # Habilita o servidor para aceitar conexões
    s.listen()
    print('Aguardando conexões...')
    # Aceita a conexão do cliente
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            # Recebe dados do cliente
            data = conn.recv(1024)
            if not data:
                break
            # Envia dados de volta para o cliente
            conn.sendall(data)
