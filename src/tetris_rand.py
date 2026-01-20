# Grenze des Tetris-Spielfelds
class Tetris_Rand:
    def __init__(self, mul, y, x):
        self.x_pos = x
        self.y_pos = y
        self.mul = mul # Multiplikator
    
    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos
    
    def draw(self, stdscr_fn, symbol): # symbol = z.B. "=" oder "=\n"
        drawing = symbol * self.mul
        stdscr_fn(self.y_pos, self.x_pos, drawing)

    def draw_Rechts(self, stdscr_fn, symbol):  # symbol = z.B.  "|"
        for i in range(self.mul):
            stdscr_fn(self.y_pos+i, self.x_pos, symbol)

# Boden des Tetris-Spielfelds
class Boden(Tetris_Rand):
    def __init__(self, mul, y, x):
        super().__init__(mul, y, x)

    """Prüft, ob ein fremdes Objekt mit dem Boden kollidiert.
    :param pos_u: Unterseite des fremden Objekts"""
    def pruefen_ob_boden(self, pos_u): #  check_ifCollide_Boden
        kollidiert = False #  collide
        if isinstance(pos_u, list):
            for pos in pos_u:
                y, x = pos
                if y+1 == self.y_pos:
                    kollidiert = True
        else:
            y, x = pos_u
            if y+1 == self.y_pos:
                kollidiert = True
        return kollidiert

# Linke oder rechte Grenze des Tetris-Spielfelds
class Wand(Tetris_Rand):
    def __init__(self, mul, y, x):
        super().__init__(mul, y, x)

    """Prüft, ob ein fremdes Objekt mit der Wand kollidiert.
    :param x_pos_r_or_l: Rechte oder linke Wand des fremden Objekts """
    def pruefen_ob_Wand(self, x_pos_r_or_l : list): #  check_ifCollide_Wand
        kollidiert = False
        for pos in x_pos_r_or_l:
            y, x = pos
            if x+1 == self.x_pos:
                kollidiert = True
            if x-1 == self.x_pos:
                kollidiert = True
        return kollidiert