from typing import Optional
from .adresse import Adresse

class Bibliotheque:
    """
    Class representing a library
    """

    def __init__(self, nom: str = "", nombre_de_livres: int = 0, adresse: Optional[Adresse] = None):
        """
        Constructor for objects of class Bibliotheque
        """
        self._nom: str = nom
        self._nombre_de_livres: int = nombre_de_livres
        self._adresse: Optional[Adresse] = adresse

    @property
    def nom(self) -> str:
        """Get the library name"""
        return self._nom

    @nom.setter
    def nom(self, value: str) -> None:
        """Set the library name"""
        self._nom = value

    @property
    def nombre_de_livres(self) -> int:
        """Get the number of books"""
        return self._nombre_de_livres

    @nombre_de_livres.setter
    def nombre_de_livres(self, value: int) -> None:
        """Set the number of books"""
        self._nombre_de_livres = value

    @property
    def adresse(self) -> Optional[Adresse]:
        """Get the library address"""
        return self._adresse

    @adresse.setter
    def adresse(self, value: Adresse) -> None:
        """Set the library address"""
        self._adresse = value

    def afficher_details(self) -> str:
        """Display basic details about the library"""
        return f"Le nom : {self._nom} Le nombre de pages : {self._nombre_de_livres}"

    def get_description(self) -> str:
        """Get a full description of the library including location if available"""
        description = f"Bibliothèque: {self._nom} ({self._nombre_de_livres} livres)"
        if self._adresse is not None:
            description += f", Localisation: {self._adresse.get_full_address()}"
        else:
            description += ", Pas d'adresse renseignée."
        return description
