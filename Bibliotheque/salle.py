import datetime


class Salle:
    """
    Classe représentant une salle de travail dans une bibliothèque.
    Cette classe est développée selon l'approche Outside-In (BDD).
    """

    def __init__(self, code, capacite):
        """
        Initialise une nouvelle salle avec un code et une capacité.
        """
        self._code = code
        self._capacite = capacite
        self._reservations = {}  # date -> {heure_debut -> (heure_fin, utilisateur, code)}

    @property
    def code(self):
        return self._code

    @property
    def capacite(self):
        return self._capacite

    def est_disponible(self, date):
        """
        Vérifie si la salle a des réservations pour une date donnée.
        """
        return date not in self._reservations or len(self._reservations[date]) == 0

    def est_disponible_pour_creneau(self, debut, fin):
        """
        Vérifie si la salle est disponible pour un créneau horaire donné.
        """
        if debut.date() != fin.date():
            raise ValueError("Les réservations doivent être sur la même journée")

        date = debut.date()
        if date not in self._reservations:
            return True

        for heure_debut_res, (heure_fin_res, _, _) in self._reservations[date].items():
            # Vérifier si les créneaux se chevauchent
            if (debut <= heure_fin_res and fin >= heure_debut_res):
                return False

        return True

    def ajouter_reservation(self, debut, fin, utilisateur, code_reservation):
        """
        Ajoute une réservation pour cette salle.
        """
        if not self.est_disponible_pour_creneau(debut, fin):
            raise ValueError("Créneau déjà occupé")

        date = debut.date()
        if date not in self._reservations:
            self._reservations[date] = {}

        self._reservations[date][debut] = (fin, utilisateur, code_reservation)
        return True

    def supprimer_reservation(self, code_reservation):
        """
        Supprime une réservation par son code.
        """
        for date, reservations in list(self._reservations.items()):
            for debut, (fin, utilisateur, code) in list(reservations.items()):
                if code == code_reservation:
                    del self._reservations[date][debut]
                    if len(self._reservations[date]) == 0:
                        del self._reservations[date]
                    return True

        return False

    def trouver_reservation(self, code_reservation):
        """
        Trouve les détails d'une réservation par son code.
        """
        for date, reservations in self._reservations.items():
            for debut, (fin, utilisateur, code) in reservations.items():
                if code == code_reservation:
                    return {
                        'date': date,
                        'debut': debut,
                        'fin': fin,
                        'utilisateur': utilisateur,
                        'code': code
                    }

        return None