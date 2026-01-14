from src.klotz import Block
import random
random.seed()

import enum
class Formen(enum.Enum):
    Z = 1
    L = 2
    I = 3
    T = 4
    O = 5

class TetrisBlock:
    def __init__(self, y, x):
        self.bloecke = [Block(),Block(),Block(),Block()] #self.klotz_cluster
        self.y = y
        self.x = x
        self.form = None

    def get_Bloecke(self): # get_Kloetze # get_Block
        return self.bloecke # self.klotz_cluster
    
    def set_TetrisBlock(self, neue_bloecke): # set_Cluster, kloetz_liste
        self.bloecke = neue_bloecke # self.klotz_cluster

    def waehle_form(self, form_auswahl : Formen, ist_rotiert, anzahl_rotationen): # waehl_Form, isRotiert, rotation_anzahl, waehle_Form
        y = self.y
        x = self.x
        if form_auswahl == Formen.Z:
            z = [(x,y),(x+3,y),(x+3,y+2), (x+(3)*2, y+2)]
            self.form = z
        if form_auswahl == Formen.I:
            i = [(x,y), (x,y+2), (x,y+2*2), (x,y+2*3)]
            self.form = i
        if form_auswahl == Formen.L:
            l = [(x,y), (x,y+2), (x,y+2*2), (x+3,y+2*2)]
            self.form = l
        if form_auswahl == Formen.O:
            o = [(x,y), (x+3, y), (x,y+2), (x+3, y+2)]
            self.form = o
        if form_auswahl == Formen.T:
            t = [(x,y), (x-3,y+2), (x,y+2), (x+3, y+2)]
            self.form = t
        if ist_rotiert == True:
            anzahl_rotationen = self.rotieren(form_auswahl, anzahl_rotationen)
        return anzahl_rotationen

    def set_form(self): #setForm
        for blockindx in range(len(self.bloecke)): # self.klotz_cluster, i
            block = self.bloecke[blockindx] # k , self.klotz_cluster[i]
            x, y = self.form[blockindx]
            block.set_pos(y,x) #  setPosition

    def draw_TetrisBlock(self, stdscr_fn): # drawCluster
        for block in self.bloecke:  # self.klotz_cluster, i
            block.draw(stdscr_fn)

    def get_Seite(self, richtung : str): # von allen Klötzen im Cluster // Richtung = z.B. 'R', 'L', 'U', 'O'
        x_oder_y_pos = [] # 
        for block in self.bloecke: # i, self.klotz_cluster
            if richtung == 'R':
                x_oder_y_pos.append(block.get_R_Seite())
            if richtung == 'L':
                x_oder_y_pos.append(block.get_L_Seite())
            if richtung == 'U':
                x_oder_y_pos.append(block.get_U_Seite()) # das ist [(y,x), (y,x), ...] # get_Unterseite
            if richtung == 'O':
                x_oder_y_pos.append(block.get_O_Seite())  # das ist [(y,x), (y,x), ...]
        return x_oder_y_pos

    def set_pos(self, y, x): # setPos
        self.y = y
        self.x = x

    def kollidiert_m_Cluster(self): pass

    def rotieren(self, form_auswahl : Formen, anzahl_rotationen): # waehl_form, rotation_anzahl
        y = self.y
        x = self.x
        if form_auswahl == Formen.T:
            match anzahl_rotationen:
                case 1:
                    t2 = [(x,y), (x-3+(2*3),y+2), (x+(1*3),y+2-(1*2)), (x+3, y+2-(2*2))]
                    self.form = t2
                case 2:
                    t3 = [(x-1*3, y-1*2),(x+0, y-1*2),(x+1*3,y-1*2),(x,y)]
                    self.form = t3
                case 3:
                    t4 = [(x-1*3,y-1*2),(x-1*3,y+0),(x-1*3,y+1*2),(x,y)]
                    self.form = t4

        if form_auswahl == Formen.I:
            i2 = [(x,y), (x+(1*3),y+2-(1*2)), (x+(2*3),y+2*2-(2*2)), (x+(3*3),y+2*3-(3*2))]
            self.form = i2
            anzahl_rotationen += 3

        if form_auswahl == Formen.Z:
            z2 = [(x,y),(x+3-(1*3),y-(1*2)),(x+3,y+2-(2*2)), (x+3*2-(1*3), y+2-(2*3))]
            self.form = z2
            anzahl_rotationen += 3

        if form_auswahl == Formen.L:
            match anzahl_rotationen:
                case 1:
                    l2 = [(x,y),(x+1*3,y),(x+2*3,y),(x+2*3,y-1*2)]
                    self.form = l2
                case 2:
                    l3 = [(x,y), (x+1*3,y), (x+1*3,y+1*2), (x+1*3,y+2*2)]
                    self.form = l3
                case 3:
                    l4 = [(x,y),(x+1*3,y),(x+2*3,y),(x, y-1*2)]
                    self.form = l4
                    
        return anzahl_rotationen



'''
T:
         (x,y)
(x-3,y+2)(x,y+2)(x+3, y+2)

T3:
(x-1*3, y+)(x+0, y-1*2)(x+1*3,y-1*2)
             (x,y)
T4:
(x-1*3,y-1*2)
(x-1*3,y+0)  (x,y)
(x-1*3,y+1*2)

I:
(x,y)
(x,y+2)
(x,(y+2*2)
(x,(y+2*3)

L:
(x,y)
(x,y+2)
(x,(y+2*2)(x+3,(y+2*2)

L3:
(x,y)(x+1*3,y)
     (x+1*3,y+1*2)
     (x+1*3,y+2*2)

L2:
                  (x+2*3,y-3*2)
(x,y)(x+1*3,y-1*2)(x+2*3,y-2*2)

L4:
(x,y)(x+1*3,y)(x+2*3,y)
(x, y-1*2)

O:
(x,y)(x+3, y)
(x,y+2)(x+3, y+2)
'''