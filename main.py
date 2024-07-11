import numpy as np
import sys
import curses
import time


class Tanque():
    
    def __init__(self, tamanho, conteudo):
        self.tamanho = tamanho
        self.conteudo = conteudo 
        self._atualizar_porcentagem()
        self._atualizar_status()

    def _atualizar_porcentagem(self):
        if self.conteudo <= 0:
            self.porcentagem=0
        else:
            self.porcentagem = round((self.conteudo/self.tamanho)*100, 0)

    def _atualizar_status(self):       
        if self.porcentagem <= 80:
            self.status = 'Ok'
        elif self.porcentagem > 80:
            self.status = '!!! Acima do Limiar'

    def Encher(self, vol):
        self.conteudo += vol
        if self.conteudo > self.tamanho:
            self.conteudo = self.tamanho
        self._atualizar_porcentagem()
        self._atualizar_status()
    
    def Esvaziar(self, vol):
        self.conteudo -= vol
        if self.conteudo < 0:
            self.conteudo = 0
        self._atualizar_porcentagem()
        self._atualizar_status()


class Triangular(): # construtor da funcao pertinencia triangular

    def __init__(self, start, vertice, stop):
        self.start = start
        self.vertice= vertice
        self.stop = stop
        
            
    def CalcPert(valor):



        

def draw_tank(screen, tanque):
    screen.clear()
    height, width = screen.getmaxyx()
    box_height = height - 30
    box_width = 50
    filled_height = int(box_height * (tanque.porcentagem / 100))

    
    screen.addstr(1, 1, 'Teste')


    for i in range(box_height - filled_height):
        screen.addstr(i, 1, "|" + " " * (box_width - 2) + "|")
    for i in range(box_height - filled_height, box_height):
        screen.addstr(i, 1, "|" + "#" * (box_width - 2) + "|")
    
    screen.addstr(box_height, 1, "+" + "-" * (box_width - 2) + "+")
    screen.addstr(box_height + 1, 1, f"Capacidade = {tanque.porcentagem}% --- {tanque.status}")
    screen.refresh()



vazao_in = 15#np.random.randint(0, 15)
vazao_out = 3


def Simulacao(screen, total_time):
    curses.curs_set(0)
    screen.nodelay(1)

    tanque = Tanque(1000, 500)
    t = 0
    while t <= total_time:
        draw_tank(screen, tanque)
        tanque.Encher(vazao_in)
        tanque.Esvaziar(vazao_out)
        t += 1
        time.sleep(0.1)


curses.wrapper(Simulacao, 100)






