from .spaceship_model import Spaceship
from .pilot_model import Pilot
import unittest


class TestSpaceship(unittest.TestCase):
    def setUp(self):
        """Fixture pour initialiser les objets."""
        self.spaceship = Spaceship("Explorer", 100)
        self.pilot = Pilot("Jean-Luc")
        self.spaceship.assign_pilot(self.pilot)

    def test_travel_success(self):
        """Test si le vaisseau peut voyager normalement."""
        result = self.spaceship.travel(30)
        self.assertEqual(
            result, "Le vaisseau Explorer a voyagé ! Il reste 70 unités de carburant."
        )

    def test_travel_failure(self):
        """Test si le vaisseau refuse un voyage avec carburant insuffisant."""
        result = self.spaceship.travel(120)
        self.assertEqual(result, "Carburant insuffisant pour voyager !")


if __name__ == "__main__":
    unittest.main()
