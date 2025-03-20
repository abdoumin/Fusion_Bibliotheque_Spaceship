from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from pilot_model import Pilot


class Spaceship:
    def __init__(self, name: str, fuel_level: int):
        self.name = name
        self.fuel_level = fuel_level
        self.pilot = None

    def assign_pilot(self, pilot: "Pilot"):
        """Assigne un pilote au vaisseau."""
        self.pilot = pilot
        pilot.assign_spaceship(self)

    def travel(self, fuel_used: int) -> str:
        """Simule un voyage si le carburant est suffisant."""
        if self.fuel_level >= fuel_used:
            self.fuel_level -= fuel_used
            return f"Le vaisseau {self.name} a voyagé ! Il reste {self.fuel_level} unités de carburant."
        return "Carburant insuffisant pour voyager !"


# === Exécution directe pour tester la classe Spaceship ===
if __name__ == "__main__":
    print("=== Test de Spaceship ===")
    spaceship = Spaceship("Enterprise", 100)
    print(spaceship.travel(30))  # Doit afficher que le vaisseau a voyagé
    print(spaceship.travel(80))  # Doit afficher "Carburant insuffisant pour voyager !"
