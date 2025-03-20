from spaceship_model import Spaceship
from pilot_model import Pilot

print("=== Test Interaction Pilot & Spaceship ===")

# Création des objets
spaceship = Spaceship("Enterprise", 100)
pilot = Pilot("Jean-Luc")

# Assigner le pilote au vaisseau
spaceship.assign_pilot(pilot)

# Tester un voyage
print(
    pilot.launch_mission(30)
)  # Attendu : Le vaisseau a voyagé et il reste 70 unités de carburant.
print(pilot.launch_mission(80))  # Attendu : Carburant insuffisant !
