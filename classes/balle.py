"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025 , 16/10/2025 , 23/10/2025

fichier de la classe balle qui gère la balle et toute ses interactions 

Amélioration possible: - ajouter des méthodes pour la balle
               - ajouter un meilleur design à la balle 
               - ajouter des effets sonores 
               - ajouter une meilleure gestion des collisions avec des effets visuels 
               - faire en sorte que la balle change de couleur en fonction du niveau
               - faire en sorte que la balle accélère légèrement à chaque rebond pour augmenter la difficulté

"""
from typing import Tuple, Optional
import random


class Balle:
    
    """Classe représentant la balle du casse-briques.

    Attributs: - la position de la balle (posX, posY)
    - la vitesse de la balle (vitX, vitY)
    - l'acceleration de la balle (aX, aY)
    - le rayon de la balle (rayon)
    - la vie de la balle (vie)
    - la couleur de la balle (couleur)

    ensuite on a tout les setter pour pouvoir modifier les attributs tout au long du jeu 

    Fonctions : - position 
    - de la vitesse de la balle
    - met à jour la position de la balle 
    - draw qui afffiche la balle 
    - reset qui remet la balle à la pos et à la vitesse initiale 
    - intersects_rect qui teste la collision entre la balle et un rectangle (paddle ou brique)
    """

    def __init__(self,
                 pos: Tuple[float, float] = (0.0, 0.0), # position initiale de la balle
                 vit: Tuple[float, float] = (0.0, 0.0), # vitesse initiale de la balle
                 acc: Tuple[float, float] = (0.0, 0.0), # acceleration de la balle
                 rayon: int = 8, # rayon de la balle 
                 vie: int = 3, # vie de la balle (augmenté à 3)
                 couleur: str = "white") -> None: # couleur de la balle
        self.niveau = 1  # niveau par défaut 
        self.vie: int = vie 
        self.posX: float = float(pos[0])
        self.posY: float = float(pos[1])
        self.vitX: float = float(vit[0])
        self.vitY: float = float(vit[1])
        self.aX: float = float(acc[0])
        self.aY: float = float(acc[1])
        self.rayon: int = rayon
        self.couleur: str = couleur
        self._canvas_id: Optional[int] = None # correspond à l'ID d'un objet graphique ( balle ou bloc par exemple ) sur un canevas graphique. Initialiser a "None" car la balle n'est pas encore dessinée

    def pos(self, x: float, y: float) -> None:
        """Positionne la balle à la position (x, y).
        """
        self.posX = float(x)
        self.posY = float(y)

    def set_niveau(self, niveau: int) -> None:
        """Définit le niveau de difficulté qui affecte la vitesse de la balle."""
        self.niveau = niveau

    def set_vitesse(self, vx: float, vy: float) -> None:
        """Définit la vitesse de la balle avec une composante aléatoire et ajustée selon le niveau."""
        # Facteur de vitesse basé sur le niveau (augmentation de 15% par niveau)
        facteur_vitesse = 1.0 + (self.niveau - 1) * 0.15
        
        # Application du facteur de vitesse et ajout de l'aléatoire
        self.vitX = (float(vx) + random.uniform(-20, 20)) * facteur_vitesse
        self.vitY = (float(vy) + random.uniform(-20, 20)) * facteur_vitesse

    def update(self, dt: float, bounds: Tuple[int, int]) -> None:
        
        """Met à jour la position et gère les collisions simples contre
        les bords du canevas.

        - dt : pas de temps en secondes
        - bounds : (largeur, hauteur) du canevas
        """
        # si la diff de temps est nulle ou négative, ne rien faire
        if dt <= 0:
            return

        # appliquer accélération (on prend l'origine en haut à gauche,
        # y positif vers le bas — donc aY positive fera accélérer vers le bas)
        self.vitX += self.aX * dt
        self.vitY += self.aY * dt

        # mise à jour position en fonction de la vitesse et du temps 
        self.posX += self.vitX * dt
        self.posY += self.vitY * dt

        largeur, hauteur = bounds 

        # collisions gauche/droite (rebond simple)
        if self.posX - self.rayon < 0:
            self.posX = self.rayon
            self.vitX = -self.vitX

        if self.posX + self.rayon > largeur:
            self.posX = largeur - self.rayon
            self.vitX = -self.vitX

        # collision haut (rebond vers le bas)
        if self.posY - self.rayon < 0:
            self.posY = self.rayon
            self.vitY = -self.vitY

        # si la balle dépasse le bas du canevas -> perte de vie
        if self.posY - self.rayon > hauteur:
            self.vie -= 1
            # Réinitialiser la vitesse à 0 pour que la balle reste attachée au pad
            self.vitX = 0
            self.vitY = 0
            return True  # Indique qu'une vie a été perdue
        return False    # Pas de perte de vie

    def affichage(self, canvas) -> None:
        """Dessine ou met à jour la représentation de la balle sur un tk.Canvas.
        """
        x0 = self.posX - self.rayon 
        y0 = self.posY - self.rayon
        x1 = self.posX + self.rayon
        y1 = self.posY + self.rayon

        if self._canvas_id is None: # si la balle n'est pas dessinée 
            try: # essayer de la dessiner
                self._canvas_id = canvas.create_oval(x0, y0, x1, y1, fill=self.couleur, outline=self.couleur)
            except Exception: # en cas d'erreur ( par exemple le canvas n'existe pas ) 
                self._canvas_id = None
        else:
            try: # mettre à jour la position de la balle existante
                canvas.coords(self._canvas_id, x0, y0, x1, y1) # on met à jour les coordonnées 
            except Exception:
                self._canvas_id = None

    
    def reset(self, pos: Tuple[float, float], vel: Tuple[float, float] = (0.0, 0.0)) -> None:
        """Réinitialise la position et la vitesse de la balle.
        """
        self.posX, self.posY = float(pos[0]), float(pos[1])
        self.vitX, self.vitY = float(vel[0]), float(vel[1])

    
    def collisions_balle(self, rx: float, ry: float, rwidth: float, rheight: float) -> bool:
        """Teste la collision cercle-brique.

        Renvoie True si la balle intersecte le rectangle défini par
        (rx, ry, rwidth, rheight).
        """
        closest_x = max(rx, min(self.posX, rx + rwidth)) # coordonnée x du point le plus proche
        closest_y = max(ry, min(self.posY, ry + rheight)) # coordonnée y du point le plus proche 
       
        dx = self.posX - closest_x  # distance en x entre le center de la balle et le point le plus proche 
        dy = self.posY - closest_y  # même chose en y 
        return (dx * dx + dy * dy) <= (self.rayon * self.rayon)

    
    def rebond_brique(self, rx: float, ry: float, rwidth: float, rheight: float) -> bool:
        """ Si la balle intersecte le rectangle, on ajuste la vitesse pour simuler un rebond.
    - détecte le côté de contact par la plus petite distance entre le centre de la balle et le bord du rectangle.
    - inverse la composante de vitesse correspondante après un rebond.
    Retourne False si pas d'intersection.
    """

        if not self.collisions_balle(rx, ry, rwidth, rheight):
            return False

        # coordonnées du point le plus proche (déjà calculées dans intersects_rect
        # mais recalculées ici pour simplicité)
        closest_x = max(rx, min(self.posX, rx + rwidth)) 
        closest_y = max(ry, min(self.posY, ry + rheight))
        dx = self.posX - closest_x
        dy = self.posY - closest_y

        # déterminer côté de rebond par la plus petite distance normalisée
        # si |dx| > |dy| alors on rebondit horizontalement (inverser vitX)
        if abs(dx) > abs(dy):
            self.vitX = -self.vitX
            # Ajouter une variation aléatoire à la vitesse Y
            self.vitY += random.uniform(-200, 200)  # Réduit la variation pour plus de contrôle
            # pousser la balle hors du rectangle d'une petite marge
            if dx > 0:
                self.posX = rx + rwidth + self.rayon  # à droite
            else:
                self.posX = rx - self.rayon  # à gauche
        else:
            self.vitY = -self.vitY  # rebond vertical
            # Ajouter une variation aléatoire à la vitesse X
            self.vitX += random.uniform(-500, 500)
            # pousser la balle hors du rectangle d'une petite marge
            if dy > 0:
                self.posY = ry + rheight + self.rayon  # en bas
            else:
                self.posY = ry - self.rayon  # en haut
        return True  # rebond effectué
    

    """Casse briques de Sacha BARGOIN & Mouâd OUAMANE 

A faire fichier dans main2.py : 
  - rajouter un piles & files pour gerer les niveaux et les scores mais aussi un systeme de vie
  - ameliorer le design
  - ameliorer la gestion des collisions
  - faire en sorte que le caneva s'adapte a la taille de l'ecran
""" 