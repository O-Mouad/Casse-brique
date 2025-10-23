"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025
fichier main

A faire : -rajouter un piles & files pour gerer les niveaux et les scores mais aussi un systeme de vie
- ameliorer le design
- ameliorer la gestion des collisions
- faire en sorte que le caneva s'adapte a la taille de l'ecran
"""
import os
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from classes.briques import Brique
from classes.balle import Balle
from classes.pad import Pad

# Liste des couleurs des briques
color = [
    "#F80008",  # rouge vif
    "#FF924C",  # orange clair
    "#FFCA3A",  # jaune
    "#8AC926",  # vert clair
    "#1982C4",  # bleu
    "#6A4C93",  # violet
    "#C03221",  # rouge foncé
    "#0FA3B1",  # turquoise
    "#A29BFE",  # lavande
    "#FFD6E0",  # rose pâle
    "#FF5100",  # orange doux
    "#43AA8B",  # vert menthe
    "#577590",  # bleu gris
    "#FF70A6",  # rose vif
    "#FF9770",  # pêche
    "#70D6FF",  # bleu ciel
    "#A1F954",  # vert lime clair
    "#9B5DE5",  # violet flashy
    "#F15BB5",  # rose magenta
    "#F4E374"   # jaune fluo
]

"ouverture du fichier contenant les scores"
score = [] 
with open("score", "r") as f:
    for val in f: 
        score.append(int(val))

"fonction qui enregistre les scores"
def enregistrer_score(): 
    with open("score", "w") as f:
        for val in score: 
            f.write(str(val) + "\n")

"""fonction jeu : gère tout le déroulement de la partie une fois le jeu lancé , 
"""

def jeu():
    dif = curseur.get()

    caneva.delete("all")
    caneva.config(bg="#2E003E")
  
    briques = []

    # Paramètres d'affichage
    nb_lignes = dif
    nb_par_ligne = 9
    marge = 10  # espace entre les briques
    offset_y = 10  # distance du haut de l'écran

    for ligne in range(nb_lignes):
        for col in range(nb_par_ligne): # 9 briques par ligne
            x = marge + col * (100 + marge)
            y = offset_y + ligne * (20 + marge)
            brique = Brique(x, y, couleur=color[ligne % len(color)])
            brique.afficher(caneva)
            briques.append(brique)

    pad = Pad(caneva, 440, 650)  # position au bas de l’écran
    pad.afficher()

    # Création de la balle avec rayon connu
    balle = Balle(rayon=10, couleur="white")  # rayon visible

    # Position : centrée sur le pad, au-dessus (centre X du pad)
    balle_x = pad.x + pad.largeur / 2
    balle_y = pad.y - balle.rayon - 1  # -1 pour éviter un léger recouvrement
    balle.pos(balle_x, balle_y)

    # Affichage initial de la balle
    balle.affichage(caneva)

    # state: ball starts attached to the pad
    ball_attached = True

    # Affichage initial de la balle
    balle.affichage(caneva)

    # gestion des touches clavier

    def lancer(direction: str): # Lancer la balle selon la touche appuyée
        nonlocal ball_attached
        if not ball_attached:  # si la balle est déjà en mvt ne rien faire
            return
        vx = -180.0 if direction == "left" else 180.0 
        vy = -300.0
        balle.set_vitesse(vx, vy)
        ball_attached = False


    def fleche_gauche(event=None):  # déplacer le pad à gauche avec la fleche de gauche
        pad.start_move_left(event)
        lancer("left")

    def fleche_droite(event=None): # déplacer le pad à droite avec la fleche de droite
        pad.start_move_right(event)
        lancer("right")

    def relacher_gauche(event=None): # arrêter le déplacement
        pad.stop_move_left(event)

    def relacher_droite(event=None): # arrêter le déplacement
        pad.stop_move_right(event)

    Fenetre.bind("<KeyPress-Left>", fleche_gauche)
    Fenetre.bind("<KeyRelease-Left>", relacher_gauche)
    Fenetre.bind("<KeyPress-Right>", fleche_droite)
    Fenetre.bind("<KeyRelease-Right>", relacher_droite)

    # Boucle de jeu : update physics, collisions et redraw
    def game_loop():
        nonlocal ball_attached
        dt = 1 / 60.0  # approximativement 60 FPS

        if ball_attached:
            # garde la balle au centre du pad
            balle.pos(pad.x + pad.largeur / 2, pad.y - balle.rayon - 1)
        else:
            # mise à jour de la physique qui sont dans balle.py
            balle.update(dt, (largeur, hauteur))

            # collision entre le pad et la balle 
            balle.rebond_brique(pad.x, pad.y, pad.largeur, pad.hauteur)

            # collision briques : si rebond contre une brique -> suppression
            for b in briques[:]:
                if balle.rebond_brique(b.x, b.y, b.largeur, b.hauteur):
                    if b.id is not None:
                        caneva.delete(b.id)
                    try:
                        briques.remove(b)
                    except ValueError:
                        pass

    
        balle.affichage(caneva)

        # continuer ou afficher game over si vies épuisées
        if balle.vie > 0:
            Fenetre.after(int(dt * 1000), game_loop)
        else:           
            # Fond semi-transparent
            caneva.create_rectangle(0, 0, largeur, hauteur, fill="#000000", stipple="gray50")

            # Message principal
            caneva.create_text(largeur // 2, hauteur // 2 - 30,
                       text="GAME OVER",
                       fill="#FF0000",
                       font=("Helvetica", 64, "bold"))

            # Message secondaire humoristique
            caneva.create_text(largeur // 2, hauteur // 2 + 40,
                       text="Tu pues le chameau mort 🐫💀",
                       fill="white",
                       font=("Helvetica", 28, "italic"))

            # Bouton pour relancer (optionnel)
            retry_button = tk.Button(Fenetre, text="Rejouer", font=("Helvetica", 16, "bold"), bg="#333", fg="white", command=lambda: jeu())
            caneva.create_window(largeur // 2, hauteur // 2 + 100, window=retry_button)


    # start updates
    pad.update()
    game_loop()

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

caneva.create_text(500, 150, text="CASSE BRIQUES DU FUTURE", fill="white",font =("Lucida Console", 24))
subtitle = tk.Label(Fenetre, text="Appuie sur 'Jouer' pour commencer",)
texte = tk.Label(Fenetre, text="difficulté du jeu:")
play_button = tk.Button(Fenetre, text="Jouer", command=lambda: jeu())

curseur = tk.Scale(
    caneva,             # parent
    from_=1, to=15,      # bornes
    orient='horizontal', # orientation
    length=300,          # longueur du slider 
    )

# Placer les widgets sur le canevas
caneva.create_window(500, 250, window=subtitle)
caneva.create_window(500, 600, window=texte)
caneva.create_window(500, 350, window=play_button)
caneva.create_window(500, 650, window=curseur)

Fenetre.mainloop()