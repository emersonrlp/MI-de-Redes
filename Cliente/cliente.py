from flask import Flask, jsonify, request
import threading
import os
import requests

url = "http://127.0.0.1:8081/sensores"
url_solicitacoes = "http://127.0.0.1:8081/solicitacoes"

def menu():
    global url_solicitacoes
    while True:
        limpar_terminal()
        while True:
            entrada = input("############################################################################\n#       Para listar os sensores conectados digite               (1);       #\n#       Para solicitar a temperatura de um dos sensores digite  (2);       #\n#       Para solicitar o desligamento de  um sensor digite      (3);       #\n#       Para solicitar o ligamento de um sensor digite          (4).       #\n==>")
            try:
                num1 = int(entrada)
                if 2 <= num1 <= 4:
                    
                    break
                elif num1 == 1:
                    # Exemplo de uso
                    sensores = obter_lista_sensores()
                    if sensores is not None:
                        print("\nLista de Sensores")
                        for i in sensores:
                            print("",i)
                        input("Precione enter para continuar!")
                        limpar_terminal()
                else:
                    limpar_terminal()
                    print("Entrada fora do intervalo. Por favor, digite um número inteiro de 1 a 4.")
            except ValueError:
                limpar_terminal()
                print("Entrada inválida. Por favor, digite um número inteiro de 1 a 4 ou 4 para sair.")
        
        while True:
            try:
                entrada = input("Digite o numero do sensor: ")
                num2 = int(entrada)  # Tenta converter a entrada para um inteiro
                break  # Sai do loop se a conversão for bem-sucedida
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
        if num1 == 2:
            sensores = obter_lista_sensores()
            for i in sensores:
                if i["id"] == num2:
                    print(i["temperatura"])
                    input("Precione enter para continuar!")
        elif num1 == 3:
            # Dados do novo sensor a serem enviados
            novo_sensor = {"id": "", "num": num2, "Comando": 'desligar'}  # Suponha que você está adicionando um novo sensor com ID 4

        # Enviar uma solicitação POST para a API Flask para criar o novo sensor
            response = requests.post(url_solicitacoes, json=novo_sensor)
        else:
            # Dados do novo sensor a serem enviados
            novo_sensor = {"id": "", "num": num2, "Comando": 'ligar'}  # Suponha que você está adicionando um novo sensor com ID 4

        # Enviar uma solicitação POST para a API Flask para criar o novo sensor
            response = requests.post(url_solicitacoes, json=novo_sensor)
        limpar_terminal()

def obter_lista_sensores():
    url = "http://127.0.0.1:8081/sensores"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter a lista de sensores:", response.status_code)
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