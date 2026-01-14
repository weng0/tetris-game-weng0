from src.cluster import TetrisBlock
from src.klotz import Block
from src.tetris_rand import Boden

class Tetrismauer: #  ClusterFest
    def __init__(self, spielfeld_hoehe, spielfeld_breite):
        self.immobile_t_bloecke : TetrisBlock = [] # unbewegbare_Cluster
        self.spielfeld_hoehe = spielfeld_hoehe # screen_height
        self.bildschirm_breite = spielfeld_breite # screen_width
        self.y_schritte = int(spielfeld_hoehe/2)
        self.x_schritte = int((spielfeld_breite-1)/3)
        #self.koordinatensys = None
        self.mauerbloecke : Block = [] # alle_kloetze
        # self.cluster : TetrisBlock # cluster
        self.kompleteReihen = 0
        self.koordinaten = None

    def get_kompleteReihen(self):
        return self.kompleteReihen

    # def draw(self, fn_stdscr):
    #     for c in self.immobile_t_bloecke:
    #         c.draw_TetrisBlock(fn_stdscr) # c.draw

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

    def kollidiert_oben(self, obj_u_seiten : list): #  obj_cluster_pos_u
        kollidiert = False
        mauerbloecke_o_seiten = [] #  o_fest_kloetze
        for block in self.mauerbloecke: # k
            mauerbloecke_o_seiten.append(block.get_O_Seite())

        for einzelne_pos_u in obj_u_seiten: # pos_u
            y_u, x_u = einzelne_pos_u
            for einzelne_pos_o in mauerbloecke_o_seiten: # pos_o_seite
                y_o, x_o = einzelne_pos_o

                if y_u+1 == y_o and x_u == x_o:
                    kollidiert = True
        return kollidiert
    
    def kollidiert_seitlich(self, cluster_R_or_L : list, get_R_or_L : str): # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L # 
        kollidiert = False
        feste_seiten = []
        if get_R_or_L == 'R':
            for k in self.mauerbloecke:
                feste_seiten.append(k.get_R_Seite())
                #feste_seiten = self.get_Seiten('R') # das ist [(y,x), (y,x), ...]
        if get_R_or_L == 'L':
            for k in self.mauerbloecke:
                feste_seiten.append(k.get_L_Seite())
            #feste_seiten = self.get_Seiten('L')

        for cluster_pos in cluster_R_or_L:
            cluster_y, cluster_x = cluster_pos
            for pos_fest in feste_seiten:
                y_fest, x_fest = pos_fest

                if cluster_y == y_fest and x_fest == cluster_x-1: # Fest_R <- Cluster_L
                    kollidiert = True
                if cluster_y == y_fest and cluster_x+1 == x_fest: # Cluster_R -> Fest_L
                    kollidiert = True
        return kollidiert
    
    def koordinatensystem(self):
        screen_blocks = []
        y = 0
        for ys in range(self.y_schritte):
            screen_blocks.append([])
            x = 1
            for xs in range(self.x_schritte):
                pos = (y,x)
                screen_blocks[ys].append(pos)
                x += 3
            #print(screen_blocks[ys])
            y += 2
        self.koordinaten = screen_blocks
        
    def anordnung(self):
        for ucluster in self.immobile_t_bloecke:
            for k in ucluster.get_Bloecke(): #  get_Kloetze
                self.mauerbloecke.append(k)
        del self.immobile_t_bloecke[0:]
        #print('Alle_kloetze:', self.alle_kloetze)
        #print('Unbewegbare Cluster:', self.unbewegbare_clusters)

        # Klötze neu anordnen
        angeordnet = []
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

    def zeile_merken(self, zeile : int):
        gemerkt = []
        gemerkt.append(zeile)
        return gemerkt

    def zeile_Loeschen(self, boden : Boden):
        #self.anordnung()

        deleted_zeile = 0
        
        merke = []
        #y = 0
        for zeile in self.koordinaten:
            line = []
            for pos in zeile:
                y,x = pos
                for k in self.mauerbloecke:
                    if k.get_y() == y and k.get_x() == x:
                        line.append(pos)
            if len(line) != self.x_schritte:
                del line[0:]
            merke.append(line)
            
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

            deleted_zeile+=1

    def pruef_ob_max_Hoehe(self):
        max_Hoehe = False
        for k in self.mauerbloecke:
            if k.get_y() == 0:
                max_Hoehe = True
                break
        return max_Hoehe