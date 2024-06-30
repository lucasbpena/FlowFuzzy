import numpy as np
import sys
import time

import os

class Tanque():
    
    def __init__(self, tamanho, conteudo):
        self.tamanho = tamanho
        self.conteudo = conteudo
        self._atualizar_porcentagem() 
        self._atualizar_status() 
        
    def _atualizar_porcentagem(self): # recalcula porcentagem para cada conteudo / tamanho
        if self.conteudo <= 0:
            self.porcentagem=0
        else:
            self.porcentagem = round((self.conteudo/self.tamanho)*100, 0)

    def _atualizar_status(self):
        if self.porcentagem <= 80:
            self.status = 'Ok'
        elif self.porcentagem > 80:
            self.status = 'Acima do Limiar'
        elif self.porcentagem >= 100:
            self.status = 'OVERFLOW!'

    def Encher(self, vol):
        self.conteudo += vol
        self._atualizar_porcentagem() 
        if self.conteudo > self.tamanho:
            self.conteudo = self.tamanho
    
    def Esvaziar(self, vol):
        self.conteudo -= vol
        self._atualizar_porcentagem()
        if self.conteudo < 0:
            self.conteudo = 0
    
    def display(self):
        height = 10 
        width = 20
        water_level = int((self.porcentagem / 100) * height)
        
        tanque_art = []
        for i in range(height):
            if i < height - water_level:
                tanque_art.append('|' + ' ' * width + '|')
            else:
                tanque_art.append('|' + '#' * width + '|')
        
        tanque_art.append('+' + '-' * width + '+')
        tanque_art.append(f"Porcentagem: {self.porcentagem:.2f}%")

        return '\n'.join(tanque_art)
    
vazao_in = 5#np.random.randint(0, 15)
vazao_out = 3

def Simulacao(total_time, delay=1):
    tanque = Tanque(1000, 0) 
    t = 0
    while t <= total_time:
        vazao_in = np.random.randint(0, 15)
        tanque.Encher(vazao_in)
        tanque.Esvaziar(vazao_in)
        
        os.system('clear')
        sys.stdout.write(tanque.display() + "\n")
        #sys.stdout.flush()
        
        time.sleep(delay)
        t += 1

# Executando a simulação por 20 unidades de tempo com 1 segundo de delay entre atualizações
Simulacao(20, delay=0.5)