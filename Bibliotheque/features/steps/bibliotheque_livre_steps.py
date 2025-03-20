from behave import given, when, then
import datetime
from Bibliotheque.livre import Livre  # Classe cible à implémenter
from Bibliotheque.membre import Membre  # Autre classe requise
from Bibliotheque.emprunt import SystemeEmprunt  # Autre classe requise

@given('une bibliothèque avec des livres disponibles')
def step_given_bibliotheque_avec_livres(context):
    context.livres = {}

@given('un système d\'emprunt initialisé')
def step_given_systeme_emprunt(context):
    context.systeme_emprunt = SystemeEmprunt()

@given('un livre "{titre}" avec l\'ISBN "{isbn}"')
def step_given_livre(context, titre, isbn):
    livre = Livre(titre, isbn)
    context.livre_courant = livre
    context.livres[isbn] = livre

@given('un livre "{titre}" avec l\'ISBN "{isbn}" qui est emprunté')
def step_given_livre_emprunte(context, titre, isbn):
    livre = Livre(titre, isbn)
    livre.statut = "Emprunté"
    context.livre_courant = livre
    context.livres[isbn] = livre

@given('un membre "{nom}" avec le numéro "{numero}"')
def step_given_membre(context, nom, numero):
    context.membre_courant = Membre(nom, numero)

@given('un membre "{nom}" avec le numéro "{numero}" qui a emprunté le livre')
def step_given_membre_emprunteur(context, nom, numero):
    membre = Membre(nom, numero)
    context.membre_courant = membre
    context.livre_courant.emprunteur = membre

@when('le membre emprunte le livre')
def step_when_membre_emprunte_livre(context):
    context.systeme_emprunt.emprunter_livre(
        context.livre_courant,
        context.membre_courant
    )

@when('le livre est retourné')
def step_when_livre_retourne(context):
    context.systeme_emprunt.retourner_livre(context.livre_courant)

@then('le livre devrait être marqué comme "{statut}"')
def step_then_livre_statut(context, statut):
    assert context.livre_courant.statut == statut, f"Statut attendu: {statut}, obtenu: {context.livre_courant.statut}"

@then('la date de retour prévue devrait être dans {jours:d} jours')
def step_then_date_retour(context, jours):
    date_attendue = datetime.date.today() + datetime.timedelta(days=jours)
    assert context.livre_courant.date_retour == date_attendue, f"Date de retour incorrecte"

@then('le livre devrait être associé au membre "{nom}"')
def step_then_livre_associe_membre(context, nom):
    assert context.livre_courant.emprunteur is not None, "L'emprunteur ne devrait pas être None"
    assert context.livre_courant.emprunteur.nom == nom, f"Emprunteur attendu: {nom}, obtenu: {context.livre_courant.emprunteur.nom}"

@then('le livre ne devrait plus être associé à aucun membre')
def step_then_livre_non_associe(context):
    assert context.livre_courant.emprunteur is None, "L'emprunteur devrait être None"