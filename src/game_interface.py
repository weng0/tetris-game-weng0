from src.cluster_fest import ClusterFest

class Game_Interface:
    def __init__(self):
        self.punktzahl = 0
        self.spieler_name = ''
    
    def setName(self, stdscr_fn, curses_fn): pass


    def update_Punktzahl(self, cluster_f : ClusterFest):
        self.punktzahl = cluster_f.get_kompleteReihen()

    def print_Interface(self, stdscr_fn):
        stdscr_fn.addstr(10, 55, f"Punktzahl: {self.punktzahl}")

    def if_gameover(self,  cluster_f : ClusterFest): # Für GAMEOVER
        if cluster_f.pruef_ob_max_Hoehe():
            return True
        
    def print_gameover(self, stdscr_fn,curses_fn): # Für GAMEOVER
        stdscr_fn.addstr(10, 1, "/////     //  //    //  /////   //  /     / ///// ////")
        stdscr_fn.addstr(11, 1, "//       / /  / /  / /  /___  /   /  /   /  /___  /  /")
        stdscr_fn.addstr(12, 1, "/  ///  ///// /  //  /  /     /   /   / /   /     ////")
        stdscr_fn.addstr(13, 1, "////   /   // // /   // /////  //      /    ///// /  // ")

        stdscr_fn.addstr(17, 10, f"Punktzahl: {self.punktzahl}")




'''
/////     //  //    //  /////   //  /     / ///// ////
//       / /  / /  / /  /___  /   /  /   /  /___  /  /
/  ///  ///// /  //  /  /     /   /   / /   /     ////
////   /   // // /   // /////  //      /    ///// /  // 
'''