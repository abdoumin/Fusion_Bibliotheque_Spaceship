from typing import Optional

from AdapterPattern.spaceship_adapter import SpaceshipAdapter
from Bibliotheque.adresse import Adresse
from Bibliotheque.bibliotheque import Bibliotheque
from Bibliotheque.membre import Membre
from SpaceShip.spaceship_model import Spaceship


class BibliothequeSpatiale(Bibliotheque):
    """Extended Library class that includes a fleet of spaceships"""

    def __init__(self, nom: str = "", nombre_de_livres: int = 0, adresse: Optional[Adresse] = None):
        super().__init__(nom, nombre_de_livres, adresse)
        self._spaceship_fleet = {}  # name -> SpaceshipAdapter

    def add_spaceship(self, spaceship: Spaceship):
        """Add a spaceship to the library's fleet"""
        adapter = SpaceshipAdapter(spaceship)
        self._spaceship_fleet[spaceship.name] = adapter

    def get_spaceship(self, name: str) -> Optional[SpaceshipAdapter]:
        """Get a spaceship by name"""
        return self._spaceship_fleet.get(name)

    def list_available_spaceships(self):
        """List all available spaceships"""
        return [ship for ship in self._spaceship_fleet.values() if ship.est_disponible()]

    def borrow_spaceship(self, spaceship_name: str, membre: Membre) -> bool:
        """Allow a member to borrow a spaceship"""
        spaceship = self.get_spaceship(spaceship_name)
        if not spaceship:
            return False

        if spaceship.emprunter(membre):
            membre.ajouter_emprunt(spaceship)
            return True
        return False

    def return_spaceship(self, spaceship_name: str, membre: Membre) -> bool:
        """Process a spaceship return"""
        spaceship = self.get_spaceship(spaceship_name)
        if not spaceship or spaceship.emprunteur != membre:
            return False

        if spaceship.retourner():
            membre.supprimer_emprunt(spaceship)
            # Refuel the spaceship after return
            spaceship.spaceship.fuel_level = 100
            return True
        return False

    def get_description(self) -> str:
        """Enhanced description including spaceship fleet"""
        basic_desc = super().get_description()
        ship_count = len(self._spaceship_fleet)
        return f"{basic_desc} Cette bibliothèque dispose également d'une flotte de {ship_count} vaisseaux spatiaux."

    def add_book(self, livre):
        """Add a book to the library"""
        if not hasattr(self, '_books'):
            self._books = {}
        self._books[livre.isbn] = livre
        self.nombre_de_livres += 1

    def find_book_by_title(self, titre):
        """Find a book by its title"""
        if not hasattr(self, '_books'):
            return None
        for book in self._books.values():
            if book.titre == titre:
                return book
        return None
