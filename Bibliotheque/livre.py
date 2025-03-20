import datetime


class Livre:
    """
    Classe représentant un livre dans une bibliothèque.
    Cette classe est développée selon l'approche Outside-In (BDD).
    """

    def __init__(self, titre, isbn):
        """
        Initialise un nouveau livre avec un titre et un ISBN.
        """
        self._titre = titre
        self._isbn = isbn
        self._statut = "Disponible"
        self._emprunteur = None
        self._date_retour = None

    @property
    def titre(self):
        return self._titre

    @property
    def isbn(self):
        return self._isbn

    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, statut):
        self._statut = statut

    @property
    def emprunteur(self):
        return self._emprunteur

    @emprunteur.setter
    def emprunteur(self, membre):
        self._emprunteur = membre

    @property
    def date_retour(self):
        return self._date_retour

    @date_retour.setter
    def date_retour(self, date):
        self._date_retour = date

    def est_disponible(self):
        """
        Vérifie si le livre est disponible pour emprunt.
        """
        return self._statut == "Disponible"

    def emprunter(self, membre):
        """
        Marque le livre comme emprunté par un membre.
        """
        if not self.est_disponible():
            raise ValueError(f"Le livre {self._titre} n'est pas disponible")

        self._statut = "Emprunté"
        self._emprunteur = membre
        self._date_retour = datetime.date.today() + datetime.timedelta(days=21)
        return True

    def retourner(self):
        """
        Marque le livre comme retourné et disponible.
        """
        if self._statut != "Emprunté":
            raise ValueError(f"Le livre {self._titre} n'est pas emprunté")

        self._statut = "Disponible"
        self._emprunteur = None
        self._date_retour = None
        return True