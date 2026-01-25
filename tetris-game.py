import os
os.system("echo \033[1;1H")
os.system("echo \033[2J")
import curses
from curses import wrapper

from src.cluster import TetrisBlock
from src.tetris_rand import Boden
from src.tetris_rand import Wand
from src.cluster import Formen
from src.cluster_fest import Tetrismauer
from src.game_interface import Game_Interface
import random
random.seed()
stdscr = curses.initscr()

class TetrisGame:
    def __init__(self):
        self.x_start = 37 # Startpunkt
        self.y_start = 0 # Startpunkt statt 0
        self.screen_width = 52 # screen_width (max 120)
        self.screen_height = 30 # screen_height (max 30)
        self.boden = Boden(self.screen_width, self.screen_height, 0)
        self.wand_L = Wand(self.screen_height, 0, 0)
        self.wand_R = Wand(self.screen_height, 0, self.screen_width)
        self.tetrismauer = Tetrismauer(self.screen_height, self.screen_width)
        self.tetris_block = TetrisBlock(self.y_start, self.x_start)
        self.zufallsform = Formen.T
        self.interface = Game_Interface()

    def main(self,stdscr):
        # Bildschirm
        stdscr.clear()
        y, x = self.y_start, self.x_start
        isRotated = False
        rotation_count = 0
        self.tetrismauer.gitter_erfassen()
        while True:
            stdscr.clear()
            
            self.boden.draw(stdscr.addstr, '=')
            self.wand_L.draw(stdscr.addstr, '|\n')
            self.wand_R.draw_Rechts(stdscr.addstr, '|')
            self.interface.print_Interface(stdscr)

            rotation_count = self.tetris_block.set_form(Formen(self.zufallsform), isRotated, rotation_count)
            self.tetris_block.draw_TetrisBlock(stdscr)

            self.tetrismauer.draw(stdscr)

            isBoden = self.boden.pruefen_ob_boden(self.tetris_block.get_Seite('U'))
            isFCluster = self.tetrismauer.kollidiert_oben(self.tetris_block.get_Seite('U')) # unbenennten: is_tetris_mauer
            isFCluster_R = self.tetrismauer.kollidiert_seitlich(self.tetris_block.get_Seite('L'), 'R')  # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L # is_tetris_mauer_R
            isFCluster_L = self.tetrismauer.kollidiert_seitlich(self.tetris_block.get_Seite('R'), 'L') # is_tetris_mauer_L
            kollidiert = False
            
            # Wenn keine Tasten gedrückt werden, dann werden sämtliche Funktionen, die nach key = stdscr.getch() kommen, gar nicht ausgeführt
            key = stdscr.getch()
            if key == ord('q'):
                break

            if self.interface.if_gameover(self.tetrismauer):
                stdscr.clear()
                self.interface.print_gameover(stdscr)
                stdscr.getch()
                break

            if key == ord('r'):
                rotation_count += 1
                if rotation_count > 3:
                    rotation_count = 0
                    isRotated = False
                else:
                    isRotated = True

            if key == curses.KEY_UP and y > 0:
                y -= 2
                self.tetris_block.set_pos(y,x)
            if key == curses.KEY_DOWN:
                if isBoden == False and isFCluster == False:
                    y += 2
                    self.tetris_block.set_pos(y,x)
                else: # Cluster haftet am Boden und kann nicht mehr bewegt werden, der Cluster wird dann von dieser Variable entfernt 
                    kollidiert = True
            
            if self.wand_R.pruefen_ob_Wand(self.tetris_block.get_Seite('R')) == False:
                if key == curses.KEY_RIGHT:
                    if isFCluster_L == False:
                        x += 3
                        self.tetris_block.set_pos(y,x)

            if self.wand_L.pruefen_ob_Wand(self.tetris_block.get_Seite('L')) == False:
                if key == curses.KEY_LEFT:
                    if isFCluster_R == False:
                        x -= 3
                        self.tetris_block.set_pos(y,x)

            if kollidiert == True:
                self.tetrismauer.immobile_t_bloecke.append(self.tetris_block)
                self.zufallsform = random.randint(1,5)
                y, x = self.y_start, self.x_start
                self.tetris_block = TetrisBlock(y, x)
                rotation_count = 0
                isRotated = False
                
                if len(self.tetrismauer.immobile_t_bloecke) > 0 :
                    self.tetrismauer.bloecke_anordnen()
                    self.tetrismauer.zeile_loeschen(self.boden)
                    self.interface.update_Punktzahl(self.tetrismauer)
            
game = TetrisGame()
curses.wrapper(game.main)