# Das ist der atomare Bestandteil eines Tetrisblocks
# Ein Block besteht aus zwei Zeilen, je gefüllt mit 3 Rauten
class Block:
    def __init__(self):
        self.x_pos = 0 # x-Koordinate der obersten rechten Raute
        self.y_pos = 0 # y-Koordinate der obersten rechten Raute
        self.zeilen = ['###','###'] # Der sichtbare Block besteht aus Rauten

# Jede Zeile des Blocks hat eine Länge von 3
    def get_zeilen_laenge(self):
        return 3

# Diese Funktionen geben die Koordinaten des Blocks zurück
    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos
    
    def get_pos(self):
        return self.y_pos, self.x_pos

# Diese Funktionen geben die Koordinaten der Blockseiten zurück
    def get_U_Seite(self):
        return self.y_pos+1,self.x_pos
    
    def get_R_Seite(self):
        return self.y_pos, self.x_pos+2
    
    def get_L_Seite(self):
        return self.y_pos, self.x_pos
    
    def get_O_Seite(self):
        return self.y_pos, self.x_pos

# Diese Funktionen überschreiben die Koordinaten des Blocks
    def set_pos(self, y, x):
        self.y_pos = y
        self.x_pos = x

    def set_y(self, y):
        self.y_pos = y

# Diese Funktion malt ein Block auf dem Terminalfenster
    def draw(self, stdscr_fn):
        for zeilennummer in range(len(self.zeilen)):
            zeile = self.zeilen[zeilennummer] # rows
            stdscr_fn.addstr(self.y_pos+zeilennummer, self.x_pos, zeile)