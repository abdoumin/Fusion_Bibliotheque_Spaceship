# utilisateur.py
class Utilisateur:
    """Classe représentant un utilisateur de la bibliothèque."""

    def __init__(self, nom, identifiant):
        self._nom = nom
        self._identifiant = identifiant
        self._reservations = []  # Liste des codes de réservation

    @property
    def nom(self):
        return self._nom

    @property
    def identifiant(self):
        return self._identifiant

    @property
    def reservations(self):
        return self._reservations.copy()

    def ajouter_reservation(self, code_reservation):
        self._reservations.append(code_reservation)

    def supprimer_reservation(self, code_reservation):
        if code_reservation in self._reservations:
            self._reservations.remove(code_reservation)
            return True
        return False