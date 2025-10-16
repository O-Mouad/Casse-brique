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
from classes.pad import Pad

color = [
    "#FF595E",  # rouge vif
    "#FF924C",  # orange clair
    "#FFCA3A",  # jaune
    "#8AC926",  # vert clair
    "#1982C4",  # bleu
    "#6A4C93",  # violet
    "#C03221",  # rouge foncé
    "#0FA3B1",  # turquoise
    "#A29BFE",  # lavande
    "#FFD6E0",  # rose pâle
    "#F9844A",  # orange doux
    "#43AA8B",  # vert menthe
    "#577590",  # bleu gris
    "#FF70A6",  # rose vif
    "#FF9770",  # pêche
    "#70D6FF",  # bleu ciel
    "#B5E48C",  # vert lime clair
    "#9B5DE5",  # violet flashy
    "#F15BB5",  # rose magenta
    "#FEE440"   # jaune fluo
]

def jeu(dif):
    print("jeu")
    caneva.delete("all")
    caneva.config(bg="#2E003E")  
    briques = []

    # Paramètres d'affichage
    nb_lignes = dif
    nb_par_ligne = 9
    marge = 10  # espace entre les briques
    offset_y = 5  # distance du haut de l'écran


    for ligne in range(nb_lignes):
        for col in range(nb_par_ligne):
            x = marge + col * (100 + marge)
            y = offset_y + ligne * (20 + marge)
            brique = Brique(x, y, couleur =color[ligne])
            brique.afficher(caneva)
            briques.append(brique)

    pad = Pad(caneva, 440, 650)  # position au bas de l’écran
    pad.afficher()
    # Bind touches clavier
    Fenetre.bind("<Left>", pad.move_left)
    Fenetre.bind("<Right>", pad.move_right)


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
play_button = tk.Button(Fenetre, text="Jouer", command=lambda: jeu(10))

# Placer les widgets sur le canevas
caneva.create_window(500, 150, window=title)
caneva.create_window(500, 250, window=subtitle)
caneva.create_window(500, 350, window=play_button)

Fenetre.mainloop()