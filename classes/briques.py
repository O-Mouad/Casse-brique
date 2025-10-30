
"""
Mouad Ouamane
Sacha Bargoin 
Groupe C
TP4 Casse briques 09/10/2025 , 16/10/2025 , 23/10/2025

fichier de la class briques qui gère les briques du jeu 

Amélioration possible : - ajouter des méthodes pour chaque brique ( par exemple pour gérer les briques spéciales )
                        - ajouter une animùation lors de la destruction des briques
                        - ajouter des effets sonores lors de la destruction des briques
                        - ajouter des briques avec plus de vie ( 2 ou 3 coups pour les casser)
                        - ajouter des briques spéciales ( qui donnent des bonus ou malus )
                        
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