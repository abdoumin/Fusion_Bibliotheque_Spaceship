# Create a spatial library
from AdapterPattern.bibliotheque_spatiale import BibliothequeSpatiale
from AdapterPattern.intergalactic_mission_service import IntergalacticMissionService
from AdapterPattern.member_pilote import MembrePilote
from Bibliotheque.adresse import Adresse
from Bibliotheque.livre import Livre
from SpaceShip.spaceship_model import Spaceship

adresse_spatiale = Adresse("42 Avenue Cosmos", "Space City", "SC-42")
biblio_spatiale = BibliothequeSpatiale("Bibliothèque Intergalactique", 5000, adresse_spatiale)

# Add some spaceships to the library
enterprise = Spaceship("Enterprise", 100)
millennium = Spaceship("Millennium Falcon", 150)
serenity = Spaceship("Serenity", 80)

biblio_spatiale.add_spaceship(enterprise)
biblio_spatiale.add_spaceship(millennium)
biblio_spatiale.add_spaceship(serenity)

# Create a qualified pilot/member
jean_luc = MembrePilote("Jean-Luc Picard", "P12345")
jean_luc.qualification_level = 5  # Top qualification

# Create some books
livre_python = Livre("Python Programming", "978-0-13-513877-0")
livre_space = Livre("Space Travel Techniques", "978-1-86197-876-9")
livre_physics = Livre("Physics of Warp Drive", "978-0-553-57548-0")

# Create the mission service
mission_service = IntergalacticMissionService(biblio_spatiale)

# Prepare a mission
mission_id = mission_service.prepare_mission(
    "Enterprise",
    jean_luc,
    "Alpha Centauri",
    [livre_python, livre_space]
)

if mission_id:
    print(f"Mission {mission_id} prepared successfully with Captain {jean_luc.nom}")

    # Launch the mission
    if mission_service.launch_mission(mission_id):
        print(f"Mission to Alpha Centauri launched successfully!")
        print(f"Captain {jean_luc.nom} now has {jean_luc.flight_hours} flight hours")

        # Eventually complete the mission
        if mission_service.complete_mission(mission_id):
            print("Mission completed successfully! Books and spaceship returned.")
            print(f"Enterprise fuel level: {enterprise.fuel_level}")
    else:
        print("Mission launch failed - check fuel levels")
else:
    print("Failed to prepare mission - check requirements")