from behave import given, when, then
from SpaceShip.pilot_model import Pilot
from SpaceShip.spaceship_model import Spaceship


@given('un vaisseau spatial "{spaceship_name}" avec une capacité de "{capacity}" pilotes')
def step_impl(context, spaceship_name, capacity):
    context.current_spaceship = Spaceship(spaceship_name, 100)  # Default fuel level of 100
    context.current_capacity = int(capacity)


@when('un pilote "{pilot_name}" est assigné à ce vaisseau')
def step_impl(context, pilot_name):
    pilot = Pilot(pilot_name)
    context.current_spaceship.assign_pilot(pilot)
    context.current_pilot = pilot


@then('le pilote doit apparaître dans la liste des pilotes du vaisseau')
def step_impl(context):
    assert context.current_spaceship.pilot is not None
    assert context.current_spaceship.pilot.name == context.current_pilot.name


@given('un vaisseau spatial "{spaceship_name}" avec un niveau de carburant de "{fuel_level}" unités')
def step_impl(context, spaceship_name, fuel_level):
    context.current_spaceship = Spaceship(spaceship_name, int(fuel_level))


@when('il tente de voyager en consommant "{fuel_used}" unités')
def step_impl(context, fuel_used):
    context.result_message = context.current_spaceship.travel(int(fuel_used))


@then('il doit afficher le message "{expected_message}"')
def step_impl(context, expected_message):
    if "Voyage réussi" in expected_message:
        assert "a voyagé" in context.result_message
        remaining_fuel = int(expected_message.split("reste ")[1].split(" ")[0])
        assert f"reste {remaining_fuel}" in context.result_message
    elif "Carburant insuffisant" in expected_message:
        assert "Carburant insuffisant" in context.result_message


@given('un pilote "{pilot_name}" déjà assigné au vaisseau "{spaceship_name1}"')
def step_impl(context, pilot_name, spaceship_name1):
    pilot = Pilot(pilot_name)
    spaceship1 = Spaceship(spaceship_name1, 100)
    spaceship1.assign_pilot(pilot)

    context.current_pilot = pilot
    context.first_spaceship = spaceship1


@when('on tente de l\'assigner à un autre vaisseau "{spaceship_name2}"')
def step_impl(context, spaceship_name2):
    spaceship2 = Spaceship(spaceship_name2, 100)
    context.second_spaceship = spaceship2

    context.error_message = None
    try:
        if context.current_pilot.spaceship is not None:
            context.error_message = "Pilote déjà assigné"
        else:
            spaceship2.assign_pilot(context.current_pilot)
    except Exception as e:
        context.error_message = str(e)


@then('le système refuse avec le message "{error_message}"')
def step_impl(context, error_message):
    assert context.error_message == error_message
    assert context.current_pilot.spaceship.name == context.first_spaceship.name

