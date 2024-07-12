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
        if int(self.porcentagem) == 0:
            self.status = 'Vazio'
        elif self.porcentagem <= 80:
            self.status = 'Ok'
        elif self.porcentagem > 80:
            self.status = '!!! Acima do limiar'

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


def PertFlowIn(x_in):

    pert_dict = {'baixo', 'medio' , 'alto'}

    if x_in <= 3:
        pert_dict['baixo'] = 1
        pert_dict['medio'] = 0
        pert_dict['alto'] = 0
    
    elif 3 < x_in < 7.5 :
        pert_dict['baixo'] = 1
        pert_dict['medio'] = 0
        pert_dict['alto'] = 0
    
    elif x_in == 7.5:
        pert_dict['baixo'] = 1
        pert_dict['medio'] = 0
        pert_dict['alto'] = 0

    elif 7.5 < x_in < 12:
        pert_dict['baixo'] = 0
        pert_dict['medio'] = 0
        pert_dict['alto'] = 0
    
    elif 12 <= x_in:
        pert_dict['baixo'] = 0
        pert_dict['medio'] = 0
        pert_dict['alto'] = 1

    return pert_dict

def PertVolume(x_vol):
    
    pert_dict = {'vazio', 'ocupado' , 'cheio'}

    if x_vol <= 20:
        pert_dict['vazio'] = 1
        pert_dict['ocupado'] = 0
        pert_dict['cheio'] = 0
    
    elif 20 < x_vol < 7.5 :
        pert_dict['vazio'] = 1
        pert_dict['ocupado'] = 0
        pert_dict['cheio'] = 0
    
    elif x_vol == 7.5:
        pert_dict['vazio'] = 1
        pert_dict['ocupado'] = 0
        pert_dict['cheio'] = 0

    elif 7.5 < x_vol < 12:
        pert_dict['vazio'] = 0
        pert_dict['ocupado'] = 0
        pert_dict['cheio'] = 0
    
    elif 12 <= x_vol:
        pert_dict['vazio'] = 0
        pert_dict['ocupado'] = 0
        pert_dict['cheio'] = 1

    return pert_dict

    return pert_dict


def PertControler(pert_in, pert_vol):

    if pert_in > 0 and pert_vol > 2:
        pass
       

def display(screen, tanque, tempo, flow_in, flow_out):
    screen.clear()

    # Cores
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

    PAR_AGUA = curses.color_pair(2)
    PAR_OVERFLOW = curses.color_pair(3)
    PAR_CAIXA = curses.color_pair(4)
    PAR_OK = curses.color_pair(5)
    PAR_ERROR = curses.color_pair(6)

    # Gera arte da caixa
    height, width = screen.getmaxyx()
    box_height = height - 15
    box_width = 40
    filled_height = int(box_height * (tanque.porcentagem / 100))
    
    if tempo % 2 == 0:
        fall_w = '-'
    else:
        fall_w = '~'

    # Draw the empty part of the tank
    for i in range(box_height - filled_height):
        screen.addstr(i+3, 2, "|", PAR_CAIXA | curses.A_BOLD)
        screen.addstr(i+3, 3, " " * (box_width - 2), PAR_CAIXA | curses.A_BOLD)
        screen.addstr(i+3, box_width + 1, "|", PAR_CAIXA | curses.A_BOLD)

    # Draw the filled part of the tank
    for i in range(box_height - filled_height, box_height):
        screen.addstr(i + 3, 2, "|", PAR_CAIXA | curses.A_BOLD)
        for j in range(1, box_width - 1):
            screen.addstr(i + 3, 2 + j, f"{fall_w}", PAR_AGUA | curses.A_BOLD)
        screen.addstr(i + 3, box_width + 1, "|", PAR_CAIXA | curses.A_BOLD)

    # Draw the bottom of the tank
    screen.addstr(box_height + 2, 2, "+", PAR_CAIXA | curses.A_BOLD)
    screen.addstr(box_height + 2, 3, "-" * (box_width - 2), PAR_CAIXA | curses.A_BOLD)
    screen.addstr(box_height + 2, box_width + 1, "+", PAR_CAIXA | curses.A_BOLD)

    # Canos
    screen.addstr(1, 1, "=" * 4 + f"{fall_w}", PAR_CAIXA | curses.A_BOLD)
    screen.addstr(1, 5, fall_w, PAR_AGUA | curses.A_BOLD)
    screen.addstr(box_height+1, box_width+2, f"=" * 4, PAR_CAIXA | curses.A_BOLD)
    screen.addstr(box_height+1, box_width+6, fall_w *5, PAR_AGUA | curses.A_BOLD)
    
    # Overflow
    if filled_height < 2:
        for i in range(box_width-2):
            screen.addstr(box_height+1, i+3, '_', PAR_OVERFLOW | curses.A_BOLD)
    for i in range(10):
        screen.addstr(i, 5, fall_w, PAR_AGUA | curses.A_BOLD)
    
    # Info
    screen.addstr(0, 0, f'Flow in = {int(flow_in)} L/s', curses.A_BOLD)
    screen.addstr(box_height+2, box_width+3, f'Flow out = {int(flow_out)} L/s', curses.A_BOLD)
    screen.addstr(box_height + 4, 1, f"Time = {tempo} s", curses.A_BOLD)
    if tanque.status=='Ok':
        screen.addstr(box_height + 5, 1, f"Volume =  {int(tanque.conteudo)} L ({tanque.porcentagem}%) {tanque.status}", PAR_OK | curses.A_BOLD)
    else:
        screen.addstr(box_height + 5, 1, f"Volume =  {int(tanque.conteudo)} L ({tanque.porcentagem}%) {tanque.status}", PAR_ERROR | curses.A_BOLD)
    
    
    screen.refresh()

    
def Simulacao(screen, total_time):
    curses.curs_set(0)
    screen.nodelay(1)

    flow_out = 2
    flow_in = np.random.randint(0, 15)
    tanque = Tanque(100, 0)
    t = 0
    counter=0
    while True:
        if t % 100 == 0:
            flow_in_update = np.random.randint(0, 15)    
            counter = flow_in - flow_in_update

        if counter >= 0.1:
            flow_in -=0.1
            counter -=0.1
        elif counter <= -0.1:
            flow_in +=0.1
            counter +=0.1

        display(screen, tanque, t, flow_in, flow_out)
        tanque.Esvaziar(flow_out)
        tanque.Encher(flow_in)
        
        t += 1
        time.sleep(0.1)


curses.wrapper(Simulacao, 100)






