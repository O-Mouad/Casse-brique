"""
Mouad Ouamane
Sacha Bargoin 
Groupe C
TP4 Casse briques 09/10/2025 , 16/10/2025 , 23/10/2025 

fichier main qui gère le deroulement du jeu et toutes les interactions entre les différentes classes

Amélioration possible : - ajouter des niveaux bonus
                        - mettre les messages de victoire et de défaites de manieres interactive ( en mouvement par exemple )
                        - faire en sorte que le caneva soit redimensionnable et qu'il prenne tout l'écran ( super compliqué )
                        - ajouter une bande son ou des effets sonores pour le menu et le jeu 
                        - réorganiser le code en plusieurs fichiers pour une meilleure lisibilité 
                        - configurer le jeu pour pouvoir jouer avec différents périphériques 
                        - rajouter des bonus ( voir class pad.py pour les idées de bonus et malus ) 
                        
"""

# Imports standard
import os
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk

# Imports locaux
from classes.briques import Brique
from classes.balle import Balle
from classes.pad import Pad
from classes.structures import File, Pile

# Constantes globales
LARGEUR, HAUTEUR = 1000, 700
NIVEAU_MIN, NIVEAU_MAX = 1, 15
TAILLE_PAD_MIN, TAILLE_PAD_MAX = 60, 180
TAILLE_PAD_DEFAUT = 120
MAX_SCORES_AFFICHES = 7

# Structures de données
niveaux = File()  # File pour gérer la progression des niveaux
scores_historique = Pile(MAX_SCORES_AFFICHES)  # Pile pour gérer les scores

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

# Initialisation des scores depuis le fichier
def charger_scores():
    """Charge les scores depuis le fichier score.txt dans la pile des scores"""
    try:
        with open("score.txt", "r") as f:
            for ligne in f:
                score = int(ligne.strip())
                scores_historique.empiler(score)
    except FileNotFoundError:
        # Créer le fichier s'il n'existe pas
        with open("score.txt", "w") as f:
            f.write("0\n")
        scores_historique.empiler(0)

def enregistrer_scores():
    """Enregistre les scores de la pile dans le fichier score.txt"""
    with open("score.txt", "w") as f:
        for score in scores_historique.elements:
            f.write(f"{score}\n")

def initialiser_niveaux(difficulte):
    """Initialise la file des niveaux en fonction de la difficulté choisie"""
    niveaux.elements.clear()
    niveau_actuel = difficulte
    # Ajoute 3 niveaux à la file, en augmentant progressivement la difficulté
    for i in range(3):
        niveaux.enfiler({
            'niveau': niveau_actuel + i,
            'nb_briques': 9 * (niveau_actuel + i),
            'vitesse_balle': 200 + (niveau_actuel + i) * 20
        })

# Score global pour la partie en cours
score = 0

# Chargement initial des scores
charger_scores()

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
    caneva.create_window(500, 550, window=texte_pad)
    caneva.create_window(500, 600, window=texte)
    caneva.create_window(500, 350, window=play_button)
    caneva.create_window(500, 580, window=curseur_pad)
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

    # Création du pad avec la taille choisie dans le menu
    taille_pad = curseur_pad.get()
    pad = Pad(caneva, 440, 650, largeur=taille_pad)  # position au bas de l'écran
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
            
            scores_historique.empiler(score)
            enregistrer_scores()
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

            # Bouton pour relancer
            retry_button = tk.Button(Fenetre, text="Rejouer", font=("Helvetica", 16, "bold"), 
                                   bg="#333", fg="white", command=lambda: jeu())
            caneva.create_window(largeur // 2, hauteur // 2 + 100, window=retry_button)
            scores_historique.empiler(score)
            enregistrer_scores()

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
texte_pad = tk.Label(Fenetre, text="taille du pad:")
play_button = tk.Button(Fenetre, text="Jouer", command=lambda: jeu())

curseur_pad = tk.Scale(
    caneva,             # parent
    from_=60, to=180,   # bornes (taille min et max du pad)
    orient='horizontal', # orientation
    length=300,         # longueur du slider
    )
curseur_pad.set(120)    # taille par défaut du pad

curseur = tk.Scale(
    caneva,             # parent
    from_=1, to=15,     # bornes
    orient='horizontal', # orientation
    length=300,         # longueur du slider 
    )

# Création du cadre des high scores
score_frame = tk.Frame(caneva, bg="#C1B7B7", width=150, height=300)
score_frame.pack_propagate(False)
title_label = tk.Label(score_frame, text="High Scores", fg="#000000", bg="#C1B7B7", 
                      font=("Lucida Console", 10))
title_label.pack(pady=(10, 2))

# Affichage des meilleurs scores
scores_tries = scores_historique.get_scores_tries()
for score in scores_tries[:MAX_SCORES_AFFICHES]:
    lbl = tk.Label(score_frame, text=str(score), fg="#000000", bg="#C1B7B7", 
                  font=("Lucida Console", 20))
    lbl.pack(anchor="w", pady=2)

# Placer les widgets sur le canevas
caneva.create_window(900, 500, window=score_frame)  # x=800, y=200 ce sont les coordonées du centre du cadre
caneva.create_window(500, 250, window=subtitle) 
caneva.create_window(500, 550, window=texte_pad)   # Label pour la taille du pad
caneva.create_window(500, 600, window=texte)       # Label pour la difficulté
caneva.create_window(500, 350, window=play_button)
caneva.create_window(500, 580, window=curseur_pad) # Curseur pour la taille du pad
caneva.create_window(500, 650, window=curseur)     # Curseur pour la difficulté

Fenetre.mainloop()