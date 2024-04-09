import socket

# Configurações do servidor
HOST = '192.168.1.106'  # Endereço IP do servidor
PORT = 65432        # Porta a ser usada

# Criação do socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
s.connect((HOST, PORT))
MESSAGE = input('Digite: ligar/Desligar/solicitar_temperatura')
MESSAGE = bytes(MESSAGE, 'utf-8')
# Envia mensagem para o servidor
s.sendall(MESSAGE)

# Recebe resposta do servidor
data = s.recv(1024)

print('Mensagem recebida do servidor:', data.decode())

# Fecha o socket
s.close()
