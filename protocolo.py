from collections import namedtuple
class Protocolo:
    def __init__(self):
        self.mensagem=namedtuple("mensagem",['cod','valor'])
    def MostrarMensagensCliente(self):
        cod=[1,3,5,5,7,9,11,13]
        valor=['x','x','x','-1','1','1','1','1']
        significado=['Pesquisar por letra (retorna todos os registros com aquela letra);','Pesquisar por nome (retorna todos os registros com aquele nome);','Seleciona o registro X','Retorna o proximo registro a partir da ultima pesquisa','Pular para próxima letra;','Apagar um registro;','Alterar um registro.','Adicionar um novo registro']
        print("-"*20+" Protocolo "+"-"*20)
        l=[]
        l.append("Escolha uma operação \n")
        for i in range(0,len(cod),1):
            l.append("cod:{}   valor:{}    significado:{}\n".format(cod[i],valor[i],significado[i]))
        return l
    def MostrarMensagensServidor(self):
        cod1=['2','2','4','4','6','6','6','8','8','10','10,12','10 ou 12 ou 14','10 ou 12 ou 14']
        valor1=['-1','x','-1','x','-2','x','-1','-1','x','0','-3','-1','-2']
        significado1=['nenhuma registro começa com essa letra','pesquisa realizada com sucesso e retornou x','pesquisa não encontrou nenhum registro com esse nome','Pesquisa realizada com sucesso e retornou x','nenhuma pesquisa anterior foi feita','Proxímo registro x','Aviso não há mais registros!','última letra do alfabeto','X corresponde aos registros da letra seguinte','Registro apagado com sucesso','Registro não encontrado nenhuma alteração','Valor erro verifique os dados digitados','Index erro verifique os espaços no envio de datagramas']
        print("-"*20+" Protocolo "+"-"*20)
        l=[]
        l.append("Escolha uma operação \n")
        for i in range(0,len(cod1),1):
            l.append("cod:{}   valor:{}    significado:{}\n".format(cod1[i],valor1[i],significado1[i]))
        return l
    def mensagem_consulta_tokens(self):
        return self.mensagem(1,-1)
    def mensagem_solicita_tokens(self):
        return self.mensagem(3,-1)
    def mensagem_devolve_tokens(self,n=1):
        return self.mensagem(5,n)
    @staticmethod
    def get(cod,valor):
        mensagem=namedtuple("mensagem",['cod','valor'])
        s=mensagem(str(cod),str(valor))
        return s