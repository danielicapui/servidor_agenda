#!/usr/bin/env python3
import socket
import threading
from protocolo import Protocolo
class Cliente:
    def __init__(self,host='127.0.0.1',port=50000,id=None):
        self.soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host=host
        self.port=port
        self.token=False
        self.soquete.connect((self.host,self.port))
        self.id=id
    def recebe_mensagem(self):
        self.soquete.settimeout(7)
        while True:
            try:
                mensagem=self.soquete.recv(1024).decode('UTF-8')
                print(mensagem)
            except socket.timeout:
                print("Fim de mensagens")
                break
    def envia_mensagem(self,mensagem=None):
        mensagem=input("Digite a mensagem para enviar:") or input()
        self.soquete.sendall(str.encode(mensagem))
def main():
    #port=int(input("Digite a porta do servidor:"))
    #host=input("Digite o ip:")
    cliente=Cliente()
    try:
        while True:
            cliente.recebe_mensagem()
            cliente.envia_mensagem()
    except KeyboardInterrupt:
        op=input("Deseja interrompe o cliente?:s/n")
        if 's'==op:
            cliente.socket.close()
    return 0
if __name__=='__main__':
        main()