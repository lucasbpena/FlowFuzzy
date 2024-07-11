import numpy as np
import sys


class Tanque():
    
    def __init__(self, tamanho, conteudo):
        self.tamanho = tamanho
        self.conteudo = conteudo 
        
    def Encher(self, vol):
        self.conteudo += vol
        if self.conteudo > self.tamanho:
            self.conteudo = self.tamanho
    
    def Esvaziar(self, vol):
        self.conteudo -= vol
        if self.conteudo < 0:
            self.conteudo = 0

    def Status(self):
        if self.conteudo <= 0:
            porcentagem=0
        else:
            porcentagem = round((self.conteudo/self.tamanho)*100, 1)
        
        if porcentagem <= 80:
            status = 'OK'
        elif porcentagem > 80:
            status = 'Acima do Limiar'
        elif porcentagem > 100:
            status = 'OVERFLOW!'
        
        
        return porcentagem, status
    
vazao_in = 5#np.random.randint(0, 15)
vazao_out = 3

def Simulacao(total_time):
    
    tanque = Tanque(1000, 50)
    t = 0
    while t <= total_time:
           
        porcentagem, status = tanque.Status()
        print(f'Capacidade = {porcentagem}% --- {status}')
        tanque.Encher(vazao_in)
        tanque.Esvaziar(vazao_out)
        t +=1



Simulacao(500)







