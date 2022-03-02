import string
import psycopg2
class Agenda:
    """ registro=
        {
            'nome':'Daniel,
            'telefone':'8893018328',
            'email':'daniellucas@alu.uern.br'
        } 
    """
    def __init__(self,id=None,registro=None):
        self.id=id
        self.registro=registro
        self.atual='a'
        self.valor=0
    #mensagem:cod:1 e valor:x
    def procurar_por_letra(self,id,letra):
        self.atual=letra.lower()
        sql="select distinct nome,email,telefone from agenda where agenda.dono_id={} and agenda.nome  like '{}%'".format(id,letra.lower())
        r=list(consultar_db(sql))
        print("Procurando letra:",letra)
        if r==[]:
             #mensagem:cod:2 e valor:-1 nenhuma correspodência
            return "2","-1"
        #mensagem:cod:2 e valor:x
        self.registro=r
        return "2",r
    #mensagem:cod:3 e valor:x
    def procurar_por_nome(self,id,nome):
        sql="select distinct nome,email,telefone from agenda where agenda.dono_id={} and agenda.nome  like '{}'".format(id,nome.lower())
        r=consultar_db(sql)
        if r==[]:
            #mensagem:cod:4 e valor:-1
            return "4","-1"
        #mensagem:cod:4 e valor:x
        self.registro=r
        return "4",r
    #mensagem:cod:5 e valor:x id do registro atual
    def retornar_proximo_registro(self,id,valor=None):
        if self.registro==None:
            return "6","-2"
        elif valor!=None:
            if int(valor)<len(self.registro) and int(valor)>-1:
                self.valor=int(valor)
                return "6",self.registro[valor]
        elif self.valor==None or self.valor+1==len(self.registro) or self.valor>=len(self.registro) or self.valor<0:
            #mensagem:cod:6 e valor:-1
            return "6","-1"
        else:
            #mensagem:cod:6 e valor:X registro
            proximo=self.valor+1
            r=self.registro[proximo]
            self.valor=proximo
            return "6",r
    #mensagem:cod:7 e valor:x letra_atual
    def pular_para_proxima_letra(self,id):
        print(self.atual)
        if self.atual==None or self.atual=='z':
            #mensagem:cod:8 e valor:-1
            return "8","-1"
        p=0
        f=False
        for i in string.ascii_lowercase:
            if f==True:
                p=i
                #mensagem:cod:8 e valor:registro
                print("Proxima letra:".format(p))
                return "8",p
            if self.atual.lower()==i:
                f=True
    #mensagem:cod:9 e valor:x id do registro
    def apagar_registro(self,id,registro):
        sql="delete from agenda where agenda.nome='{}' and agenda.telefone='{}' and agenda.email='{}' and agenda.dono_id={} returning id,nome,telefone,email;".format(registro[0],registro[1],registro[2],id)
        r=criar_tabelas(sql)
        #mensagem:cod 10 e valor:-3
        if str(r[0])==str(id) and r[1]==registro[0] and r[2]==registro[1] and r[3]==registro[2]:
            return '10','0'
        else:
            return '10','-3'
    #mensagem:cod 11 e valor:X id do registro
    def alterar_registro(self,id,registro,novo_registro):
        sql="update agenda set nome='{}' and telefone='{}' and email='{}' and dono_id={} where agenda.nome='{}' and agenda.telefone='{}' and agenda.email='{}' and agenda.dono_id={} returning id,nome,telefone,email;".format(novo_registro[0],novo_registro[1],novo_registro[2],id,registro[0],registro[1],registro[2],id)
        r=criar_tabelas(sql)
        if str(r[0])==str(id) and r[1]==registro[0] and r[2]==registro[1] and r[3]==registro[2]:
            return '12','-3'
        else:
            return '12','0'
    #mensagem:cod:13 e valor:x
    def criar_registro(self,id,registro):
        sql="insert into Agenda(dono_id,nome,telefone,email) values('{}','{}','{}','{}') on conflict do nothing returning email;".format(id,registro[0],registro[1],registro[2])
        r=inserir_na_tabela(sql)
        if r==registro[2]:
        #mensagem:cod:14 e valor:x
            return "14","0"
        else:
            return "14","-1"
#configure com os dados
def conecta_db(host='localhost',port='5432',dbname='Servidor_Agenda',user='postgres',password='123456789'):
    conexao=psycopg2.connect("host={} port={} dbname={} user={} password={}".format(host,port,dbname,user,password))
    return conexao
def criar_tabelas(sql):
    conexao=conecta_db()
    cursor=conexao.cursor()
    cursor.execute(sql)
    conexao.commit()
    conexao.close()
    return cursor
def inserir_na_tabela(sql):
    conexao = conecta_db()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql)
        conexao.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error encontrado: {}".format(error))
        conexao.rollback()
        conexao.close()
        return -1
    conexao.close()
def consultar_db(sql):
    conexao=conecta_db()
    cursor=conexao.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    registros=[]
    for item in data:
        registros.append(item)
    conexao.close()
    return registros
