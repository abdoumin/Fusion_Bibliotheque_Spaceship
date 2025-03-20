from behave import given, when, then
import datetime
from Bibliotheque.salle import Salle  # Classe cible à implémenter
from Bibliotheque.utilisateur import Utilisateur
from Bibliotheque.systeme_reservation import SystemeReservation


@given('un système de bibliothèque avec des salles disponibles')
def step_given_systeme_avec_salles(context):
    context.salles = {}
    context.systeme_reservation = SystemeReservation()


@given('une plage horaire d\'ouverture de {heure_debut:d}h à {heure_fin:d}h')
def step_given_plage_horaire(context, heure_debut, heure_fin):
    context.systeme_reservation.set_heures_ouverture(heure_debut, heure_fin)


@given('une salle "{code}" avec capacité de {capacite:d} personnes')
def step_given_salle(context, code, capacite):
    salle = Salle(code, capacite)
    context.salle_courante = salle
    context.salles[code] = salle
    context.systeme_reservation.ajouter_salle(salle)


@given('un utilisateur "{nom}" avec identifiant "{identifiant}"')
def step_given_utilisateur(context, nom, identifiant):
    context.utilisateur_courant = Utilisateur(nom, identifiant)


@given('la salle est déjà réservée pour demain de {heure_debut:d}h à {heure_fin:d}h')
def step_given_salle_deja_reservee(context, heure_debut, heure_fin):
    demain = datetime.date.today() + datetime.timedelta(days=1)
    debut = datetime.datetime.combine(demain, datetime.time(heure_debut, 0))
    fin = datetime.datetime.combine(demain, datetime.time(heure_fin, 0))
    utilisateur_temp = Utilisateur("Utilisateur Temporaire", "UT000")

    # Réservation directe sans passer par le step de réservation
    context.code_reservation = context.systeme_reservation.reserver_salle(
        context.salle_courante,
        utilisateur_temp,
        debut,
        fin
    )


@given(
    'un utilisateur "{nom}" avec identifiant "{identifiant}" a réservé la salle pour demain de {heure_debut:d}h à {heure_fin:d}h')
def step_given_utilisateur_a_reserve(context, nom, identifiant, heure_debut, heure_fin):
    context.utilisateur_courant = Utilisateur(nom, identifiant)
    demain = datetime.date.today() + datetime.timedelta(days=1)
    debut = datetime.datetime.combine(demain, datetime.time(heure_debut, 0))
    fin = datetime.datetime.combine(demain, datetime.time(heure_fin, 0))

    context.code_reservation = context.systeme_reservation.reserver_salle(
        context.salle_courante,
        context.utilisateur_courant,
        debut,
        fin
    )


@given('le code de réservation est "{code}"')
def step_given_code_reservation(context, code):
    # Simuler un code spécifique pour le test
    context.code_reservation = code
    # Mettre à jour le système avec ce code
    context.systeme_reservation.forcer_code_reservation(
        context.salle_courante,
        context.utilisateur_courant,
        code
    )


@when('l\'utilisateur réserve la salle pour demain de {heure_debut:d}h à {heure_fin:d}h')
def step_when_utilisateur_reserve(context, heure_debut, heure_fin):
    demain = datetime.date.today() + datetime.timedelta(days=1)
    debut = datetime.datetime.combine(demain, datetime.time(heure_debut, 0))
    fin = datetime.datetime.combine(demain, datetime.time(heure_fin, 0))

    try:
        context.code_reservation = context.systeme_reservation.reserver_salle(
            context.salle_courante,
            context.utilisateur_courant,
            debut,
            fin
        )
        context.erreur_reservation = None
    except ValueError as e:
        context.erreur_reservation = str(e)
        context.code_reservation = None


@when(
    'un utilisateur "{nom}" avec identifiant "{identifiant}" tente de réserver la même salle demain de {heure_debut:d}h à {heure_fin:d}h')
def step_when_autre_utilisateur_reserve(context, nom, identifiant, heure_debut, heure_fin):
    utilisateur = Utilisateur(nom, identifiant)
    demain = datetime.date.today() + datetime.timedelta(days=1)
    debut = datetime.datetime.combine(demain, datetime.time(heure_debut, 0))
    fin = datetime.datetime.combine(demain, datetime.time(heure_fin, 0))

    try:
        context.code_reservation_autre = context.systeme_reservation.reserver_salle(
            context.salle_courante,
            utilisateur,
            debut,
            fin
        )
        context.erreur_reservation = None
    except ValueError as e:
        context.erreur_reservation = str(e)
        context.code_reservation_autre = None


@when('l\'utilisateur annule sa réservation avec le code "{code}"')
def step_when_utilisateur_annule(context, code):
    try:
        context.systeme_reservation.annuler_reservation(code)
        context.erreur_annulation = None
    except ValueError as e:
        context.erreur_annulation = str(e)


@then('la réservation devrait être confirmée')
def step_then_reservation_confirmee(context):
    assert context.code_reservation is not None, "La réservation n'a pas été confirmée"


@then('la salle devrait être indisponible pour cette plage horaire')
def step_then_salle_indisponible(context):
    demain = datetime.date.today() + datetime.timedelta(days=1)
    assert not context.salle_courante.est_disponible(demain), "La salle devrait être indisponible"


@then('l\'utilisateur devrait recevoir un code de réservation')
def step_then_code_reservation_recu(context):
    assert context.code_reservation and len(context.code_reservation) > 0, "Aucun code de réservation généré"


@then('la réservation devrait être refusée')
def step_then_reservation_refusee(context):
    assert context.code_reservation_autre is None, "La réservation aurait dû être refusée"


@then('un message d\'erreur indiquant "{message}" devrait être généré')
def step_then_message_erreur(context, message):
    assert context.erreur_reservation is not None, "Aucun message d'erreur n'a été généré"
    assert message in context.erreur_reservation, f"Message attendu: '{message}', obtenu: '{context.erreur_reservation}'"


@then('la réservation devrait être supprimée')
def step_then_reservation_supprimee(context):
    assert not context.systeme_reservation.reservation_existe(
        context.code_reservation), "La réservation existe toujours"


@then('la salle devrait être disponible pour cette plage horaire')
def step_then_salle_disponible(context):
    demain = datetime.date.today() + datetime.timedelta(days=1)
    debut_heure = 9  # Selon le scénario
    fin_heure = 11  # Selon le scénario
    debut = datetime.datetime.combine(demain, datetime.time(debut_heure, 0))
    fin = datetime.datetime.combine(demain, datetime.time(fin_heure, 0))
    assert context.salle_courante.est_disponible_pour_creneau(debut, fin), "La salle devrait être disponible"