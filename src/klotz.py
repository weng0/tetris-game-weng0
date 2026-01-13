class Block:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.zeilen = ['###','###']

    def get_zeilen_laenge(self):
        return 3

    def set_y(self, y):
        self.y_pos = y

    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos

    def get_U_Seite(self):
        return self.y_pos+1,self.x_pos
    
    def get_R_Seite(self):
        return self.y_pos, self.x_pos+2
    
    def get_L_Seite(self):
        return self.y_pos, self.x_pos
    
    def get_O_Seite(self):
        return self.y_pos, self.x_pos

    def set_pos(self, y, x):
        self.y_pos = y
        self.x_pos = x

    def get_pos(self):
        return self.y_pos, self.x_pos
    
    def draw(self, stdscr_fn):
        for zeilennummr in range(len(self.zeilen)):
            zeile = self.rows[zeilennummr]
            stdscr_fn.addstr(self.y_pos+zeilennummr, self.x_pos, zeile)