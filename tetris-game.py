import os
os.system("echo \033[1;1H")
os.system("echo \033[2J")
import curses
from curses import wrapper
# from src.klotz import Klotz
from src.cluster import Cluster
from src.tetris_rand import Boden
from src.tetris_rand import Wand
from src.cluster import Formen
from src.cluster_fest import ClusterFest
from src.game_interface import Game_Interface
import random
random.seed()
stdscr = curses.initscr()

class TetrisGame:
    def __init__(self):
        self.x_start = 37 # Startpunkt
        self.y_start = 6 # Startpunkt statt 0
        self.screen_width = 52 # screen_width (max 120) original: 119
        self.screen_height = 30 # screen_height (max 30)
        self.boden = Boden(self.screen_width, self.screen_height, 0)
        self.wand_L = Wand(self.screen_height, 0, 0)
        self.wand_R = Wand(self.screen_height, 0, self.screen_width) # 119
        self.feste_clusters = ClusterFest(self.screen_height, self.screen_width)
        self.cluster = Cluster(self.y_start, self.x_start)
        self.zufallsform = Formen.T
        self.interface = Game_Interface()

    def main(self,stdscr):
        # Bildschirm
        stdscr.clear()
        # screen_height, screen_width = stdscr.getmaxyx() // not used
        y, x = self.y_start, self.x_start
        isRotated = False
        rotation_count = 0
        self.feste_clusters.koordinatensystem()
        while True:
            stdscr.clear()
            
            self.boden.draw(stdscr.addstr, '=')
            self.wand_L.draw(stdscr.addstr, '|\n')
            self.wand_R.draw_Rechts(stdscr.addstr, '|')
            self.interface.print_Interface(stdscr)

            rotation_count = self.cluster.waehleForm(Formen(self.zufallsform), isRotated, rotation_count)
            self.cluster.setForm()
            self.cluster.drawCluster(stdscr)

            self.feste_clusters.draw(stdscr)

            isBoden = self.boden.check_ifCollide_Boden(self.cluster.get_Seite('U'))
            isFCluster = self.feste_clusters.kollidiert_oben(self.cluster.get_Seite('U'))
            isFCluster_R = self.feste_clusters.kollidiert_seitlich(self.cluster.get_Seite('L'), 'R')  # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L
            isFCluster_L = self.feste_clusters.kollidiert_seitlich(self.cluster.get_Seite('R'), 'L')
            kollidiert = False
            
            # Wenn keine Tasten gedrückt werden, dann werden sämtliche Funktionen, die nach key = stdscr.getch() kommen, gar nicht ausgeführt
            key = stdscr.getch()
            if key == ord('q'):
                break

            if self.interface.if_gameover(self.feste_clusters):
                stdscr.clear()
                self.interface.print_gameover(stdscr, curses)
                stdscr.getch()
                break

            if key == ord('r'):
                rotation_count += 1
                if rotation_count > 3:
                    rotation_count = 0
                    isRotated = False
                    self.cluster.setForm()
                else:
                    isRotated = True
                    self.cluster.setForm()

            if key == curses.KEY_UP and y > 0:
                y -= 2
                self.cluster.setPos(y,x)
            if key == curses.KEY_DOWN:
                if isBoden == False and isFCluster == False: # and isFCluster_L == False
                    y += 2
                    self.cluster.setPos(y,x)
                else: # Cluster haftet am Boden und kann nicht mehr bewegt werden, der Cluster wird dann von dieser Variable entfernt 
                    kollidiert = True
            
            if self.wand_R.check_ifCollide_Wand(self.cluster.get_Seite('R')) == False:
                if key == curses.KEY_RIGHT:
                    if isFCluster_L == False:
                        x += 3
                        self.cluster.setPos(y,x)

            if self.wand_L.check_ifCollide_Wand(self.cluster.get_Seite('L')) == False:
                if key == curses.KEY_LEFT:
                    if isFCluster_R == False:
                        x -= 3
                        self.cluster.setPos(y,x)

            if kollidiert == True:
                self.feste_clusters.unbewegbare_clusters.append(self.cluster) # !!!
                self.zufallsform = random.randint(1,5)
                y, x = self.y_start, self.x_start # draw Koordinaten
                self.cluster = Cluster(y, x)
                rotation_count = 0
                isRotated = False
                
                if len(self.feste_clusters.unbewegbare_clusters) > 0 :
                    self.feste_clusters.anordnung()
                    self.feste_clusters.zeile_Loeschen(self.boden)
                    self.interface.update_Punktzahl(self.feste_clusters)
            
game = TetrisGame()
curses.wrapper(game.main)