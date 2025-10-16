
"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025
fichier de la class game
"""

class Brique(): 
    def __init__(self): 
        self.vie = 1
        self.posX = 0 
        self.posY = 0
        self.hauteur = 20
        self.largeur = 100
        
    def pos(self,x,y): 
        self.posX = x
        self.posY = y 