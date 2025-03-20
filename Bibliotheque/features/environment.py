# features/environment.py

def before_scenario(context, scenario):
    """
    Cette fonction est exécutée avant chaque scénario.
    Elle réinitialise l'état si nécessaire.
    """
    context.bibliotheque = None
    context.adresse = None
