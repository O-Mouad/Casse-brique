
"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025
fichier de la class game
"""

import tkinter as tk

class Brique:
    def __init__(self, x, y, largeur=100, hauteur=20, couleur="orange"):
        self.vie = 1
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.id = None  # identifiant du rectangle dans le canvas

    def afficher(self, canvas: tk.Canvas):
        """Affiche la brique sur le canvas et garde son ID."""
        self.id = canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.largeur,
            self.y + self.hauteur,
            fill=self.couleur,
            outline="black"
        )