# systeme_reservation.py
import datetime
import random
import string


class SystemeReservation:
    """Classe gérant les réservations de salles."""

    def __init__(self):
        self._salles = {}  # code_salle -> objet Salle
        self._reservations = {}  # code_reservation -> (salle, utilisateur)
        self._heures_ouverture = (9, 18)  # (heure_debut, heure_fin)

    def ajouter_salle(self, salle):
        """Ajoute une salle au système."""
        if salle.code in self._salles:
            raise ValueError(f"Une salle avec le code {salle.code} existe déjà")
        self._salles[salle.code] = salle

    def set_heures_ouverture(self, heure_debut, heure_fin):
        """Définit les heures d'ouverture."""
        if heure_debut >= heure_fin:
            raise ValueError("L'heure de début doit être antérieure à l'heure de fin")
        self._heures_ouverture = (heure_debut, heure_fin)

    def _generer_code_reservation(self, longueur=8):
        """Génère un code de réservation aléatoire."""
        caracteres = string.ascii_uppercase + string.digits
        code = 'RES' + ''.join(random.choice(caracteres) for _ in range(longueur))
        return code

    def _valider_creneau(self, debut, fin):
        """Valide qu'un créneau horaire est acceptable."""
        # Vérifier que début et fin sont le même jour
        if debut.date() != fin.date():
            raise ValueError("Les réservations doivent être sur la même journée")

        # Vérifier que le créneau est dans les heures d'ouverture
        heure_debut, heure_fin = self._heures_ouverture
        if debut.hour < heure_debut or fin.hour > heure_fin:
            raise ValueError(f"Les réservations sont possibles uniquement entre {heure_debut}h et {heure_fin}h")

        # Vérifier que la durée est raisonnable
        if (fin - debut).seconds < 30 * 60:  # Minimum 30 minutes
            raise ValueError("La durée minimale de réservation est de 30 minutes")

        # Vérifier que la réservation n'est pas dans le passé
        if debut < datetime.datetime.now():
            raise ValueError("Impossible de réserver dans le passé")

    def reserver_salle(self, salle, utilisateur, debut, fin):
        """Réserve une salle pour un utilisateur sur un créneau donné."""
        # Vérifier que la salle existe
        if salle.code not in self._salles:
            raise ValueError(f"Salle {salle.code} inconnue")

        # Valider le créneau horaire
        self._valider_creneau(debut, fin)

        # Vérifier la disponibilité
        if not salle.est_disponible_pour_creneau(debut, fin):
            raise ValueError("Créneau déjà occupé")

        # Générer un code de réservation unique
        code = self._generer_code_reservation()
        while code in self._reservations:
            code = self._generer_code_reservation()

        # Ajouter la réservation
        salle.ajouter_reservation(debut, fin, utilisateur, code)
        self._reservations[code] = (salle, utilisateur)
        utilisateur.ajouter_reservation(code)

        return code

    def annuler_reservation(self, code_reservation):
        """Annule une réservation par son code."""
        if code_reservation not in self._reservations:
            raise ValueError(f"Réservation {code_reservation} inconnue")

        salle, utilisateur = self._reservations[code_reservation]

        # Supprimer la réservation de la salle
        if salle.supprimer_reservation(code_reservation):
            # Supprimer la réservation de l'utilisateur
            utilisateur.supprimer_reservation(code_reservation)
            # Supprimer la réservation du système
            del self._reservations[code_reservation]
            return True

        return False

    def reservation_existe(self, code_reservation):
        """Vérifie si une réservation existe."""
        return code_reservation in self._reservations

    def get_reservations_utilisateur(self, utilisateur):
        """Récupère toutes les réservations d'un utilisateur."""
        reservations = []
        for code in utilisateur.reservations:
            if code in self._reservations and self._reservations[code][1] == utilisateur:
                salle = self._reservations[code][0]
                details = salle.trouver_reservation(code)
                if details:
                    reservations.append(details)
        return reservations

    def get_reservations_salle(self, code_salle, date=None):
        """Récupère toutes les réservations pour une salle à une date donnée."""
        if code_salle not in self._salles:
            raise ValueError(f"Salle {code_salle} inconnue")

        salle = self._salles[code_salle]

        # Si aucune date n'est spécifiée, utiliser la date d'aujourd'hui
        if date is None:
            date = datetime.date.today()

        reservations = []
        for code, (s, utilisateur) in self._reservations.items():
            if s == salle:
                details = salle.trouver_reservation(code)
                if details and details['date'] == date:
                    reservations.append(details)

        return reservations

    def forcer_code_reservation(self, salle, utilisateur, code):
        """
        Force un code de réservation spécifique (uniquement pour les tests).
        """
        # On suppose que cette méthode n'est utilisée que dans un contexte de test
        # et qu'elle simule une réservation existante
        self._reservations[code] = (salle, utilisateur)
        utilisateur.ajouter_reservation(code)

        # On simule également une entrée dans la salle
        demain = datetime.date.today() + datetime.timedelta(days=1)
        debut = datetime.datetime.combine(demain, datetime.time(9, 0))
        fin = datetime.datetime.combine(demain, datetime.time(11, 0))

        if demain not in salle._reservations:
            salle._reservations[demain] = {}

        salle._reservations[demain][debut] = (fin, utilisateur, code)