from multiprocessing.sharedctypes import Value
import socket
import threading
from utills import *
from protocolo import *
import sys
class Servidor:
    def __init__(self,host='localhost',port=50000):
        self.soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soquete.bind((host,port))
        self.protocolo=Protocolo()
        self.running=False
    def start(self):
        self.running=True
        try:
            while self.running==True:
                self.soquete.listen()
                print("Esperando conexão com o cliente")
                conn,ender=self.soquete.accept()
                print("Conectando em:",ender)
                novo_thread = threading.Thread(target=self.manipula, args=(conn,ender))
                novo_thread.start()
        except KeyboardInterrupt:
            print("Desligando o servidor.")
            return False
    def envia_mensagem(self,conn=None,ender=None,mensagem='Servidor processando'):
        conn.sendall(str.encode(mensagem))
    def manipula(self, conn, ender):
        aviso_login="Realize o sign in com seu login e senha,\nCaso não possua um login, Cadastre-se: Enviando um login e senha.\nlogin: senha:"
        aviso_welcome="Opções de respostas para cliente:\n".join(self.protocolo.MostrarMensagensCliente())
        aviso_servidor="Protocolo do servidor:\n".join(self.protocolo.MostrarMensagensServidor())
        self.envia_mensagem(conn,ender,aviso_login)
        id=self.verificar_login(conn,ender)
        if id=='-1':
            return 0
        self.agenda=Agenda(id)
        self.envia_mensagem(conn,ender,aviso_servidor)
        while True:
            try:
                self.envia_mensagem(conn,ender,aviso_welcome)
                data=conn.recv(1024).decode('utf-8')
                print("Esperando cliente entradas")
                print(conn,ender)
                if not data:
                    print("Conexão fechando.")
                    conn.close()
                    break
                m=data.split()
                p=Protocolo.get(m[0],m[1])
                d=self.recebe_msg(id,p,conn,ender)
                s=self.formatar_msg(d[1])
                print(s)     
                self.envia_mensagem(conn,ender,"cod:"+d[0]+" valor:\n"+s)
                print("Enviou mensagem")
            except KeyboardInterrupt:
                print("entrou na encerração")
                self.running=False
                return False
    def formatar_msg(self,msg):
        string=""
        print(msg)
        if msg==[]:
            return '-1'
        try:
            for tupla in msg:
                print("mensagem:",tupla)
                m=[]
                for item in tupla:
                    print("items:",item)
                    m.append(item)
                string=string+"nome:"+m[0]+" telefone:"+m[1]+" email:"+m[2]+"\n"
        except IndexError:
            return '-1'
        return string
    def verificar_registro(self,conn,ender,mensagem):
        try:
            self.envia_mensagem(conn,ender,mensagem)
            nome,telefone,email=conn.recv(1024).decode('utf-8').split()
            return nome,telefone,email
        except ValueError:
            return '-1'
        except IndexError:
            return '-2'
    def verificar_login(self,conn,ender):
        while True:
            c="Envie o login e a senha no formato login senha"
            self.envia_mensagem(conn,ender,c)
            login,senha=conn.recv(1024).decode('utf-8').split()
            print("recebeu os dados")
            s="select usuário_id from Usuário where usuário.login= '"+login+"' and usuário.senha='"+senha+"'"
            r=consultar_db(s)
            try:
                user=r[0][0]
                self.envia_mensagem(conn,ender,"Login realizado com sucesso, bem vindo {} \n".format(login.split('@')[0]))
                return user
            except IndexError: 
                self.envia_mensagem(conn,ender,"Usuário não reconhecido, deseja criar um cadastro com os mesmo dados? 1 ou 0 ou sair")
                op=conn.recv(1024).decode('utf-8')
                if op=='1':
                    novo_user="insert into Usuário(login,senha) values('{}','{}') on conflict do nothing;".format(login,senha)
                    inserir_na_tabela(novo_user)
                    self.envia_mensagem(conn,ender,"Login realizado com sucesso, bem vindo {}".format(login.split('@')[0]))
                    return consultar_db(s)[0][0]
                elif op=='0':
                    self.envia_mensagem(conn,ender,"Verifique seu usuário e senha e tente logar de novo.")
                elif op=='sair':
                    return -1
                else:
                    self.envia_mensagem(conn,ender,"Opção invalida")
    def recebe_msg(self,id,mensagem,conn,ender):
        cod=mensagem.cod
        valor=mensagem.valor
        print("cod:",cod," valor:",valor)
        if cod=='1' and valor in string.ascii_lowercase:
            return self.agenda.procurar_por_letra(id,valor)
        elif cod=='3' and type(valor)==str and valor.isnumeric()==False:
            return self.agenda.procurar_por_nome(id,valor)
        elif cod=='5' and valor.isnumeric()==True:
            if valor=='-1':
                return self.agenda.retornar_proximo_registro(id)
            else:
                return self.agenda.retornar_proximo_registro(id,valor)
        elif cod=='7' and valor=='1':
            letra=self.agenda.pular_para_proxima_letra(id)
            if letra[1]=='-1':
                return '8','-1'
            _,r=self.agenda.procurar_por_letra(id,letra[1])
            self.envia_mensagem(conn,ender,"Você está agora na letra:{} e foram encontrados:{} registros\n".format(self.agenda.atual,len(r)))
            return '8',r
        elif cod=='9' and valor=='1':
            registro=self.verificar_registro(conn,ender,"Envie o nome telefone email no formato nome telefone email do registro que deseja excluir:\n")
            if registro=="-1" or registro=="-2":
                return '10',registro
            return self.agenda.apagar_registro(id,registro)
        elif cod=='11' and valor=='1':
            registro=self.verificar_registro(conn,ender,"Envie o antigo nome,telefone e email do registro antigo:\n")
            novo_registro=self.verificar_registro(conn,ender,"Agora envie o novo nome,telefone,email do arquivo:\n")
            r=self.agenda.alterar_registro(id,registro,novo_registro)
            if r[1]=='0':
                self.envia_mensagem(conn,ender,"Registro modificado com sucesso!")
            elif r[1]=='3':
                self.envia_mensagem(conn,ender,"Registro não modificado porque não existe nenhum registro similar a esse. Verifique os dados e tente de novo!\n")
            return r
        elif cod=='13' and valor=='1':
            registro=self.verificar_registro(conn,ender,"Digite o nome,telefone e email do registo que deseja adicionar:\n")
            return self.agenda.criar_registro(id,registro)

def main(parametro=None):
    #Crie a database Servidor_Agenda no postgres
    try:
        if parametro==None or parametro==[]:
            print("Carregando configurações padrões")
        elif len(parametro)==5:
            global dados
            dados=parametro
            conecta_db=lambda dados=dados:psycopg2.connect(host=dados[0],port=dados[1],dbname=dados[2],user=dados[3],password=dados[4])
    except IndexError:
        print("Houve um erro, usando configurações padrões.")
    #drop_agenda="drop table Agenda cascade;"
    #drop_usuario="drop table Usuário cascade;"
    tabela_usuario="create table if not exists Usuário (usuário_id serial primary key,login varchar(100) unique not null,senha varchar(10) not null)"
    tabela_agenda="create table if not exists Agenda (dono_id integer,nome varchar(100),telefone varchar(14),email varchar(100),foreign key(dono_id) references Usuário(usuário_id))"
    #criar_tabelas(drop_agenda)
    #criar_tabelas(drop_usuario)
    criar_tabelas(tabela_usuario)
    criar_tabelas(tabela_agenda)
    inserir_em_usuario="insert into Usuário(login,senha) values('daniel_silva','123'),('lucas_silva','321') on conflict do nothing;"
    inserir_em_agenda="insert into Agenda(dono_id,nome,telefone,email) values('1','misaki','88993018328','misaki@gmail.com'),('1','daniel','88993288301','daniel.icapui@hotmail.com'),('2','ana','88930909030','ana@gmail.com'),('2','sakura','41992438750','sakura@hotmail.com') on conflict do nothing;"
    inserir_em_agenda2="insert into Agenda(dono_id,nome,telefone,email) values('2','angela','3992438751','angela@hotmail.com'),('2','bela','8893022324','bela@hotmail.com'),('2','beatriz','88991018191','beatriz@gmail.com') on conflict do nothing;"
    inserir_na_tabela(inserir_em_usuario)
    inserir_na_tabela(inserir_em_agenda)
    inserir_na_tabela(inserir_em_agenda2)
    servidor=Servidor()
    servidor.start()
if __name__=='__main__':
    sys.argv.pop(0)
    main(sys.argv)