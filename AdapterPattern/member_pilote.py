# bibliotheque/models.py
from Bibliotheque.membre import Membre


class MembrePilote(Membre):
    """Extended member class with piloting capabilities"""

    def __init__(self, nom, numero):
        super().__init__(nom, numero)
        self._qualification_level = 0
        self._flight_hours = 0

    @property
    def qualification_level(self):
        return self._qualification_level

    @qualification_level.setter
    def qualification_level(self, level):
        if 0 <= level <= 5:  # 5 levels of qualification
            self._qualification_level = level

    @property
    def flight_hours(self):
        return self._flight_hours

    def log_flight_hours(self, hours):
        """Add flight hours to the member's record"""
        if hours > 0:
            self._flight_hours += hours
            # Automatically upgrade qualification if enough hours
            if self._flight_hours > 100 and self._qualification_level < 5:
                self._qualification_level += 1

    def can_pilot(self, spaceship_adapter):
        """Check if the member can pilot a particular spaceship"""
        # Règle simple : Enterprise et Millennium Falcon nécessitent un niveau 4+
        spaceship_name = spaceship_adapter.spaceship.name
        if spaceship_name in ["Enterprise", "Millennium Falcon"]:
            required_level = 4
        else:  # Les autres vaisseaux nécessitent un niveau 2+
            required_level = 2

        return self._qualification_level >= required_level