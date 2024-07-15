import numpy as np
import sys
import curses
import time
import random


class Tanque():
    
    def __init__(self, tamanho, volume):
        self.tamanho = tamanho
        self.volume = volume 
        self._atualizar_porcentagem()
        self._atualizar_status()

    def _atualizar_porcentagem(self):
        if self.volume <= 0:
            self.porcentagem=0
        else:
            self.porcentagem = round((self.volume/self.tamanho)*100, 0)

    def _atualizar_status(self):       
        if int(self.porcentagem) == 0:
            self.status = 'Vazio'
        elif self.porcentagem <= 80:
            self.status = 'Ok'
        elif self.porcentagem > 80:
            self.status = '!!! Acima do limiar'

    def Encher(self, vol):
        self.volume += vol
        if self.volume > self.tamanho:
            self.volume = self.tamanho
        self._atualizar_porcentagem()
        self._atualizar_status()
    
    def Esvaziar(self, vol):
        self.volume -= vol
        if self.volume < 0:
            self.volume = 0
        self._atualizar_porcentagem()
        self._atualizar_status()

class OutputTS():

    def __init__(self):
        
        self.wabs_flow = 0.5
        self.wabs_vol = 0.05
        self.n_rules = 3
        self.rule_counter = 0
        self.operators = ['e', 'ou']
        self.rule_operators = {}
        self.rule_activations = {}
        self.rule_words = {}
        self.rule_functions = {}
        self.rule_weights = {}
    
    def PertFlow(self, x_in):
        pert_dict = {}

        if x_in <= 3:
            pert_dict['baixa'] = 1
            pert_dict['media'] = 0
            pert_dict['alta'] = 0
        
        elif 3 < x_in < 7.5 :
            pert_dict['baixa'] = (6-x_in)/(6-3)
            pert_dict['media'] = (3-x_in)/(7.5-3)
            pert_dict['alta'] = 0
        
        elif x_in == 7.5:
            pert_dict['baixa'] = 0
            pert_dict['media'] = 1
            pert_dict['alta'] = 0

        elif 7.5 < x_in < 12:
            pert_dict['baixa'] = 0
            pert_dict['media'] = (12-x_in)/(12-7.5)
            pert_dict['alta'] = (x_in-9)/(12-9)
        
        elif 12 <= x_in:
            pert_dict['baixa'] = 0
            pert_dict['media'] = 0
            pert_dict['alta'] = 1
        
        self.pert_flow = pert_dict
        self.words_flow = list(pert_dict.keys())
        

    def PertVolume(self, x_in):
        pert_dict = {}

        if x_in <= 20:
            pert_dict['vazio'] = 1
            pert_dict['ocupado'] = 0
            pert_dict['cheio'] = 0
        
        elif 20 < x_in <= 40 :
            pert_dict['vazio'] = (40-x_in)/(40-20)
            pert_dict['ocupado'] = (50-x_in)/(50-20)
            pert_dict['cheio'] = 0
        
        elif 40 < x_in < 50 :
            pert_dict['vazio'] = (40-x_in)/(40-20)
            pert_dict['ocupado'] = (50-x_in)/(50-20)
            pert_dict['cheio'] = 0
        
        elif x_in == 50:
            pert_dict['vazio'] = 0
            pert_dict['ocupado'] = 1
            pert_dict['cheio'] = 0

        elif 50 < x_in <= 60:
            pert_dict['vazio'] = 0
            pert_dict['ocupado'] = (80-x_in)/(80-50)
            pert_dict['cheio'] = (x_in-60)/(80-60)
        
        elif 60 < x_in < 80:
            pert_dict['vazio'] = 0
            pert_dict['ocupado'] = (80-x_in)/(80-50)
            pert_dict['cheio'] = (x_in-60)/(80-60)
        
        elif 80 <= x_in:
            pert_dict['vazio'] = 0
            pert_dict['ocupado'] = 0
            pert_dict['cheio'] = 1

        self.pert_vol =  pert_dict
        self.words_vol = list(pert_dict.keys())
        
    def BuildRules(self):
        for n in range(self.n_rules):
            r = np.random.randint(0,2)
            
            a1 = np.random.randint(0,3)
            a2 = np.random.randint(0,3)

            weight_flow = round(np.random.uniform(-self.wabs_flow, self.wabs_flow),2)
            weight_vol = round(np.random.uniform(-self.wabs_vol, self.wabs_vol), 2)

            rules_str = f'{self.rule_counter} Se flow_in é {self.words_flow[a1]} {self.operators[r]} volume é {self.words_vol[a1]}' 
            
            self.rule_words[rules_str] = [self.words_flow[a1], self.words_vol[a2]]

            if self.operators[r] == 'e':
                self.rule_activations[rules_str] = round(min(self.pert_flow[self.words_flow[a1]], self.pert_vol[self.words_vol[a2]]), 2)
                self.rule_operators[rules_str] = 'e' 
            elif self.operators[r] == 'ou':
                self.rule_activations[rules_str] = round(max(self.pert_flow[self.words_flow[a1]], self.pert_vol[self.words_vol[a2]]), 2)
                self.rule_operators[rules_str] = 'ou'

            self.rule_weights[rules_str] = [weight_flow, weight_vol]
            self.rule_counter += 1
    
    def CustomRule(self, word1, word2, operator, weight1, weight2):
        rules_str = f'{self.rule_counter} Se flow_in é {word1} {operator} volume é {word2}' 
        self.rule_operators[rules_str] = 'e' 
        self.rule_words[rules_str] = [word1, word2]
        self.rule_weights[rules_str] = [weight1, weight2]
        self.rule_activations[rules_str] = round(min(self.pert_flow[word1], self.pert_vol[word2]), 2)
        self.rule_counter += 1


    def CalculateOutput(self, x1, x2):
        self.consequents = {}

        for rule in self.rule_activations:
            if self.rule_operators[rule] == 'e':
                self.rule_activations[rule] = round(min(self.pert_flow[self.rule_words[rule][0]], self.pert_vol[self.rule_words[rule][1]]), 2)
            elif self.rule_operators[rule] == 'ou':
                self.rule_activations[rule] = round(max(self.pert_flow[self.rule_words[rule][0]], self.pert_vol[self.rule_words[rule][1]]), 2)
                
            self.consequents[rule] = self.rule_activations[rule] * (self.rule_weights[rule][0]*x1 + self.rule_weights[rule][1]*x2)

        activations = list(self.rule_activations.values())
        consequents = list(self.consequents.values())
        
        try:
            res = sum(consequents)/sum(activations)
        except:
            res = 0

        return res
                             

def display(tanque, tsk, screen, tempo, flow_in, flow_out, out):
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
    
    # Falling water animation
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

    # Draw canos
    screen.addstr(1, 1, "=" * 4 + f"{fall_w}", PAR_CAIXA | curses.A_BOLD)
    screen.addstr(1, 5, fall_w, PAR_AGUA | curses.A_BOLD)
    screen.addstr(box_height+1, box_width+2, f"=" * 4, PAR_CAIXA | curses.A_BOLD)
    screen.addstr(box_height+1, box_width+6, fall_w *5, PAR_AGUA | curses.A_BOLD)
    
    # Draw overflow
    if filled_height < 2:
        for i in range(box_width-2):
            screen.addstr(box_height+1, i+3, '_', PAR_OVERFLOW | curses.A_BOLD)
    for i in range(box_height+2):
        screen.addstr(i, 5, fall_w, PAR_AGUA | curses.A_BOLD)
    
    # Draw info
    screen.addstr(0, 0, f'Flow in = {int(flow_in)} L/s', curses.A_BOLD)
    screen.addstr(box_height+2, box_width+3, f'Flow out = {int(flow_out)} L/s (Ajuste = {out})', curses.A_BOLD)
    screen.addstr(box_height + 4, 1, f"Time = {tempo} s", curses.A_BOLD)
    if tanque.status=='Ok':
        screen.addstr(box_height + 5, 1, f"Volume =  {int(tanque.volume)} L ({tanque.porcentagem}%) {tanque.status}", PAR_OK | curses.A_BOLD)
    else:
        screen.addstr(box_height + 5, 1, f"Volume =  {int(tanque.volume)} L ({tanque.porcentagem}%) {tanque.status}", PAR_ERROR | curses.A_BOLD)

    for n,rule in enumerate(tsk.rule_activations):
        screen.addstr(box_height + 7 + n, 4, f"{rule} | Activation = [{tsk.rule_activations[rule]}] Weights = {tsk.rule_weights[rule]}")

    
    
    screen.refresh()




def Simulacao(screen, total_time):
    curses.curs_set(0)
    screen.nodelay(1)

    init_volume = 100
    flow_out = np.random.randint(0, 15)
    
    flow_in = np.random.randint(0, 15)
    
    tanque = Tanque(init_volume, 0)
    
    tsk = OutputTS()
    tsk.PertFlow(flow_in)
    tsk.PertVolume(init_volume)
    tsk.CustomRule('alta', 'cheio', 'ou', 0.2, 0.05)
    tsk.CustomRule('baixa', 'vazio', 'ou', -0.1, -0.01)
    
    t = 0
    out=0
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

        display(tanque, tsk, screen, t, flow_in, flow_out, out)
        tanque.Esvaziar(flow_out)
        tanque.Encher(flow_in)
        tsk.PertFlow(flow_in)
        tsk.PertVolume(tanque.volume)
        out = round(tsk.CalculateOutput(flow_in, tanque.volume), 2)

        flow_out += out
        if flow_out >15:
            flow_out = 15
        elif flow_out < 0:
            flow_out = 0


        t += 1
        time.sleep(0.5)


curses.wrapper(Simulacao, 100)






