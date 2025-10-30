import tkinter as tk

"""Classe représentant la raquette du casse-briques.

    Attributs: 
    - les coordonnées du pad 
    - la vitesse de déplacement du pad 
    - ses dimensions 
    - sa couleur

    on declare les variable sans _self. pour pouvoir y acceder plus simplement par la suite
    
    Fonctions : 
    - afficher 
    - 4 fonctions pour le déplacement avec 4 flags 
    - une fonction get_coords qui permet de recuperer x et y d'un seul coup 
    - une fonction update qui gère le déplacement du pad
    """


class Pad:

    # fonction d'initialisation des attribur de l'objet pad
    def __init__(self, canvas, x, y, vitesse = 10, largeur=120, hauteur=20, couleur="blue"):
        self.canvas = canvas
        self.x = x 
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur  
        self.vitesse = vitesse  #vitesse de déplacement du pad
        self.id = None
        self.moving_left = False
        self.moving_right = False

    #fonction permettant l'affichage du pad 
    def afficher(self): 
        self.id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill=self.couleur
        )

    """ ces 4 fonctions sont appeler par .bind (ligne 104 a 107 de main2)
    elle fixe des flags (moving_lef et moving_right) qui sont ensuite utiliser par la fonction update pour déplacer la balle.
    """
    def start_move_left(self, event=None):
        self.moving_left = True

    def stop_move_left(self, event=None):   
        self.moving_left = False

    def start_move_right(self, event=None):
        self.moving_right = True

    def stop_move_right(self, event=None):
        self.moving_right = False

    # retourne les 2coordonées du pad. 
    def get_coords(self):
        return self.canvas.coords(self.id)
    
    """
    regarde l'état des flags et la position du pad: suivant les conditions le pad est déplacer , ou non.
    cette fonction s'éxecute toutes les 15 ms
    """
    def update(self):
        if self.moving_left and self.x > 0 :
            self.canvas.move(self.id, -self.vitesse, 0)
            self.x -= self.vitesse
        if self.moving_right and self.x < 1000-self.largeur:
            self.canvas.move(self.id, self.vitesse, 0)
            self.x += self.vitesse
        self.canvas.after(15, self.update) 

    def set_taille(self, nouvelle_largeur):
        """Change la taille du pad et met à jour son affichage
        
        variable:
            nouvelle_largeur (int): La nouvelle largeur du pad en pixels
        """
        # Sauvegarde la position actuelle du centre du pad
        centre_x = self.x + self.largeur / 2
        
        # Met à jour la largeur
        self.largeur = nouvelle_largeur
        
        # Recalcule la position x pour garder le pad centré
        self.x = centre_x - self.largeur / 2
        
        # Si le pad sort de l'écran, le ramener dans les limites
        if self.x < 0:
            self.x = 0
        elif self.x + self.largeur > 1000:
            self.x = 1000 - self.largeur
            
        # Supprime l'ancien pad
        if self.id is not None:
            self.canvas.delete(self.id)
            
        # Réaffiche le pad avec sa nouvelle taille
        self.afficher()