from ObserverPattern.library_monitor import LibraryMonitor
from ObserverPattern.spaceship import Spaceship


class DeliverySystem:
    """Facade for setting up the entire observer system"""

    def __init__(self):
        """Initialise le système de livraison"""
        self.active_missions = {}  # title -> {spaceship, book_info, status}
        self.completed_missions = {}  # title -> {spaceship, book_info, status}
        self.delivery_log = []  # Journal de toutes les activités


    @staticmethod
    def initialize(bibliotheque) -> LibraryMonitor:
        """Initialize the library monitoring system"""
        monitor = LibraryMonitor(bibliotheque)
        print(f"Monitoring initialized for library: {bibliotheque.nom}")
        return monitor

    @staticmethod
    def register_spaceship(monitor: LibraryMonitor, ship: Spaceship) -> None:
        """Register a spaceship with the library monitor"""
        monitor.add_observer(ship)
        print(f"Spaceship {ship.name} registered for delivery missions")

    def assign_mission(self, book_info, spaceships):
        """Attribue une mission de livraison au vaisseau le plus adapté

        Args:
            book_info: Informations sur le livre à livrer
            spaceships: Liste des vaisseaux disponibles

        Returns:
            dict: Résultat de l'attribution avec les clés 'success', 'spaceship', 'message'
        """
        # Vérifier s'il y a des vaisseaux
        if not spaceships:
            self._log(f"Aucun vaisseau disponible pour livrer {book_info.title}")
            return {'success': False, 'spaceship': None, 'message': "Aucun vaisseau disponible"}

        # Trouver le meilleur vaisseau pour cette mission
        suitable_ships = []
        for ship in spaceships:
            if ship.can_fulfill_mission(book_info):
                suitable_ships.append(ship)

        if not suitable_ships:
            self._log(f"Aucun vaisseau capable de livrer {book_info.title}")
            return {'success': False, 'spaceship': None, 'message': "Aucun vaisseau adapté"}

        # Sélection du meilleur vaisseau (celui avec le plus de carburant)
        # Dans un système plus sophistiqué, vous pourriez avoir une logique plus complexe
        best_ship = max(suitable_ships, key=lambda ship: ship.fuel_level)

        # Attribuer la mission
        success = best_ship.accept_mission(book_info)

        if success:
            self.active_missions[book_info.title] = {
                'spaceship': best_ship,
                'book_info': book_info,
                'status': 'assigned'
            }
            self._log(f"Mission attribuée: {book_info.title} à {best_ship.name}")

            return {'success': True, 'spaceship': best_ship, 'message': "Mission attribuée avec succès"}
        else:
            self._log(f"Échec d'attribution: {book_info.title} à {best_ship.name}")
            return {'success': False, 'spaceship': best_ship, 'message': "Le vaisseau n'a pas accepté la mission"}

    def verify_book_delivered(self, book_title):
        """Vérifie si un livre a été livré

        Args:
            book_title: Le titre du livre à vérifier

        Returns:
            bool: True si le livre a été livré, False sinon
        """
        return (book_title in self.completed_missions and
                self.completed_missions[book_title]['status'] == 'completed')

    def record_mission_completion(self, book_info, spaceship):
        """Enregistre la fin d'une mission de livraison

        Args:
            book_info: Informations sur le livre livré
            spaceship: Le vaisseau qui a effectué la livraison

        Returns:
            bool: True si l'enregistrement a réussi, False sinon
        """
        if book_info.title not in self.active_missions:
            self._log(f"Impossible de terminer une mission inexistante: {book_info.title}")
            return False

        # Déplacer de active_missions à completed_missions
        mission_data = self.active_missions.pop(book_info.title)
        mission_data['status'] = 'completed'
        self.completed_missions[book_info.title] = mission_data

        self._log(f"Mission terminée: {book_info.title} par {spaceship.name}")
        return True

    def _log(self, message):
        """Ajoute une entrée au journal

        Args:
            message: Le message à journaliser
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.delivery_log.append(log_entry)
        print(log_entry)

    def get_mission_status(self, book_title):
        """Récupère le statut d'une mission

        Args:
            book_title: Le titre du livre

        Returns:
            dict: Statut de la mission ou None si non trouvée
        """
        if book_title in self.active_missions:
            return {'active': True, **self.active_missions[book_title]}
        elif book_title in self.completed_missions:
            return {'active': False, **self.completed_missions[book_title]}
        return None

    def reassign_mission(self, book_info, available_ships, exclude_ships=None):
        """Réattribue une mission à un autre vaisseau

        Args:
            book_info: Informations sur le livre à livrer
            available_ships: Liste des vaisseaux disponibles
            exclude_ships: Liste des vaisseaux à exclure

        Returns:
            dict: Résultat de l'attribution
        """
        if exclude_ships is None:
            exclude_ships = []

        # Filtrer les vaisseaux exclus
        eligible_ships = [ship for ship in available_ships if ship not in exclude_ships]

        return self.assign_mission(book_info, eligible_ships)
