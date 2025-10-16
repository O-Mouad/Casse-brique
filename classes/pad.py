import tkinter as tk

class Pad:
    def __init__(self, canvas, x, y, vitesse = 15, largeur=120, hauteur=20, couleur="blue"):
        self.canvas = canvas
        self.x = x 
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.vitesse = vitesse  # déplacement par touche
        self.id = None
        self.moving_left = False
        self.moving_right = False
    def afficher(self): 
        self.id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill=self.couleur
        )

    def start_move_left(self, event=None):
        self.moving_left = True

    def stop_move_left(self, event=None):   
        self.moving_left = False

    def start_move_right(self, event=None):
        self.moving_right = True
 

    def stop_move_right(self, event=None):
        self.moving_right = False

    def get_coords(self):
        return self.canvas.coords(self.id)
    
    def update(self):
        if self.moving_left and self.x > 0 :
            self.canvas.move(self.id, -self.vitesse, 0)
            self.x -= self.vitesse
        if self.moving_right and self.x < 1000-self.largeur:
            self.canvas.move(self.id, self.vitesse, 0)
            self.x += self.vitesse
        self.canvas.after(5, self.update) 