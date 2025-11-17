from src.cluster import Cluster
from src.klotz import Klotz
from src.tetris_rand import Boden

class ClusterFest:
    def __init__(self, screen_height, screen_width):
        self.unbewegbare_clusters : Cluster = []
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.y_schritte = int(screen_height/2)
        self.x_schritte = int((screen_width-1)/3)
        #self.koordinatensys = None
        self.alle_kloetze : Klotz = []
        self.cluster : Cluster
        self.kompleteReihen = 0
        self.koordinaten = None

    def get_kompleteReihen(self):
        return self.kompleteReihen

    def draw(self, fn_stdscr):
        for c in self.unbewegbare_clusters:
            c.drawCluster(fn_stdscr)

    def draw(self, fn_stdscr):
        if len(self.alle_kloetze) > 0:
            for k in self.alle_kloetze:
                k.draw(fn_stdscr)

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

    def kollidiert_oben(self, obj_cluster_pos_u : list):
        kollidiert = False
        o_fest_kloetze = []
        for k in self.alle_kloetze:
            o_fest_kloetze.append(k.get_O_Seite())

        for pos_u in obj_cluster_pos_u:
            y_u, x_u = pos_u
            for pos_o in o_fest_kloetze:
                y_o, x_o = pos_o

                if y_u+1 == y_o and x_u == x_o:
                    kollidiert = True
        return kollidiert
    
    def kollidiert_seitlich(self, cluster_R_or_L : list, get_R_or_L : str): # Wenn Cluster_R -> Fest_L / Fest_R <- Cluster_L
        kollidiert = False
        feste_seiten = []
        if get_R_or_L == 'R':
            for k in self.alle_kloetze:
                feste_seiten.append(k.get_R_Seite())
                #feste_seiten = self.get_Seiten('R') # das ist [(y,x), (y,x), ...]
        if get_R_or_L == 'L':
            for k in self.alle_kloetze:
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
        for ucluster in self.unbewegbare_clusters:
            for k in ucluster.get_Kloetze():
                self.alle_kloetze.append(k)
        del self.unbewegbare_clusters[0:]
        #print('Alle_kloetze:', self.alle_kloetze)
        #print('Unbewegbare Cluster:', self.unbewegbare_clusters)

        # Klötze neu anordnen
        angeordnet = []
        # koo = [] # Test
        for zeile in self.koordinaten:
            for koord in zeile:
                y,x = koord
                for k in self.alle_kloetze : # geändert
                    if y == k.get_y() and x == k.get_x():
                        angeordnet.append(k)
                        #,ko = k.get_y(),k.get_x() # Test
                        #,koo.append(ko)  # Test
        del self.alle_kloetze[0:] # geändert
        # print(koo) # Test
        self.alle_kloetze += angeordnet.copy()
        #print(self.alle_kloetze) # Test

    def zeile_merken(self, zeile : int):
        gemerkt = []
        gemerkt.append(zeile)
        return gemerkt

    def zeile_Loeschen(self, boden : Boden):
        #self.anordnung()

        deleted_zeile = 0
        # verschiebung = 0
        merke = []
        y = 0
        for zeile in self.koordinaten:
            align = 0
            for k in self.alle_kloetze:
                if k.get_y() == y:
                    # print('Element in Zeile','y:',k.get_y(),'x:', k.get_x())
                    align += 1
                if align == self.x_schritte:
                    merke = self.zeile_merken(y)
                    # print('Zeilen gemerkt',merke) # Test 
            # print('Align Elemente',align)  # Test 
            y += 2
            # for koord in zeile: pass
            
        # gemerkte Zeilen löschen
        y_2te = 0
        for zeile in self.koordinaten:
            # print('y_2te:', y_2te, 'Zeile_list:',zeile) # Test
            if y_2te in merke:
                k = len(self.alle_kloetze)-1
                while k >= 0:
                    klotz = self.alle_kloetze[k]
                    #for k in self.alle_kloetze:
                    if klotz.get_y() == y_2te:
                        del self.alle_kloetze[k]
                    k-= 1
                deleted_zeile += 1
            y_2te += 2

        for k in self.alle_kloetze:
            if boden.check_ifCollide_Boden(k.getUnterseite()) == False:
                y = k.get_y() + deleted_zeile*2
                k.set_y(y)
        #print(self.alle_kloetze)
        self.kompleteReihen += deleted_zeile

    def pruef_ob_max_Hoehe(self):
        max_Hoehe = False
        for k in self.alle_kloetze:
            if k.get_y() == 0:
                max_Hoehe = True
                break
        return max_Hoehe