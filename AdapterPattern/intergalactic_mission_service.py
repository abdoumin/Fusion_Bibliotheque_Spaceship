# integration/models.py
from typing import Optional, List, Dict
import datetime

from AdapterPattern.bibliotheque_spatiale import BibliothequeSpatiale
from AdapterPattern.member_pilote import MembrePilote


class IntergalacticMissionService:
    """Service managing space missions for knowledge exchange"""

    def __init__(self, bibliotheque_spatiale: BibliothequeSpatiale):
        self.bibliotheque = bibliotheque_spatiale
        self.active_missions = {}  # mission_id -> mission_details
        self.mission_counter = 0
        self.last_error = None  # Pour stocker le dernier message d'erreur

    def prepare_mission(self, spaceship_name: str, pilot_membre: MembrePilote, destination: str,
                        books_to_transport: list) -> Optional[int]:
        """
        Prepare an intergalactic knowledge exchange mission
        Returns mission ID if successful, None otherwise
        """
        # Reset last error
        self.last_error = None

        # Check if spaceship is available
        spaceship_adapter = self.bibliotheque.get_spaceship(spaceship_name)
        if not spaceship_adapter or not spaceship_adapter.est_disponible():
            self.last_error = "Vaisseau non disponible"
            return None

        # Check if member is qualified
        if not pilot_membre.can_pilot(spaceship_adapter):
            self.last_error = "Niveau de qualification insuffisant"
            return None

        # Check if all books are available
        for book in books_to_transport:
            if not book.est_disponible():
                self.last_error = f"Livre {book.titre} non disponible"
                return None

        # Borrow spaceship and books
        if not self.bibliotheque.borrow_spaceship(spaceship_name, pilot_membre):
            self.last_error = "Échec de l'emprunt du vaisseau"
            return None

        for book in books_to_transport:
            book.emprunter(pilot_membre)

        # Create mission
        self.mission_counter += 1
        mission_id = self.mission_counter

        mission_details = {
            "id": mission_id,
            "pilot": pilot_membre,
            "spaceship": spaceship_adapter,
            "destination": destination,
            "books": books_to_transport,
            "departure_date": datetime.date.today(),
            "status": "Preparing"
        }

        self.active_missions[mission_id] = mission_details
        return mission_id

    def launch_mission(self, mission_id: int) -> bool:
        """Launch a prepared mission"""
        if mission_id not in self.active_missions:
            self.last_error = "Mission non trouvée"
            return False

        mission = self.active_missions[mission_id]
        if mission["status"] != "Preparing":
            self.last_error = f"Mission dans un état incorrect: {mission['status']}"
            return False

        # Calculate fuel needed based on books and destination
        fuel_needed = 10 + (len(mission["destination"]) % 20) + (len(mission["books"]) * 5)

        # Launch the spaceship's mission
        spaceship_adapter = mission["spaceship"]
        result = spaceship_adapter.spaceship.travel(fuel_needed)
        if "a voyagé" in result:  # Success indication
            mission["status"] = "In Progress"

            # Log flight hours for the pilot
            flight_hours = len(mission["destination"]) / 10
            mission["pilot"].log_flight_hours(flight_hours)
            return True
        else:
            mission["status"] = "Failed - Insufficient Fuel"
            self.last_error = "Carburant insuffisant"
            return False

    def complete_mission(self, mission_id: int) -> bool:
        """Mark a mission as completed and return resources"""
        if mission_id not in self.active_missions:
            self.last_error = "Mission non trouvée"
            return False

        mission = self.active_missions[mission_id]
        if mission["status"] != "In Progress":
            self.last_error = f"Mission dans un état incorrect: {mission['status']}"
            return False

        # Return spaceship
        spaceship_adapter = mission["spaceship"]
        spaceship_name = spaceship_adapter.spaceship.name

        self.bibliotheque.return_spaceship(spaceship_name, mission["pilot"])

        # Return books with new knowledge
        for book in mission["books"]:
            try:
                # Vérifier si le livre peut être retourné
                if book.statut == "Emprunté" and book.emprunteur == mission["pilot"]:
                    book.retourner()
                else:
                    # Si le livre n'est pas emprunté, simplement s'assurer qu'il est disponible
                    book.statut = "Disponible"
                    book.emprunteur = None
                    book.date_retour = None

                # Add a note about intergalactic journey (if the book class supports it)
                if hasattr(book, 'add_note'):
                    book.add_note(f"This book traveled to {mission['destination']}!")
            except Exception as e:
                print(f"AVERTISSEMENT lors du retour du livre {book.titre}: {str(e)}")

        mission["status"] = "Completed"
        return True