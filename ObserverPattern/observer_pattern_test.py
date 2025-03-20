# test_observer_pattern.py
import unittest
from unittest.mock import patch, Mock

from Bibliotheque.bibliotheque import Bibliotheque
from ObserverPattern.delivery_observer import BookInfo
from ObserverPattern.library_monitor import LibraryMonitor
from ObserverPattern.pilot import Pilot
from ObserverPattern.spaceship import Spaceship
from ObserverPattern.delivery_system import DeliverySystem


class TestObserverPattern(unittest.TestCase):

    def setUp(self):
        # Setup the library
        self.bibliotheque = Bibliotheque("Galactic Archives", 1000)

        # Setup the monitor
        self.monitor = LibraryMonitor(self.bibliotheque)

        # Setup spaceships
        self.enterprise = Spaceship("USS Enterprise", 200, 500)
        self.millennium = Spaceship("Millennium Falcon", 150, 300)

        # Setup pilots
        self.kirk = Pilot("James Kirk")
        self.solo = Pilot("Han Solo")

        # Assign pilots to ships
        self.enterprise.assign_pilot(self.kirk)
        self.millennium.assign_pilot(self.solo)

        # Register ships with monitor
        self.monitor.add_observer(self.enterprise)
        self.monitor.add_observer(self.millennium)

    def test_bidirectional_pilot_relationship(self):
        """Test bidirectional relationship between pilot and spaceship"""
        # Create a new pilot and spaceship
        chewie = Pilot("Chewbacca")
        falcon = Spaceship("Falcon", 100)

        # Assign pilot to ship
        falcon.assign_pilot(chewie)

        # Verify bidirectional relationship
        self.assertEqual(falcon.pilot, chewie)
        self.assertEqual(chewie.spaceship, falcon)

        # Change assignment
        new_ship = Spaceship("New Ship", 150)
        chewie.assign_spaceship(new_ship)

        # Verify relationship updated correctly
        self.assertEqual(chewie.spaceship, new_ship)
        self.assertEqual(new_ship.pilot, chewie)
        self.assertIsNone(falcon.pilot)

    def test_observer_notifications(self):
        """Test that observers receive notifications"""
        # Create a mock method to track updates
        self.enterprise.update = Mock(wraps=self.enterprise.update)
        self.millennium.update = Mock(wraps=self.millennium.update)

        # Create book info
        book_info = BookInfo(
            title="Test Book",
            destination="Test Planet",
            priority=3
        )

        # Notify observers
        self.monitor.notify_observers(book_info)

        # Verify both ships got notified
        self.enterprise.update.assert_called_once_with(book_info)
        self.millennium.update.assert_called_once_with(book_info)

    def test_monitor_detects_new_books(self):
        """Test that the monitor detects when books are added"""
        # Add new books to the library
        initial_count = self.bibliotheque.nombre_de_livres
        self.bibliotheque.nombre_de_livres += 5

        # Create spy for notify_observers
        with patch.object(self.monitor, 'notify_observers') as mock_notify:
            # Check for new books
            self.monitor.check_for_new_books()

            # Verify notify_observers was called
            self.assertEqual(mock_notify.call_count, 1)

            # Verify book info was created correctly
            call_args = mock_notify.call_args[0][0]
            self.assertEqual(call_args.title, "5 new books")
            self.assertEqual(call_args.priority, 2)

            # Verify count was updated
            self.assertEqual(self.monitor._last_book_count, initial_count + 5)

    def test_mission_acceptance(self):
        """Test that a spaceship can accept a mission"""
        # Create book info for a mission
        book_info = BookInfo(
            title="Important Book",
            destination="Alpha Centauri",
            priority=2
        )

        # Verify initial state
        self.assertEqual(len(self.enterprise.current_missions), 0)

        # Accept mission
        initial_fuel = self.enterprise.fuel_level
        result = self.enterprise.accept_mission(book_info)

        # Verify mission was accepted
        self.assertTrue(result)
        self.assertEqual(len(self.enterprise.current_missions), 1)
        self.assertIn(book_info, self.enterprise.current_missions)

        # Verify fuel was consumed
        expected_fuel_used = 10 * book_info.priority  # Base formula
        self.assertEqual(self.enterprise.fuel_level, initial_fuel - expected_fuel_used)

    def test_mission_completion(self):
        """Test completing a mission"""
        # Create and accept a mission
        book_info = BookInfo(
            title="Science Book",
            destination="Mars Colony",
            priority=1
        )
        self.millennium.accept_mission(book_info)

        # Verify mission is active
        self.assertIn(book_info, self.millennium.current_missions)

        # Record initial state
        initial_mission_count = self.solo.mission_count
        initial_experience = self.solo.experience

        # Complete the mission
        result = self.solo.complete_mission(book_info)

        # Verify mission completion
        self.assertTrue(result)
        self.assertNotIn(book_info, self.millennium.current_missions)
        self.assertIn(book_info, self.millennium.mission_history)



if __name__ == '__main__':
    unittest.main()