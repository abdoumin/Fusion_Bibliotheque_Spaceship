from ObserverPattern.delivery_observer import DeliveryObserver, BookInfo


class Spaceship(DeliveryObserver):
    """A spaceship that can deliver books across space"""

    def __init__(self, name: str, fuel_level: int, capacity: int = 100):
        """Initialize a spaceship for book delivery missions

        Args:
            name: The name of the spaceship
            fuel_level: Current fuel level (in units)
            capacity: Maximum book carrying capacity
        """
        self.name = name
        self.fuel_level = fuel_level
        self.capacity = capacity
        self.pilot = None
        self.current_location = "Library Hub Alpha"
        self.current_missions = []
        self.mission_history = []
        self.received_alerts = []  # Stocker les alertes reçues


    def assign_pilot(self, pilot: 'Pilot') -> None:
        """Assign a pilot to the spaceship with bidirectional relationship

        Args:
            pilot: The pilot to assign to this spaceship
        """
        # Remove this spaceship from current pilot if exists
        if self.pilot is not None:
            self.pilot.spaceship = None

        # Assign the new pilot
        self.pilot = pilot

        # Create the bidirectional relationship
        if pilot.spaceship != self:
            pilot.assign_spaceship(self)

    def update(self, book_info: BookInfo) -> None:
        """Receive updates about new books that need delivery

        This method is called by the publisher when new books are available.

        Args:
            book_info: Information about books that need delivery
        """
        # Ajouter l'alerte à la liste des alertes reçues
        self.received_alerts.append(book_info)

        if self.can_fulfill_mission(book_info):
            if self.pilot:
                self.pilot.receive_mission_alert(book_info)
            else:
                print(f"Spaceship {self.name} needs a pilot to deliver {book_info.title}")
        else:
            print(f"Spaceship {self.name} cannot fulfill the delivery mission for {book_info.title}")

    def can_fulfill_mission(self, book_info: BookInfo) -> bool:
        """Determine if the spaceship can fulfill a delivery mission

        Args:
            book_info: Information about the delivery mission

        Returns:
            True if the mission can be fulfilled, False otherwise
        """
        # Calculate fuel needed based on priority and any special requirements
        fuel_needed = 10 * book_info.priority

        # Special requirements might need additional fuel
        if book_info.special_requirements:
            fuel_needed += 5 * len(book_info.special_requirements)

        # Check if we have a pilot, enough fuel, and enough capacity
        has_pilot = self.pilot is not None
        has_fuel = self.fuel_level >= fuel_needed
        has_capacity = self.capacity > 0

        return has_pilot and has_fuel and has_capacity

    def accept_mission(self, book_info: BookInfo) -> bool:
        """Accept a delivery mission

        Args:
            book_info: Information about the delivery mission

        Returns:
            True if the mission was accepted, False otherwise
        """
        if not self.can_fulfill_mission(book_info):
            return False

        # Calculate and consume the fuel needed
        fuel_needed = 10 * book_info.priority
        if book_info.special_requirements:
            fuel_needed += 5 * len(book_info.special_requirements)

        self.fuel_level -= fuel_needed

        # Add to current missions
        self.current_missions.append(book_info)

        print(f"Mission accepted: {self.name} will deliver {book_info.title} to {book_info.destination}")
        return True

    def complete_mission(self, book_info: BookInfo) -> bool:
        """Mark a mission as completed

        Args:
            book_info: The mission to complete

        Returns:
            True if the mission was completed, False otherwise
        """
        if book_info in self.current_missions:
            self.current_missions.remove(book_info)
            self.mission_history.append(book_info)
            print(f"Mission completed: {self.name} delivered {book_info.title} to {book_info.destination}")
            return True
        return False

    def refuel(self, amount: int) -> None:
        """Refuel the spaceship

        Args:
            amount: The amount of fuel to add
        """
        self.fuel_level += amount
        print(f"{self.name} refueled. New fuel level: {self.fuel_level}")

    def get_status(self) -> str:
        """Get the current status of the spaceship

        Returns:
            A status report as a string
        """
        pilot_info = f"Piloted by {self.pilot.name}" if self.pilot else "No pilot assigned"
        mission_count = len(self.current_missions)
        mission_info = f"Active missions: {mission_count}" if mission_count > 0 else "No active missions"

        return (f"Spaceship: {self.name}\n"
                f"Location: {self.current_location}\n"
                f"Fuel: {self.fuel_level} units\n"
                f"Capacity: {self.capacity} books\n"
                f"{pilot_info}\n"
                f"{mission_info}")

    def travel(self, fuel_used: int) -> str:
        """Simulate traveling and using fuel (compatibility with original code)

        Args:
            fuel_used: Amount of fuel to use

        Returns:
            A message about the travel result
        """
        if self.fuel_level >= fuel_used:
            self.fuel_level -= fuel_used
            return f"The spaceship {self.name} has traveled! Remaining fuel: {self.fuel_level} units."
        return "Insufficient fuel for travel!"

    def has_received_alert(self, book_info):
        """Vérifie si ce vaisseau a reçu une alerte spécifique

        Args:
            book_info: L'information sur le livre à vérifier

        Returns:
            bool: True si l'alerte a été reçue, False sinon
        """
        for alert in self.received_alerts:
            # Comparaison basée sur le titre pour simplifier
            if alert.title == book_info.title:
                return True

        return False

    def add_active_mission(self, book_info):
        """Ajoute une mission active pour ce vaisseau"""
        if book_info not in self.current_missions:
            self.current_missions.append(book_info)


    def has_active_mission(self, book_info):
        """Vérifie si ce vaisseau a une mission active spécifique"""
        return book_info in self.current_missions


    def is_available(self):
        """Vérifie si ce vaisseau est disponible pour de nouvelles missions"""
        return len(self.current_missions) < self.capacity / 10  # Par exemple, chaque mission occupe 10% de capacité
