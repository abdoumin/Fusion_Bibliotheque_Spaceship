# features/environment.py
def before_all(context):
    # Configuration des vaisseaux par défaut
    context.config.userdata['vaisseaux'] = [
        {'nom': 'Enterprise', 'niveau_carburant': '100'},
        {'nom': 'Millennium Falcon', 'niveau_carburant': '150'},
        {'nom': 'Serenity', 'niveau_carburant': '80'}
    ]

def before_scenario(context, scenario):
    # Initialiser les structures de données pour chaque scénario
    context.initial_fuel_levels = {}