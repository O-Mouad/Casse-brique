class File:
    """
    Implémentation d'une structure de file (FIFO - First In First Out)
    pour gérer la séquence des niveaux
    """
    def __init__(self):
        self.elements = []
    
    def enfiler(self, element):
        """Ajoute un élément à la fin de la file"""
        self.elements.append(element)
    
    def defiler(self):
        """Retire et retourne le premier élément de la file"""
        if not self.est_vide():
            return self.elements.pop(0)
        return None
    
    def est_vide(self):
        """Vérifie si la file est vide"""
        return len(self.elements) == 0
    
    def taille(self):
        """Retourne le nombre d'éléments dans la file"""
        return len(self.elements)
    
    def premier(self):
        """Retourne le premier élément sans le retirer"""
        if not self.est_vide():
            return self.elements[0]
        return None

class Pile:
    """
    Implémentation d'une structure de pile (LIFO - Last In First Out)
    pour gérer l'historique des scores
    """
    def __init__(self, taille_max=7):
        self.elements = []
        self.taille_max = taille_max
    
    def empiler(self, element):
        """Ajoute un élément au sommet de la pile"""
        if len(self.elements) >= self.taille_max:
            self.elements.pop(0)  # Retire le plus ancien score si la pile est pleine
        self.elements.append(element)
    
    def depiler(self):
        """Retire et retourne l'élément au sommet de la pile"""
        if not self.est_vide():
            return self.elements.pop()
        return None
    
    def est_vide(self):
        """Vérifie si la pile est vide"""
        return len(self.elements) == 0
    
    def sommet(self):
        """Retourne l'élément au sommet sans le retirer"""
        if not self.est_vide():
            return self.elements[-1]
        return None
    
    def get_scores_tries(self):
        """Retourne une liste triée des scores (du plus grand au plus petit)"""
        return sorted(self.elements, reverse=True)