"""
Mouad Ouamane
Sacha Bargoin 
TP4 09/10/2025 , 16/10/2025 , 23/10/2025
fichier de la classe balle 

Amélioration : ajouter des méthodes pour la balle
"""
from typing import Tuple, Optional


class Balle:
    """Classe représentant la balle du casse-briques.

    Conçue pour être utilisée avec Tkinter (un `tk.Canvas`), mais
    indépendante de l'affichage : expose `update()` pour la physique
    et `draw(canvas)` pour l'affichage.
    """

    def __init__(self,
                 pos: Tuple[float, float] = (0.0, 0.0),
                 vel: Tuple[float, float] = (0.0, 0.0),
                 acc: Tuple[float, float] = (0.0, 0.0),
                 rayon: int = 8,
                 vie: int = 1,
                 couleur: str = "white") -> None:
        self.vie: int = vie
        self.posX: float = float(pos[0])
        self.posY: float = float(pos[1])
        self.vitX: float = float(vel[0])
        self.vitY: float = float(vel[1])
        self.aX: float = float(acc[0])
        self.aY: float = float(acc[1])

        self.rayon: int = rayon
        self.couleur: str = couleur
        # id de l'oval sur le Canvas (si utilisé)
        self._canvas_id: Optional[int] = None

    def pos(self, x: float, y: float) -> None:
        """Place la balle à la position (x, y)."""
        self.posX = float(x)
        self.posY = float(y)

    def set_velocity(self, vx: float, vy: float) -> None:
        """Définit la vitesse de la balle."""
        self.vitX = float(vx)
        self.vitY = float(vy)

    def update(self, dt: float, bounds: Tuple[int, int]) -> None:
        """Met à jour la position et gère les collisions simples contre
        les bords du canevas.

        - dt : pas de temps en secondes
        - bounds : (largeur, hauteur) du canevas
        """
        # appliquer accélération
        self.vitX += self.aX * dt
        self.vitY += self.aY * dt

        # mise à jour position
        self.posX += self.vitX * dt
        self.posY += self.vitY * dt

        largeur, hauteur = bounds

        # collisions gauche/droite
        if self.posX - self.rayon < 0:
            self.posX = self.rayon
            self.vitX = -self.vitX

        if self.posX + self.rayon > largeur:
            self.posX = largeur - self.rayon
            self.vitX = -self.vitX

        # collision haut
        if self.posY - self.rayon < 0:
            self.posY = self.rayon
            self.vitY = -self.vitY

        # si la balle est passée en dessous du bas, on décrémente la vie
        if self.posY - self.rayon > hauteur:
            self.vie -= 1

    def draw(self, canvas) -> None:
        """Dessine ou met à jour la représentation de la balle sur un tk.Canvas.

        Si `canvas` n'est pas un Canvas (p.ex. lors de tests), la méthode
        échoue silencieusement.
        """
        x0 = self.posX - self.rayon
        y0 = self.posY - self.rayon
        x1 = self.posX + self.rayon
        y1 = self.posY + self.rayon

        if self._canvas_id is None:
            try:
                self._canvas_id = canvas.create_oval(x0, y0, x1, y1, fill=self.couleur, outline=self.couleur)
            except Exception:
                self._canvas_id = None
        else:
            try:
                canvas.coords(self._canvas_id, x0, y0, x1, y1)
            except Exception:
                self._canvas_id = None

    def reset(self, pos: Tuple[float, float], vel: Tuple[float, float] = (0.0, 0.0)) -> None:
        """Réinitialise la position et la vitesse de la balle."""
        self.posX, self.posY = float(pos[0]), float(pos[1])
        self.vitX, self.vitY = float(vel[0]), float(vel[1])

    def intersects_rect(self, rx: float, ry: float, rwidth: float, rheight: float) -> bool:
        """Teste la collision cercle-rectangle (approximation AABB).

        Renvoie True si la balle intersecte le rectangle défini par
        (rx, ry, rwidth, rheight).
        """
        closest_x = max(rx, min(self.posX, rx + rwidth))
        closest_y = max(ry, min(self.posY, ry + rheight))

        dx = self.posX - closest_x
        dy = self.posY - closest_y
        return (dx * dx + dy * dy) <= (self.rayon * self.rayon)
