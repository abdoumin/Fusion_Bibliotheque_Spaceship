# steps/bibliotheque_spatiale_steps.py

from behave import given, when, then

from Bibliotheque.bibliotheque import Bibliotheque
from ObserverPattern.delivery_observer import BookInfo
from ObserverPattern.delivery_system import DeliverySystem
from ObserverPattern.library_monitor import LibraryMonitor
from ObserverPattern.pilot import Pilot
from ObserverPattern.spaceship import Spaceship


# Définitions des étapes pour le Contexte

@given('que la bibliothèque des Archives Galactiques est opérationnelle')
def step_impl(context):
    context.bibliotheque = Bibliotheque("Archives Galactiques", 1000)
    context.library_monitor = LibraryMonitor(context.bibliotheque)
    context.delivery_system = DeliverySystem()
    context.spaceships = {}
    context.pilots = {}


@given('que les vaisseaux spatiaux suivants sont disponibles')
def step_impl(context):
    for row in context.table:
        spaceship = Spaceship(row['Nom'], int(row['Carburant']))
        context.spaceships[row['Nom']] = spaceship
        context.library_monitor.add_observer(spaceship)


@given('que les pilotes suivants sont en service')
def step_impl(context):
    for row in context.table:
        pilot = Pilot(row['Nom'])
        spaceship = context.spaceships[row['Vaisseau']]
        pilot.assign_spaceship(spaceship)
        context.pilots[row['Nom']] = pilot


# Étapes pour "Attribution automatique des livraisons de livres à haute priorité"

@when('un nouveau manuscrit rare "{title}" arrive à la bibliothèque')
def step_impl(context, title):
    context.new_book_title = title
    context.bibliotheque.nombre_de_livres += 1


@when('qu\'il est classé comme niveau de priorité {priority:d}')
def step_impl(context, priority):
    context.book_priority = priority


@when('qu\'il doit être livré à "{destination}"')
def step_impl(context, destination):
    context.book_destination = destination
    context.book_info = BookInfo(
        title=context.new_book_title,
        destination=context.book_destination,
        priority=context.book_priority
    )


@then('le système de surveillance de la bibliothèque devrait détecter le nouveau livre')
def step_impl(context):
    # Simuler le système de surveillance détectant le nouveau livre
    new_books_detected = context.library_monitor.check_for_new_books()
    assert new_books_detected, "Le système de surveillance aurait dû détecter de nouveaux livres"


@then('une alerte devrait être envoyée à tous les vaisseaux disponibles')
def step_impl(context):
    # Notifier tous les vaisseaux
    context.library_monitor.notify_observers(context.book_info)

    # Vérifier que tous les vaisseaux ont reçu l'alerte
    for name, spaceship in context.spaceships.items():
        assert spaceship.has_received_alert(context.book_info), \
            f"Le vaisseau {name} n'a pas reçu l'alerte"


@then('la livraison devrait être automatiquement attribuée au vaisseau le plus adapté')
def step_impl(context):
    # Attribuer la mission
    assignment = context.delivery_system.assign_mission(
        context.book_info, list(context.spaceships.values()))
    context.assigned_spaceship = assignment['spaceship']
    assert assignment['success'], "La mission aurait dû être attribuée automatiquement"


@then('le pilote devrait recevoir un briefing de mission')
def step_impl(context):
    # Vérifier que le pilote du vaisseau assigné a reçu le briefing
    pilot = context.assigned_spaceship.pilot
    assert pilot.has_received_briefing(context.book_info), \
        f"Le pilote {pilot.name} n'a pas reçu le briefing de mission"


# Étapes pour "Vérification du statut d'un vaisseau spatial"

@when('le contrôleur demande le statut du "{spaceship_name}"')
def step_impl(context, spaceship_name):
    spaceship = context.spaceships.get(spaceship_name)
    assert spaceship is not None, f"Vaisseau {spaceship_name} non trouvé"

    context.spaceship_status = spaceship.get_status()


@then('le système devrait afficher le niveau de carburant actuel')
def step_impl(context):
    assert 'fuel_level' in context.spaceship_status, \
        "Le statut ne contient pas d'information sur le carburant"


@then('la liste des missions en cours')
def step_impl(context):
    assert 'current_missions' in context.spaceship_status, \
        "Le statut ne contient pas la liste des missions en cours"


# Étapes pour "Ravitaillement d'un vaisseau en carburant"

@given('que le "{spaceship_name}" a {fuel:d} unités de carburant')
def step_impl(context, spaceship_name, fuel):
    spaceship = context.spaceships.get(spaceship_name)
    assert spaceship is not None, f"Vaisseau {spaceship_name} non trouvé"

    spaceship.fuel_level = fuel
    context.refuel_spaceship = spaceship


@when('le pilote demande un ravitaillement de {amount:d} unités')
def step_impl(context, amount):
    spaceship = context.refuel_spaceship
    context.before_level = spaceship.fuel_level
    context.refuel_amount = amount

    context.report = spaceship.refuel(amount)


@then('le niveau de carburant devrait être de {level:d} unités')
def step_impl(context, level):
    spaceship = context.refuel_spaceship
    assert spaceship.fuel_level == level, \
        f"Le niveau de carburant est {spaceship.fuel_level}, mais devrait être {level}"


@then('un rapport de ravitaillement devrait être généré')
def step_impl(context):
    assert context.report, "Un rapport de ravitaillement aurait dû être généré"
    assert str(context.before_level) in context.report, "Le rapport devrait mentionner le niveau précédent"
    assert str(context.refuel_amount) in context.report, "Le rapport devrait mentionner la quantité ajoutée"


# Étapes pour "Fin de mission et retour de livre"

@given('que le "{spaceship_name}" a livré "{book_title}"')
def step_impl(context, spaceship_name, book_title):
    spaceship = context.spaceships.get(spaceship_name)
    assert spaceship is not None, f"Vaisseau {spaceship_name} non trouvé"

    # Créer une mission en cours pour le vaisseau
    book_info = BookInfo(title=book_title, destination="Test destination", priority=3)
    spaceship.add_active_mission(book_info)
    context.mission_spaceship = spaceship
    context.mission_book_info = book_info


@when('le pilote marque la mission comme terminée')
def step_impl(context):
    spaceship = context.mission_spaceship
    pilot = spaceship.pilot

    context.mission_result = pilot.complete_mission(context.mission_book_info)


@then('le livre devrait être enregistré comme livré dans le système')
def step_impl(context):
    assert context.mission_result, "La mission n'a pas été correctement terminée"
    assert context.delivery_system.verify_book_delivered(context.mission_book_info.title), \
        "Le livre n'a pas été enregistré comme livré"


@then('le vaisseau devrait être disponible pour de nouvelles missions')
def step_impl(context):
    spaceship = context.mission_spaceship
    assert not spaceship.has_active_mission(context.mission_book_info), \
        "Le vaisseau devrait avoir terminé cette mission"
    assert spaceship.is_available(), \
        "Le vaisseau devrait être disponible pour de nouvelles missions"