# Example of how to use the system
from Bibliotheque.adresse import Adresse
from Bibliotheque.bibliotheque import Bibliotheque
from ObserverPattern.delivery_system import DeliverySystem
from ObserverPattern.pilot import Pilot
from ObserverPattern.spaceship import Spaceship

if __name__ == "__main__":
    # Create a library
    address = Adresse("123 Space Avenue", "Cosmic City", "42XYZ")
    library = Bibliotheque("Galactic Archives", 1000, address)

    # Initialize the delivery system
    delivery_system = DeliverySystem()
    monitor = delivery_system.initialize(library)

    # Create spaceships and pilots
    enterprise = Spaceship("USS Enterprise", 200, 500)
    millennium = Spaceship("Millennium Falcon", 150, 300)

    kirk = Pilot("James Kirk")
    solo = Pilot("Han Solo")

    # Assign pilots to spaceships
    enterprise.assign_pilot(kirk)
    millennium.assign_pilot(solo)

    # Register spaceships with the monitor
    delivery_system.register_spaceship(monitor, enterprise)
    delivery_system.register_spaceship(monitor, millennium)

    # Simulate adding new books to the library
    print("\nAdding new books to the library...")
    library.nombre_de_livres += 5  # Add 5 new books

    # Check for new books
    monitor.check_for_new_books()

    # Simulate adding more books later
    print("\nAdding more books later...")
    library.nombre_de_livres += 10  # Add 10 more books

    # Check for new books again
    monitor.check_for_new_books()