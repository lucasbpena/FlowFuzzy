import numpy as np
import sys


class Tanque():
    
    def __init__(self, tamanho, conteudo):
        self.tamanho = tamanho
        self.conteudo = conteudo 
        if conteudo == 0:
            self.porcentagem=0
        elif conteudo == 0:
            self.porcentagem=0            
        else:
            self.porcentagem = round((self.conteudo/self.tamanho)*100, 2)
        
    def Encher(self, vol):
        self.conteudo += vol
        if self.conteudo > self.tamanho:
            self.conteudo = self.tamanho
    
    def Esvaziar(self, vol):
        self.conteudo -= vol
        if self.conteudo < 0:
            self.conteudo = 0
    
    def Status(self):
        if self.porcentagem <= 80:
            status = 'OK'
        elif self.porcentagem > 80:
            status = 'Acima do Limiar'
        elif self.porcentagem > 100:
            status = 'OVERFLOW!'
        
        return status
    
    def display(self):
        barra = int(self.porcentagem / 2)  # 50 caracteres de largura para 100%
        ascii_art = f"[{'#' * barra}{'.' * (50 - barra)}] {self.porcentagem:.2f}%"
        return ascii_art
    
vazao_in = 5#np.random.randint(0, 15)


def Simulacao(total_time):
    
    tanque = Tanque(1000, 0)
    t = 0
    while t <= total_time:
           
        print(tanque.Status(), f'Capacidade = {tanque.porcentagem}%')
        tanque.display()
        tanque.Encher(vazao_in)
        t +=1



Simulacao(500)






