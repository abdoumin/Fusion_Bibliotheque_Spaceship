from ObserverPattern.library_monitor import LibraryMonitor
from ObserverPattern.spaceship import Spaceship


class DeliverySystem:
    """Facade for setting up the entire observer system"""

    @staticmethod
    def initialize(bibliotheque) -> LibraryMonitor:
        """Initialize the library monitoring system"""
        monitor = LibraryMonitor(bibliotheque)
        print(f"Monitoring initialized for library: {bibliotheque.nom}")
        return monitor

    @staticmethod
    def register_spaceship(monitor: LibraryMonitor, ship: Spaceship) -> None:
        """Register a spaceship with the library monitor"""
        monitor.add_observer(ship)
        print(f"Spaceship {ship.name} registered for delivery missions")