from SpaceShip.pilot_model import Pilot
from SpaceShip.spaceship_model import Spaceship


class SpaceshipAdapter:
    """Adapter to make Spaceship compatible with library system"""

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self._checkout_status = "Available"
        self._borrower = None
        self._return_date = None

    @property
    def titre(self):
        return f"Spaceship: {self.spaceship.name}"

    @property
    def isbn(self):
        # Generate a unique identifier for the spaceship
        return f"SHIP-{hash(self.spaceship.name) % 10000:04d}"

    @property
    def statut(self):
        return self._checkout_status

    @statut.setter
    def statut(self, value):
        self._checkout_status = value

    @property
    def emprunteur(self):
        return self._borrower

    @emprunteur.setter
    def emprunteur(self, membre):
        self._borrower = membre

    @property
    def date_retour(self):
        return self._return_date

    @date_retour.setter
    def date_retour(self, date):
        self._return_date = date

    def est_disponible(self):
        return self._checkout_status == "Available" and self.spaceship.fuel_level > 0

    def emprunter(self, membre):
        """Allow a library member to borrow the spaceship"""
        if not self.est_disponible():
            raise ValueError(f"Spaceship {self.spaceship.name} is not available")

        # Convert the member to a pilot
        pilot_name = membre.nom
        pilot = Pilot(pilot_name)

        # Assign the pilot to the spaceship
        self.spaceship.assign_pilot(pilot)

        # Update borrowing status
        self._checkout_status = "Checked Out"
        self._borrower = membre

        import datetime
        self._return_date = datetime.date.today() + datetime.timedelta(days=7)
        return True

    def retourner(self):
        """Return the spaceship to the library"""
        if self._checkout_status != "Checked Out":
            raise ValueError(f"Spaceship {self.spaceship.name} is not checked out")

        # Remove pilot association
        self.spaceship.pilot = None

        # Update status
        self._checkout_status = "Available"
        self._borrower = None
        self._return_date = None
        return True