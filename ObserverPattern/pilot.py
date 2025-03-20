from typing import Optional, List


class Pilot:
    """A pilot that can fly spaceships and handle book delivery missions"""

    def __init__(self, name: str):
        """Initialize a pilot

        Args:
            name: The pilot's name
        """
        self.name = name
        self.spaceship = None
        self.experience = 0
        self.mission_count = 0
        self.mission_alerts = []

    def assign_spaceship(self, spaceship: 'Spaceship') -> None:
        """Create a bidirectional relationship with a spaceship

        Args:
            spaceship: The spaceship to assign to this pilot
        """
        # Update spaceship if it's a different one
        if self.spaceship != spaceship:
            # Remove this pilot from current spaceship if exists
            if self.spaceship is not None:
                self.spaceship.pilot = None

            # Assign the new spaceship
            self.spaceship = spaceship

            # Complete the bidirectional relationship
            if spaceship is not None and spaceship.pilot != self:
                spaceship.assign_pilot(self)

    def receive_mission_alert(self, book_info: 'BookInfo') -> None:
        """Receive an alert about a potential delivery mission

        Args:
            book_info: Information about books that need delivery
        """
        self.mission_alerts.append(book_info)
        print(f"Pilot {self.name} received alert for delivery to {book_info.destination}")

        # In an interactive system, we might prompt for input here
        # For automation, we'll auto-accept based on some criteria
        if book_info.priority > 3:  # High priority missions auto-accept
            self.accept_mission(book_info)
        else:
            print(f"Awaiting decision from Pilot {self.name} for mission to {book_info.destination}")

    def accept_mission(self, book_info: 'BookInfo') -> bool:
        """Accept a book delivery mission

        Args:
            book_info: Information about the delivery mission

        Returns:
            True if the mission was accepted, False otherwise
        """
        if not self.spaceship:
            print(f"Pilot {self.name} cannot accept mission: no spaceship assigned")
            return False

        if self.spaceship.accept_mission(book_info):
            self.mission_count += 1
            # Remove from alerts since it's now an active mission
            if book_info in self.mission_alerts:
                self.mission_alerts.remove(book_info)
            return True

        return False

    def decline_mission(self, book_info: 'BookInfo') -> None:
        """Decline a book delivery mission

        Args:
            book_info: Information about the delivery mission
        """
        if book_info in self.mission_alerts:
            self.mission_alerts.remove(book_info)
            print(f"Mission declined by Pilot {self.name}: delivery to {book_info.destination}")

    def complete_mission(self, book_info: 'BookInfo') -> bool:
        """Mark a mission as completed

        Args:
            book_info: The mission to complete

        Returns:
            True if the mission was completed, False otherwise
        """
        if not self.spaceship:
            return False

        if self.spaceship.complete_mission(book_info):
            self.experience += book_info.priority  # Gain experience based on mission priority
            return True

        return False

    def launch_mission(self, fuel_used: int) -> str:
        """Launch mission using specified fuel (compatibility with original code)

        Args:
            fuel_used: Amount of fuel to use

        Returns:
            A message about the mission result
        """
        if self.spaceship:
            return f"{self.name} is piloting the spaceship {self.spaceship.name}: {self.spaceship.travel(fuel_used)}"
        return f"{self.name} has no spaceship assigned!"

    def get_status(self) -> str:
        """Get the current status of the pilot

        Returns:
            A status report as a string
        """
        spaceship_info = f"Piloting {self.spaceship.name}" if self.spaceship else "Not assigned to any spaceship"
        alert_count = len(self.mission_alerts)
        alert_info = f"Pending mission alerts: {alert_count}" if alert_count > 0 else "No pending mission alerts"

        return (f"Pilot: {self.name}\n"
                f"Experience: {self.experience} points\n"
                f"Completed missions: {self.mission_count}\n"
                f"{spaceship_info}\n"
                f"{alert_info}")