"""File for environnement class
"""
import random as r
import math

from ville import Ville

class Environnement:

    def __init__(self) -> None:
        self.l_ville = list()
        self.ville_actuelle = None
        self.distance_parcourue = 0
        self.villes_parcourues = list()

        self.voyage_fini = False

    def add_ville(self, p_nom: str, p_pos_x: float, p_pos_y: float):
        """Add a town to the environnement

        Args:
            p_nom (str): Name of the town
            p_pos_x (str): Coordinate of the town on x
            p_pos_y (str): Coordinate of the town on y
        """
        ville = Ville(p_nom, p_pos_x, p_pos_y)
        self.l_ville.append(ville)

    def changement_ville_actuelle(self, ville_choisie: Ville):

        self.villes_parcourues.append(ville_choisie)

        ancienne_ville = self.ville_actuelle
        self.ville_actuelle.visitee = True
        self.ville_actuelle = ville_choisie

        self.distance_parcourue += math.sqrt(
            (ancienne_ville.pos_x - self.ville_actuelle.pos_x)**2 +
            (ancienne_ville.pos_y - self.ville_actuelle.pos_y)**2
        )

        if len(self.villes_parcourues) == len(self.l_ville):
            self.voyage_fini = True

    def choix_ville(self):
        return r.choice([ville for ville in self.l_ville if ville not in self.villes_parcourues])