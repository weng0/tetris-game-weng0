from src.cluster import TetrisBlock
from src.klotz import Block
from src.tetris_rand import Boden

# Die Tetrismauer ist zusammengesetzt aus mehreren Tetris-Blöcken, die der Spieler endgültig abgelegt hat und die sich nicht mehr bewegen lassen.
class Tetrismauer: # unbenennen in: TetrisMauer -> tetris_mauer
    def __init__(self, spielfeld_hoehe, spielfeld_breite):
        self.immobile_t_bloecke : TetrisBlock = []
        self.spielfeld_hoehe = spielfeld_hoehe
        self.spielfeld_breite = spielfeld_breite
        self.y_schritte = int(spielfeld_hoehe/2)
        self.x_schritte = int((spielfeld_breite-1)/3)
        self.mauerbloecke : Block = [] # Alle Bestandteile der Tetris-Blöcke geordnet in einer Liste
        self.kompleteReihen = 0 # Anzahl der kompletten Reihen, die der Spieler geschaft hat
        self.koordinaten = None

    # Gibt die Anzahl der vervollständigten Reihen zurück, die auch der aktuellen Punktzahl des Spielers entsprechen.
    # return: Anzahl der vervollständigten Reihen
    def get_kompleteReihen(self):
        return self.kompleteReihen

    # Zeichnet die Tetrismauer auf dem Bildschirm
    def draw(self, fn_stdscr):
        if len(self.mauerbloecke) > 0:
            for block in self.mauerbloecke: # k
                block.draw(fn_stdscr)

    # Sensoren-Funktionen
    """ Diese Funktion prüft, ob ein fremdes Objekt mit der Tetrismauer kollidiert.
    Eine Kollision liegt vor, wenn die unterste Seite des fremden Tetris-Blocks auf die Oberfläche der Mauer trifft.

    :param obj_u_seiten: Die Unterseite des fremden Tetris-Blocks (Liste)
    :return: Ob eine Kollision mit der Mauer vorliegt (bool) """
    def kollidiert_oben(self, obj_u_seiten : list): # Kommentieren, dass da kommt funktion rein
        kollidiert = False
        mauerbloecke_o_seiten = []
        for mb in self.mauerbloecke:
            mauerbloecke_o_seiten.append(mb.get_O_Seite())

        for obj_pos_u in obj_u_seiten:
            y_u, x_u = obj_pos_u
            for mb_pos_o in mauerbloecke_o_seiten:
                mb_y_o, mb_x_o = mb_pos_o

                if y_u+1 == mb_y_o and x_u == mb_x_o:
                    kollidiert = True
        return kollidiert
    
    """ Diese Funktion prüft, ob ein fremdes Objekt mit der Tetrismauer kollidiert.
    Eine Kollision liegt vor, wenn die rechte Seite des fremden Tetris-Blocks auf die linke Seite des herausragenden Mauerblockes trifft,
    oder die linke Seite des fremden Tetris-Blockes auf die rechte Seite des herausragenden Mauerblocks trifft.

    :param obj_u_seiten: Die äußerste linke oder rechte Seite des fremden Tetris-Blocks (Liste)
    :return: Ob eine Kollision mit der Mauer vorliegt (bool) """
    def kollidiert_seitlich(self, obj_R_oder_L_seiten : list, waehle_R_oder_L : str): # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L #  cluster_R_or_L, get_R_or_L
        kollidiert = False
        mauerbloecke_seiten = []
        if waehle_R_oder_L == 'R':
            for mb in self.mauerbloecke:
                mauerbloecke_seiten.append(mb.get_R_Seite())
        if waehle_R_oder_L == 'L':
            for mb in self.mauerbloecke:
                mauerbloecke_seiten.append(mb.get_L_Seite())

        for obj_pos_seite in obj_R_oder_L_seiten:
            obj_y_seite, obj_x_seite = obj_pos_seite
            for mb_pos_seite in mauerbloecke_seiten:
                mb_y_seite, mb_x_seite = mb_pos_seite

                if obj_y_seite == mb_y_seite and mb_x_seite == obj_x_seite-1: # Fest_R <- Cluster_L
                    kollidiert = True
                if obj_y_seite == mb_y_seite and obj_x_seite+1 == mb_x_seite: # Cluster_R -> Fest_L
                    kollidiert = True
        return kollidiert
    
    # Erfasst die Koordinaten des Spielfeldgitters und speichert sie in einer verschachtelten Liste.
    def gitter_erfassen(self): 
        bildschirm_gitter = []
        y = 0
        for ys in range(self.y_schritte):
            bildschirm_gitter.append([])
            x = 1
            for xs in range(self.x_schritte):
                pos = (y,x)
                bildschirm_gitter[ys].append(pos)
                x += 3
            y += 2
        self.koordinaten = bildschirm_gitter
        
    # Alle Blöcke der abgelegten Tetris-Blöcke werden in einer neuen Liste erfasst und in eine Reihenfolge gebracht.
    def bloecke_anordnen(self):
        for t_block in self.immobile_t_bloecke:
            for block in t_block.get_Bloecke():
                self.mauerbloecke.append(block)
        del self.immobile_t_bloecke[0:]

        # Klötze neu anordnen
        angeordnet = []

        for zeile in self.koordinaten:
            for koord in zeile:
                y,x = koord
                for k in self.mauerbloecke:
                    if y == k.get_y() and x == k.get_x():
                        angeordnet.append(k)
        del self.mauerbloecke[0:]
        self.mauerbloecke += angeordnet.copy()

    # Bestimmte, ausgewählte Zeilen werden in einer Liste gespeichert.
    def zeile_merken(self, zeile : int):
        gemerkt = []
        gemerkt.append(zeile)
        return gemerkt

    """
    Überprüft das Spielfeld auf vollständig gefüllte Reihen, entfernt deren
    Blöcke und lässt die darüberliegenden Reihen nach unten rücken.
    """
    def zeile_loeschen(self, boden : Boden):
        merke = []
        for zeile in self.koordinaten:
            reihe = []
            for pos in zeile:
                y,x = pos
                for block in self.mauerbloecke:
                    if block.get_y() == y and block.get_x() == x:
                        reihe.append(pos)

            if len(reihe) == self.x_schritte:
                merke.append(reihe)
                self.kompleteReihen+=1
            else: del reihe[0:]
            
        for zeile in merke:
            y = 0
            for pos in zeile:
                y,x = pos
                index = 0
                for k in self.mauerbloecke:
                    if k.get_y() == y and k.get_x() == x:
                        del self.mauerbloecke[index]
                        break
                    index+=1

            for k in self.mauerbloecke:
                if k.get_y() < y:
                    y_k = k.get_y()+2
                    k.set_y(y_k)
 
    # Hier wird die aktuelle Höhe der Tetrismauer ermittelt.
    def pruef_max_hoehe(self):
        max_hoehe = False
        for k in self.mauerbloecke:
            if k.get_y() == 0:
                max_hoehe = True
                break
        return max_hoehe