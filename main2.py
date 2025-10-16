"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025
fichier main
"""
import os
import tkinter as tk
from PIL import Image, ImageTk
from classes.briques import Brique
from classes.balle import Balle


def jeu():
    print("jeu")



(largeur,hauteur) =(1000,700)

Fenetre = tk.Tk()
Fenetre.title("casses burnes")
Fenetre.resizable(False, False)  # Empêche le redimensionnement

 # Chemin de l'image
base_path = os.path.dirname(__file__)
image_path = os.path.join(base_path, "asset", "vis", "fond.png")
image_path = os.path.normpath(image_path)

# Charger l'image avec Pillow
image_pil = Image.open(image_path)
image_redim = image_pil.resize((largeur, hauteur), Image.Resampling.LANCZOS)
image_tk = ImageTk.PhotoImage(image_redim)  # Conversion pour Tkinter

# Canvas pour le fond
caneva = tk.Canvas(Fenetre, width=largeur, height=hauteur)
caneva.create_image(0, 0, anchor="nw", image =image_tk)
caneva.pack(fill="both", expand=True)

title = tk.Label(Fenetre , text="Casse-briques",)
subtitle = tk.Label(Fenetre, text="Appuie sur 'Jouer' pour commencer",)
play_button = tk.Button(Fenetre, text="Jouer", command=jeu)

# Placer les widgets sur le canevas
caneva.create_window(500, 150, window=title)
caneva.create_window(500, 250, window=subtitle)
caneva.create_window(500, 350, window=play_button)

Fenetre.mainloop()
