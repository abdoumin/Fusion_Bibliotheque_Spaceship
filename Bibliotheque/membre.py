# membre.py
class Membre:
    """Classe représentant un membre de la bibliothèque."""

    def __init__(self, nom, numero):
        self._nom = nom
        self._numero = numero
        self._emprunts = []

    @property
    def nom(self):
        return self._nom

    @property
    def numero(self):
        return self._numero

    @property
    def emprunts(self):
        return self._emprunts

    def ajouter_emprunt(self, livre):
        self._emprunts.append(livre)

    def supprimer_emprunt(self, livre):
        if livre in self._emprunts:
            self._emprunts.remove(livre)