from flask import Flask, jsonify, request
import os
import requests

ip = '192.168.1.105'
url = f"http://{ip}:8081/sensores"
url_solicitacoes = f"http://{ip}:8081/solicitacoes"

def menu():
    global url_solicitacoes
    while True:
        limpar_terminal()
        while True:
            entrada = input("############################################################################\n#       Para listar os sensores conectados digite               (1);       #\n#       Para solicitar a temperatura de um dos sensores digite  (2);       #\n#       Para solicitar o desligamento de  um sensor digite      (3);       #\n#       Para solicitar o ligamento de um sensor digite          (4).       #\n\n==>")
            try:
                num1 = int(entrada)
                if 2 <= num1 <= 4:
                    
                    break
                elif num1 == 1:
                    # Exemplo de uso
                    try:
                        sensores = obter_lista_sensores()
                        if sensores is not None:
                            limpar_terminal()
                            print("----------------------------------------------------------------------------\n                            Lista de Sensores\n----------------------------------------------------------------------------")
                            for i in sensores:
                                print(f"       {i}")
                            print("----------------------------------------------------------------------------\n")
                            input("Precione enter para voltar ao menu!")
                            limpar_terminal()
                    except Exception as e:
                        print("Broker desconectado!")
                        input("\nPrecione enter para voltar ao menu!") 
                        limpar_terminal()
                else:
                    limpar_terminal()
                    print("\nEntrada fora do intervalo. Por favor, digite um número inteiro de 1 a 4.")
            except ValueError:
                limpar_terminal()
                print("\nEntrada inválida. Por favor, digite um número inteiro de 1 a 4 ou 4 para sair.")
        
        while True:
            try:
                entrada = input("\nDigite o numero do sensor: ")
                num2 = int(entrada)  # Tenta converter a entrada para um inteiro
                limpar_terminal()
                break  # Sai do loop se a conversão for bem-sucedida
                
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                limpar_terminal()
            
        if num1 == 2:
            try:
                sensores = obter_lista_sensores()
                for i in sensores:
                    if i["id"] == num2:
                        print(f"\nTemperatura do {num2}° sensor = {i['temperatura']}")
                        input("\nPrecione enter para voltar ao menu!")
            except Exception as e:
                print("Broker desconectado!")
                input("\nPrecione enter para voltar ao menu!") 
        elif num1 == 3:
            try:
                # Dados do novo sensor a serem enviados
                novo_sensor = {"id": "", "num": num2, "Comando": 'desligar'}  # Suponha que você está adicionando um novo sensor com ID 4

                # Enviar uma solicitação POST para a API Flask para criar o novo sensor
                response = requests.post(url_solicitacoes, json=novo_sensor)
            except Exception as e:
                print("Broker desconectado!")   
                input("\nPrecione enter para voltar ao menu!") 
        else:
            try:
                # Dados do novo sensor a serem enviados
                novo_sensor = {"id": "", "num": num2, "Comando": 'ligar'}  # Suponha que você está adicionando um novo sensor com ID 4

            # Enviar uma solicitação POST para a API Flask para criar o novo sensor
                response = requests.post(url_solicitacoes, json=novo_sensor)
                
                limpar_terminal()
            except Exception as e:
                print("Broker desconectado!")
                input("\nPrecione enter para voltar ao menu!")
                
def obter_lista_sensores():
    global url
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter a lista de sensores:", response.status_code)
        input("\nPrecione enter para voltar ao menu!") 
        return None

def limpar_terminal():
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')
    else:
        os.system('clear')

def main():
    menu()

if __name__ == "__main__":
    main()