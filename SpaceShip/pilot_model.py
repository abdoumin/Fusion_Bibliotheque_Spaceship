from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from spaceship_model import Spaceship


class Pilot:
    def __init__(self, name: str):
        self.name = name
        self.spaceship = None

    def assign_spaceship(self, spaceship: "Spaceship"):
        """Liaison bidirectionnelle avec un vaisseau."""
        self.spaceship = spaceship

    def launch_mission(self, fuel_used: int) -> str:
        """Le pilote tente de piloter son vaisseau."""
        if self.spaceship:
            return f"{self.name} pilote le vaisseau {self.spaceship.name} : {self.spaceship.travel(fuel_used)}"
        return f"{self.name} n'a pas de vaisseau assigné !"


# === Exécution directe pour tester la classe Pilot ===
if __name__ == "__main__":
    print("=== Test de Pilot ===")
    pilot = Pilot("Jean-Luc")
    print(pilot.launch_mission(20))  # Doit afficher que le pilote n'a pas de vaisseau
