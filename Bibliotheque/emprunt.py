# emprunt.py
class SystemeEmprunt:
    """Classe gérant les emprunts de livres."""

    def __init__(self):
        self._emprunts_actifs = {}


    def emprunter_livre(self, livre, membre):
        """Enregistre l'emprunt d'un livre par un membre."""
        livre.emprunter(membre)
        membre.ajouter_emprunt(livre)
        self._emprunts_actifs[livre.isbn] = membre.numero

    def retourner_livre(self, livre):
        """Enregistre le retour d'un livre."""
        if livre.emprunteur:
            livre.emprunteur.supprimer_emprunt(livre)
            if livre.isbn in self._emprunts_actifs:
                del self._emprunts_actifs[livre.isbn]
        livre.retourner()