from src.klotz import Klotz
import random
random.seed()

import enum
class Formen(enum.Enum):
    Z = 1
    L = 2
    I = 3
    T = 4
    O = 5

class Cluster:
    def __init__(self, y, x):
        self.klotz_cluster = [Klotz(),Klotz(),Klotz(),Klotz()]
        self.y = y
        self.x = x
        self.form = None

    def get_Kloetze(self):
        return self.klotz_cluster
    
    def set_Cluster(self, kloetz_liste):
        self.klotz_cluster = kloetz_liste

    def waehleForm(self, waehl_form : Formen, isRotiert, rotation_anzahl):
        y = self.y
        x = self.x
        if waehl_form == Formen.Z:
            z = [(x,y),(x+3,y),(x+3,y+2), (x+(3)*2, y+2)]
            self.form = z
        if waehl_form == Formen.I:
            i = [(x,y), (x,y+2), (x,y+2*2), (x,y+2*3)]
            self.form = i
        if waehl_form == Formen.L:
            l = [(x,y), (x,y+2), (x,y+2*2), (x+3,y+2*2)]
            self.form = l
        if waehl_form == Formen.O:
            o = [(x,y), (x+3, y), (x,y+2), (x+3, y+2)]
            self.form = o
        if waehl_form == Formen.T:
            t = [(x,y), (x-3,y+2), (x,y+2), (x+3, y+2)]
            self.form = t
        if isRotiert == True:
            rotation_anzahl = self.rotieren(waehl_form, rotation_anzahl)
        return rotation_anzahl

    def setForm(self):
        for i in range(len(self.klotz_cluster)):
            k = self.klotz_cluster[i]
            x, y = self.form[i] # !!!
            k.setPosition(y,x)

    def drawCluster(self, stdscr_fn):
        for i in self.klotz_cluster:
            i.draw(stdscr_fn)

    def get_Seite(self, richtung : str): # von allen Klötzen im Cluster // Richtung = z.B. 'R', 'L', 'U'
        x_or_y_pos = []
        for i in self.klotz_cluster:
            if richtung == 'R':
                x_or_y_pos.append(i.get_R_Seite())
            if richtung == 'L':
                x_or_y_pos.append(i.get_L_Seite())
            if richtung == 'U':
                x_or_y_pos.append(i.getUnterseite()) # das ist [(y,x), (y,x), ...]
            if richtung == 'O':
                x_or_y_pos.append(i.get_O_Seite())  # das ist [(y,x), (y,x), ...]
        return x_or_y_pos

    def setPos(self, y, x):
        self.y = y
        self.x = x

    def kollidiert_m_Cluster(self): pass

    def rotieren(self, waehl_form : Formen, rotation_anzahl):
        y = self.y
        x = self.x
        if waehl_form == Formen.T:
            match rotation_anzahl:
                case 1:
                    t2 = [(x,y), (x-3+(2*3),y+2), (x+(1*3),y+2-(1*2)), (x+3, y+2-(2*2))]
                    self.form = t2
                case 2:
                    t3 = [(x-1*3, y-1*2),(x+0, y-1*2),(x+1*3,y-1*2),(x,y)]
                    self.form = t3
                case 3:
                    t4 = [(x-1*3,y-1*2),(x-1*3,y+0),(x-1*3,y+1*2),(x,y)]
                    self.form = t4

        if waehl_form == Formen.I:
            i2 = [(x,y), (x+(1*3),y+2-(1*2)), (x+(2*3),y+2*2-(2*2)), (x+(3*3),y+2*3-(3*2))]
            self.form = i2
            rotation_anzahl += 3

        if waehl_form == Formen.Z:
            z2 = [(x,y),(x+3-(1*3),y-(1*2)),(x+3,y+2-(2*2)), (x+3*2-(1*3), y+2-(2*3))]
            self.form = z2
            rotation_anzahl += 3

        if waehl_form == Formen.L:
            match rotation_anzahl:
                case 1:
                    l2 = [(x,y),(x+1*3,y),(x+2*3,y),(x+2*3,y-1*2)]
                    self.form = l2
                case 2:
                    l3 = [(x,y), (x+1*3,y), (x+1*3,y+1*2), (x+1*3,y+2*2)]
                    self.form = l3
                case 3:
                    l4 = [(x,y),(x+1*3,y),(x+2*3,y),(x, y-1*2)]
                    self.form = l4
                    
        return rotation_anzahl



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