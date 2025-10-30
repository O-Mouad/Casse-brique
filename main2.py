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
scores = [] 
score = 0
try:
    with open("score.txt", "r") as f:
        for val in f: 
            scores.append(int(val))
except FileNotFoundError:
    # Si le fichier n'existe pas, on le crée avec un score initial de 0 ( j'ai rajouter cette partie car suivant la version python cela peut poser probleme     )
    with open("score.txt", "w") as f:
        f.write("0\n")
    scores.append(0)

"fonction qui enregistre les scores"
def enregistrer_score(): 
    with open("score.txt", "w") as f:
        for val in scores: 
            f.write(str(val) + "\n")

"""fonction jeu : gère tout le déroulement de la partie une fois le jeu lancé , 
"""

def retour_menu():
    # Effacer le canvas et réafficher le menu principal
    caneva.delete("all")
    caneva.config(bg="#2E003E")
    
    # Réafficher l'image de fond
    caneva.create_image(0, 0, anchor="nw", image=image_tk)
    
    # Réafficher tous les éléments du menu
    caneva.create_text(500, 150, text="CASSE BRIQUES DU FUTURE", fill="white", font=("Lucida Console", 24))
    caneva.create_window(500, 250, window=subtitle)
    caneva.create_window(500, 600, window=texte)
    caneva.create_window(500, 350, window=play_button)
    caneva.create_window(500, 650, window=curseur)
    caneva.create_window(900, 500, window=score_frame)

def jeu():
    dif = curseur.get()

    caneva.delete("all")
    
    # Charger l'image de fond pour le jeu
    game_bg_path = os.path.join(os.path.dirname(__file__), "asset", "vis", "galaxie.jpg")
    game_bg_path = os.path.normpath(game_bg_path)
    
    # Charger et redimensionner l'image de fond du jeu
    game_bg = Image.open(game_bg_path)
    game_bg_resized = game_bg.resize((largeur, hauteur), Image.Resampling.LANCZOS)
    game_bg_tk = ImageTk.PhotoImage(game_bg_resized)
    
    # Créer l'image de fond
    caneva.create_image(0, 0, anchor="nw", image=game_bg_tk)
    # Garder une référence pour éviter la collecte de déchets
    caneva.game_bg = game_bg_tk
  
    briques = []
    
    # Ajouter les boutons Menu et Quitter
    menu_button = tk.Button(Fenetre, text="Menu", command=retour_menu, bg="#333", fg="white", font=("Helvetica", 12))
    quit_button = tk.Button(Fenetre, text="Quitter", command=Fenetre.quit, bg="#333", fg="white", font=("Helvetica", 12))
    
    # Créer une bande noire semi-transparente en haut pour l'en-tête
    caneva.create_rectangle(0, 0, largeur, 50, fill="#000000", stipple="gray50")
    
    # Placer les boutons en haut à droite
    caneva.create_window(largeur - 100, 25, window=menu_button)
    caneva.create_window(largeur - 30, 25, window=quit_button)
    

    # Paramètres d'affichage
    nb_lignes = dif
    nb_par_ligne = 9
    marge = 10  # espace entre les briques
    offset_y = 60  # augmenté pour laisser de la place pour l'en-tête
    
    # Créer l'en-tête
    caneva.create_rectangle(0, 0, largeur, 50, fill="#000000", stipple="gray50")
    caneva.create_line(0, 50, largeur, 50, fill="white", width=2)  # ligne de séparation

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
    # Moins de vies pour les niveaux faciles
    if dif <= 5:
        vies_initiales = 2  # 2 vies pour les niveaux 1-5
    elif dif <= 10:
        vies_initiales = 3  # 3 vies pour les niveaux 6-10
    else:
        vies_initiales = 4  # 4 vies pour les niveaux 11-15
    
    balle = Balle(rayon=10, couleur="white", vie=vies_initiales)
    
    # Définir le niveau de difficulté pour la balle
    balle.set_niveau(dif)  # dif vient du curseur

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
    def afficher_vies():
        """ Fonction qui affiche les vies restantes sous forme de cœurs """
        # Effacer les anciens cœurs et le texte
        caneva.delete("coeurs")
        # Afficher "Niveau X" au centre
        caneva.create_text(largeur // 2, 25, text=f"Niveau {dif}", fill="white", 
                          font=("Arial", 16, "bold"), tags="coeurs")
        # Afficher le texte "Vies : " suivi des cœurs à gauche
        caneva.create_text(20, 25, text="Vies :", fill="white", 
                          font=("Arial", 14), anchor="w", tags="coeurs")
        # Afficher les nouveaux cœurs
        for i in range(balle.vie):
            caneva.create_text(80 + i*25, 25, text="♥", fill="red", 
                             font=("Arial", 20), tags="coeurs")

    def game_loop():
        global score
        nonlocal ball_attached
        dt = 1 / 60.0  # approximativement 60 FPS
        
        # Mettre à jour l'affichage des vies
        afficher_vies()

        if ball_attached:
            # garde la balle au centre du pad
            balle.pos(pad.x + pad.largeur / 2, pad.y - balle.rayon - 1)
        else:
            # mise à jour de la physique qui sont dans balle.py
            vie_perdue = balle.update(dt, (largeur, hauteur))
            if vie_perdue:
                # Une vie a été perdue
                if balle.vie > 0:
                    # S'il reste des vies, réattacher la balle au pad
                    ball_attached = True
                    balle.pos(pad.x + pad.largeur / 2, pad.y - balle.rayon - 1)
                    # Mettre à jour l'affichage des vies
                    afficher_vies()
                else:
                    # Fin de partie
                    caneva.create_text(largeur // 2, hauteur // 2 + 40,
                       text="Tu pues le chameau mort �💀 ton score est de " + str(score),
                       fill="white",
                       font=("Helvetica", 28, "italic"))
                    # Créer un bouton pour rejouer
                    replay_button = tk.Button(Fenetre, text="Rejouer", command=lambda: [caneva.delete("all"), jeu()], 
                                           bg="#333", fg="white", font=("Helvetica", 16))
                    caneva.create_window(largeur/2, hauteur/2 + 100, window=replay_button)
                    return  # Arrêter la boucle de jeu
            else:
                # collision entre le pad et la balle 
                balle.rebond_brique(pad.x, pad.y, pad.largeur, pad.hauteur)

                # collision briques : si rebond contre une brique -> suppression
                for b in briques[:]:
                    if balle.rebond_brique(b.x, b.y, b.largeur, b.hauteur):
                        if b.id is not None:
                            caneva.delete(b.id)
                            briques.remove(b)
                            score += 10
                            balle.vitX += 40
                            balle.vitY += 40

    
        balle.affichage(caneva)
        # afficher gagner si il n'y a plus de brique 
        if len(briques) == 0: 
            # Fond semi-transparent
            caneva.create_rectangle(0, 0, largeur, hauteur, fill="#000000", stipple="gray50")

            # Message GAGNER en haut
            caneva.create_text(largeur // 2, hauteur // 2 - 100,
                       text="GAGNER !",
                       fill="#FFCA0C",
                       font=("Helvetica", 64, "bold"))
            
            # Score en dessous
            caneva.create_text(largeur // 2, hauteur // 2,
                       text="Score : " + str(score),
                       fill="#FAF1CE",
                       font=("Helvetica", 48, "bold"))
            
            # Boutons
            retry_button = tk.Button(Fenetre, text="Rejouer", font=("Helvetica", 16, "bold"), 
                                   bg="#333", fg="white", command=lambda: [caneva.delete("all"), jeu()])
            menu_button = tk.Button(Fenetre, text="Menu", font=("Helvetica", 16, "bold"), 
                                  bg="#333", fg="white", command=retour_menu)
            
            # Positionner les boutons côte à côte
            caneva.create_window(largeur // 2 - 80, hauteur // 2 + 100, window=retry_button)
            caneva.create_window(largeur // 2 + 80, hauteur // 2 + 100, window=menu_button)
            
            enregistrer_score()
            return  # Arrêter la boucle de jeu
        # continuer ou afficher game over si vies épuisées
        if balle.vie > 0:
            Fenetre.after(int(dt * 1000), game_loop)

        

        else:           
            # Fond semi-transparent
            caneva.create_rectangle(0, 0, largeur, hauteur, fill="#000000", stipple="gray50")

            # Conserver les boutons Menu et Quitter visibles
            menu_button = tk.Button(Fenetre, text="Menu", command=retour_menu, bg="#333", fg="white", font=("Helvetica", 12))
            quit_button = tk.Button(Fenetre, text="Quitter", command=Fenetre.quit, bg="#333", fg="white", font=("Helvetica", 12))
            caneva.create_window(largeur - 100, 30, window=menu_button)
            caneva.create_window(largeur - 30, 30, window=quit_button)

            # Message principal
            caneva.create_text(largeur // 2, hauteur // 2 - 30,
                       text="GAME OVER",
                       fill="#FF0000",
                       font=("Helvetica", 64, "bold"))

            # Message secondaire humoristique
            caneva.create_text(largeur // 2, hauteur // 2 + 40,
                       text="Tu pues le chameau mort 🐫💀 ton score est de " + str(score),
                       fill="white",
                       font=("Helvetica", 28, "italic"))

            # Bouton pour relancer s
            retry_button = tk.Button(Fenetre, text="Rejouer", font=("Helvetica", 16, "bold"), bg="#333", fg="white", command=lambda: jeu())
            caneva.create_window(largeur // 2, hauteur // 2 + 100, window=retry_button)
            enregistrer_score()

    # start updates
    pad.update()
    game_loop()

(largeur,hauteur) =(1000,700)

Fenetre = tk.Tk()
Fenetre.title("Casses briques")
Fenetre.resizable(False, False)  # Empêche le redimensionnement

 # Chemin de l'image du menu
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

score_frame = tk.Frame(caneva, bg="#C1B7B7", width=150, height=300) # cadre pour les scores
score_frame.pack_propagate(False) # empêche le redimensionnement automatique car trop compliqué pour nous 
title_label = tk.Label(score_frame, text="High Scores", fg="#000000",bg="#C1B7B7", font=("Lucida Console", 10)) # titre des scores
title_label.pack(pady=(10, 2))

scores.sort()

X = 0 
if len(scores) < 7:
    X = range(len(scores))
else :
    X = range(7)

for i in X: 
    lbl = tk.Label(score_frame, text=str(scores[-(i+1)]), fg="#000000",bg="#C1B7B7", font=("Lucida Console", 20))
    lbl.pack(anchor="w", pady=2)

# Placer les widgets sur le canevas
caneva.create_window(900, 500, window=score_frame)  # x=800, y=200 ce sont les coordonées du centre du cadre
caneva.create_window(500, 250, window=subtitle) 
caneva.create_window(500, 600, window=texte)
caneva.create_window(500, 350, window=play_button)
caneva.create_window(500, 650, window=curseur)

Fenetre.mainloop()