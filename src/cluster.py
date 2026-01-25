from src.klotz import Block
import random
random.seed()

# Die fünf möglichen Formen eines Tetris-Blocks
import enum
class Formen(enum.Enum):
    Z = 1
    L = 2
    I = 3
    T = 4
    O = 5

# Jeder Tetris-Block besteht aus mehreren Blöcken, die gemeinsam eine bestimmte Form bilden.
class TetrisBlock:
    def __init__(self, y, x):
        self.bloecke = [Block(),Block(),Block(),Block()]
        self.y = y  # x-Koordinate des obersten rechten Blockes
        self.x = x # y-Koordinate des obersten rechten Blockes
        self.form = None

    # Getter-Funktionen
    """
    Gibt alle Blöcke einer Instanz der Klasse TetrisBlock zurück.
    return: Liste von Block-Objekten """
    def get_Bloecke(self):
        return self.bloecke
    
    """
    Diese Funktion speichert von jedem Block des Tetris-Blocks nur eine ausgewählte Seite.
    param richtung: Die ausgewählte Seite des Blocks; 'R' = rechts, 'L' = links, 'U' = unten, 'O' = oben
    return: Eine Liste von Koordinaten der ausgewählten Seiten mehrerer Blöcke, z.B. links = [(y,x), (y,x), ...]. """
    def get_Seite(self, richtung : str):
        pos_seite = []
        for block in self.bloecke:
            if richtung == 'R':
                pos_seite.append(block.get_R_Seite())
            if richtung == 'L':
                pos_seite.append(block.get_L_Seite())
            if richtung == 'U':
                pos_seite.append(block.get_U_Seite())
            if richtung == 'O':
                pos_seite.append(block.get_O_Seite())
        return pos_seite
    
    # Setter-Funktionen

    # Diese Funktion ordnet einem Tetris-Block eine Liste neuer Blöcke zu, die möglicherweise andere Koordinaten besitzen.
    def set_TetrisBlock(self, neue_bloecke : list):
        self.bloecke = neue_bloecke

    # Diese Funktion verändert die Koordinaten des Tetris-Blocks
    def set_pos(self, y, x):
        self.y = y
        self.x = x

    """
    Wählt eine bestimmte Form für den Tetris-Block aus, berücksichtigt Rotationen
    und passt die Koordinaten der Blöcke an die neue Form an.

    :param form_auswahl: Ausgewählte Form (Formen-Enum)
    :param ist_rotiert: Gibt an, ob der Tetris-Block rotiert wurde (bool)
    :param anzahl_rotationen: Anzahl der bisherigen Rotationen (int)
    :return: Aktuelle Anzahl der Rotationen (int)
    """
    def set_form(self, form_auswahl : Formen, ist_rotiert, anzahl_rotationen):
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
        self.__update_block_pos()
        return anzahl_rotationen

    # Nachdem der Tetris-Block eine Form erhalten hat, müssen die Koordinaten der einzelnen Blöcke im Tetris-Block angepasst werden.
    def __update_block_pos(self):
        for blockindx in range(len(self.bloecke)):
            block = self.bloecke[blockindx]
            x, y = self.form[blockindx]
            block.set_pos(y,x)

    # Zeichnet einen Tetris-Block auf dem Bildschirm
    def draw_TetrisBlock(self, stdscr_fn):
        for block in self.bloecke:
            block.draw(stdscr_fn)

    """
    Passt die Form des Tetris-Blockes nach einer Rotation erneuert an.
    return: Aktuelle Anzahl der Rotationen """
    def rotieren(self, form_auswahl : Formen, anzahl_rotationen):
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

        self.__update_block_pos()
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