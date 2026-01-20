from src.cluster import TetrisBlock
from src.klotz import Block
from src.tetris_rand import Boden

# Der Tetrismauer ist zusammengesetzt aus mehreren Tetris-Blöcken, die der Spieler endgültig abgelegt hat und sich nicht mehr bewegen lassen.

class Tetrismauer: #  ClusterFest # doch unbenennen in TetrisMauer -> tetris_mauer
    def __init__(self, spielfeld_hoehe, spielfeld_breite):
        self.immobile_t_bloecke : TetrisBlock = [] # unbewegbare_Cluster # Kommentar: Abgelegte Tetris-Blöcken
        self.spielfeld_hoehe = spielfeld_hoehe # screen_height
        self.spielfeld_breite = spielfeld_breite # screen_width # self.bildschirm_breite -> self.spielfeld_breite
        self.y_schritte = int(spielfeld_hoehe/2)
        self.x_schritte = int((spielfeld_breite-1)/3)
        #self.koordinatensys = None
        self.mauerbloecke : Block = [] # alle_kloetze # Kommentar: Alle Bestandteile der Tetris-Blöcke geordnet in einer Liste
        # self.cluster : TetrisBlock # cluster
        self.kompleteReihen = 0 # Kommentar: Anzahl der kompletten Reihen, die der Spieler geschaft hat
        self.koordinaten = None

    # Gibt den Anzahl der aktuelle Punktzahl des Spielers zurück
    def get_kompleteReihen(self):
        return self.kompleteReihen

    # def draw(self, fn_stdscr):
    #     for c in self.immobile_t_bloecke:
    #         c.draw_TetrisBlock(fn_stdscr) # c.draw

    # Zeichnet die Tetrismauer auf dem Bildschirm
    def draw(self, fn_stdscr):
        if len(self.mauerbloecke) > 0:
            for block in self.mauerbloecke: # k
                block.draw(fn_stdscr)

    # def get_Seiten(self, seite : str):
    #     oberseiten = []
    #     for c in self.unbewegbare_clusters:
    #         if seite == 'O':
    #             oberseiten += c.get_Seite('O')
    #         if seite == 'R':
    #             oberseiten += c.get_Seite('R')
    #         if seite == 'L':
    #             oberseiten += c.get_Seite('L')
    #     return oberseiten  # = Liste mit aller Oberseiten der Klötze, die in den festsitzenden Cluster vorhanden sind
    #         # das ist [(y,x), (y,x), ...]

    # Sensoren-Funktionen
    """ Diese Funktion prüft, ob ein fremdes Objekt mit der Tetrismauer kollidiert.
    Es gilt als kollidiert, wenn die unterste Seite des fremden Tetris-Blockes auf die Oberfläche der Mauer trifft.

    :param obj_u_seiten: Die Unterseite des fremden Tetris-Blockes (Liste)
    :return: Ob die Mauer kollidiert wurde (bool) """
    def kollidiert_oben(self, obj_u_seiten : list): #  obj_cluster_pos_u # da kommt funktion rein
        kollidiert = False
        mauerbloecke_o_seiten = [] #  o_fest_kloetze
        for mb in self.mauerbloecke: # k
            mauerbloecke_o_seiten.append(mb.get_O_Seite())

        for obj_pos_u in obj_u_seiten: # pos_u
            y_u, x_u = obj_pos_u
            for mb_pos_o in mauerbloecke_o_seiten: # pos_o_seite
                mb_y_o, mb_x_o = mb_pos_o

                if y_u+1 == mb_y_o and x_u == mb_x_o:
                    kollidiert = True
        return kollidiert
    
    """ Diese Funktion prüft, ob ein fremdes Objekt mit der Tetrismauer kollidiert.
    Es gilt als kollidiert, wenn die rechte Seite des fremden Tetris-Blockes auf die linke Seite des herausragenden Mauerblockes trifft,
    oder die linke Seite des fremden Tetris-Blockes auf die rechte Seite des herausragenden Mauerblockes trifft.

    :param obj_u_seiten: Die äußerst linke oder rechte Seite des fremden Tetris-Blockes (Liste)
    :return: Ob die Mauer kollidiert wurde (bool) """
    def kollidiert_seitlich(self, obj_R_oder_L_seiten : list, waehle_R_oder_L : str): # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L #  cluster_R_or_L, get_R_or_L
        kollidiert = False
        mauerbloecke_seiten = [] # feste_seiten
        if waehle_R_oder_L == 'R':
            for mb in self.mauerbloecke:
                mauerbloecke_seiten.append(mb.get_R_Seite())
                #feste_seiten = self.get_Seiten('R') # das ist [(y,x), (y,x), ...]
        if waehle_R_oder_L == 'L':
            for mb in self.mauerbloecke: # k
                mauerbloecke_seiten.append(mb.get_L_Seite())
            #feste_seiten = self.get_Seiten('L')

        for obj_pos_seite in obj_R_oder_L_seiten: # cluster_pos
            obj_y_seite, obj_x_seite = obj_pos_seite # ,  cluster_y, cluster_x
            for mb_pos_seite in mauerbloecke_seiten: # pos_fest
                mb_y_seite, mb_x_seite = mb_pos_seite # pos_... oder ..._pos Namensgebung????????? pos_fest, y_fest-> m_block_seite_y, x_fest-> m_block_seite_x

                if obj_y_seite == mb_y_seite and mb_x_seite == obj_x_seite-1: # Fest_R <- Cluster_L
                    kollidiert = True
                if obj_y_seite == mb_y_seite and obj_x_seite+1 == mb_x_seite: # Cluster_R -> Fest_L
                    kollidiert = True
        return kollidiert
    
    # Erfasst die Koordinaten des Spielfeldgitters und speichert sie in einer verschachtelten Liste.
    def gitter_erfassen(self): # koordinatensystem, 
        bildschirm_gitter = [] #  screen_blocks
        y = 0
        for ys in range(self.y_schritte):
            bildschirm_gitter.append([])
            x = 1
            for xs in range(self.x_schritte):
                pos = (y,x)
                bildschirm_gitter[ys].append(pos)
                x += 3
            #print(screen_blocks[ys])
            y += 2
        self.koordinaten = bildschirm_gitter
        
    # Alle Blöcke in den abgelegten Tetris-Blöcken werden im einer neue Liste erfasst und in Reihenfolge gebracht.
    def bloecke_anordnen(self): # anordnung
        for t_block in self.immobile_t_bloecke: # ucluster
            for block in t_block.get_Bloecke(): #  get_Kloetze , k -> block
                self.mauerbloecke.append(block)
        del self.immobile_t_bloecke[0:]
        #print('Alle_kloetze:', self.alle_kloetze)
        #print('Unbewegbare Cluster:', self.unbewegbare_clusters)

        # Klötze neu anordnen
        angeordnet = [] # 
        # koo = [] # Test
        for zeile in self.koordinaten:
            for koord in zeile:
                y,x = koord
                for k in self.mauerbloecke : # geändert
                    if y == k.get_y() and x == k.get_x():
                        angeordnet.append(k)
                        #,ko = k.get_y(),k.get_x() # Test
                        #,koo.append(ko)  # Test
        del self.mauerbloecke[0:] # geändert
        # print(koo) # Test
        self.mauerbloecke += angeordnet.copy()
        #print(self.alle_kloetze) # Test

    # Bestimmte Zeilen werden in einer Liste gespeichert
    def zeile_merken(self, zeile : int):
        gemerkt = []
        gemerkt.append(zeile)
        return gemerkt

    """
    In einer Schleife wird geprüft, ob sich Mauerblöcke in den einzelnen Zeilen des Spielfeldgitters befinden
    und ob eine Reihe vollständig gefüllt ist. Bei jeder vollständigen Reihe werden zunächst die Koordinaten
    aller Blöcke dieser Reihe in der Liste „merke“ gespeichert. Anschließend werden diese Blöcke aus der
    Liste self.mauerbloecke entfernt. Die Reihen oberhalb der gelöschten Zeilen rücken danach
    um eine Position nach unten.
    """
    def zeile_loeschen(self, boden : Boden): # zeile_Loeschen # param löschen
        #self.anordnung()

        geloeschte_zeilen = 0 # deleted_zeilen, Anzahl gelöschte Zeilen
        
        merke = []
        #y = 0
        for zeile in self.koordinaten:
            reihe = [] # line
            for pos in zeile:
                y,x = pos
                for block in self.mauerbloecke: # k -> block
                    if block.get_y() == y and block.get_x() == x:
                        reihe.append(pos)
            if len(reihe) != self.x_schritte:
                del reihe[0:]
            merke.append(reihe)
            
        for zeile in merke:
            y = 0 # default
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

            geloeschte_zeilen+=1
 
    # Hier wird die aktuelle Höhe der Mauer ermittelt.
    def pruef_max_hoehe(self): # pruef_ob_max_Hoehe
        max_hoehe = False
        for k in self.mauerbloecke:
            if k.get_y() == 0:
                max_hoehe = True
                break
        return max_hoehe