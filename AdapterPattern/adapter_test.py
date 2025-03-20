# test_adapter_pattern.py
import unittest

from AdapterPattern.bibliotheque_spatiale import BibliothequeSpatiale
from AdapterPattern.intergalactic_mission_service import IntergalacticMissionService
from AdapterPattern.member_pilote import MembrePilote
from AdapterPattern.spaceship_adapter import SpaceshipAdapter
from Bibliotheque.adresse import Adresse
from Bibliotheque.livre import Livre
from SpaceShip.spaceship_model import Spaceship


class AdapterPatternTest(unittest.TestCase):

    def setUp(self):
        # Create a spatial library
        adresse_spatiale = Adresse("42 Avenue Cosmos", "Space City", "SC-42")
        self.biblio_spatiale = BibliothequeSpatiale("Bibliothèque Intergalactique", 5000, adresse_spatiale)

        # Create spaceships
        self.enterprise = Spaceship("Enterprise", 100)
        self.millennium = Spaceship("Millennium Falcon", 150)
        self.biblio_spatiale.add_spaceship(self.enterprise)
        self.biblio_spatiale.add_spaceship(self.millennium)

        # Create member
        self.jean_luc = MembrePilote("Jean-Luc Picard", "P12345")
        self.jean_luc.qualification_level = 5

        # Create books
        self.livre_python = Livre("Python Programming", "978-0-13-513877-0")
        self.livre_space = Livre("Space Travel Techniques", "978-1-86197-876-9")
        self.biblio_spatiale.add_book(self.livre_python)
        self.biblio_spatiale.add_book(self.livre_space)

        # Create mission service
        self.mission_service = IntergalacticMissionService(self.biblio_spatiale)

    def test_spaceship_adapter_creation(self):
        """Test if spaceship adapter is created correctly"""
        adapter = SpaceshipAdapter(self.enterprise)
        self.assertEqual(adapter.titre, "Spaceship: Enterprise")
        self.assertEqual(adapter.statut, "Available")
        self.assertIsNone(adapter.emprunteur)
        self.assertTrue(adapter.est_disponible())

    def test_successful_mission_preparation(self):
        """Test if a mission can be successfully prepared"""
        mission_id = self.mission_service.prepare_mission(
            "Enterprise",
            self.jean_luc,
            "Alpha Centauri",
            [self.livre_python, self.livre_space]
        )
        self.assertIsNotNone(mission_id)
        self.assertEqual(self.mission_service.active_missions[mission_id]["status"], "Preparing")
        self.assertEqual(self.mission_service.active_missions[mission_id]["pilot"], self.jean_luc)

    def test_mission_preparation_with_insufficient_qualification(self):
        """Test if mission preparation fails with insufficient qualification"""
        wesley = MembrePilote("Wesley Crusher", "P54321")
        wesley.qualification_level = 1  # Not qualified for Enterprise

        mission_id = self.mission_service.prepare_mission(
            "Enterprise",
            wesley,
            "Alpha Centauri",
            [self.livre_python]
        )

        self.assertIsNone(mission_id)
        self.assertEqual(self.mission_service.last_error, "Niveau de qualification insuffisant")

    def test_mission_launch_and_fuel_reduction(self):
        """Test if launching a mission reduces spaceship fuel"""
        # Prepare mission
        mission_id = self.mission_service.prepare_mission(
            "Enterprise",
            self.jean_luc,
            "Alpha Centauri",
            [self.livre_python]
        )

        initial_fuel = self.enterprise.fuel_level

        # Launch mission
        result = self.mission_service.launch_mission(mission_id)

        self.assertTrue(result)
        self.assertEqual(self.mission_service.active_missions[mission_id]["status"], "In Progress")
        self.assertLess(self.enterprise.fuel_level, initial_fuel)

    def test_complete_mission_returns_resources(self):
        """Test if completing a mission returns all resources"""
        # Prepare and launch mission
        mission_id = self.mission_service.prepare_mission(
            "Enterprise",
            self.jean_luc,
            "Alpha Centauri",
            [self.livre_python, self.livre_space]
        )
        self.mission_service.launch_mission(mission_id)

        # Complete mission
        result = self.mission_service.complete_mission(mission_id)

        self.assertTrue(result)
        self.assertEqual(self.mission_service.active_missions[mission_id]["status"], "Completed")

        # Check if resources are returned
        enterprise_adapter = self.biblio_spatiale.get_spaceship("Enterprise")
        self.assertIsNone(enterprise_adapter.emprunteur)
        self.assertTrue(enterprise_adapter.est_disponible())
        self.assertEqual(self.livre_python.statut, "Disponible")
        self.assertEqual(self.livre_space.statut, "Disponible")


if __name__ == "__main__":
    unittest.main()