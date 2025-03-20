# language: fr
Fonctionnalité: Gestion des réservations de salles de travail
  En tant qu'utilisateur de la bibliothèque
  Je veux pouvoir réserver une salle de travail
  Afin d'avoir un espace dédié pour mes études ou réunions

  Contexte:
    Étant donné un système de bibliothèque avec des salles disponibles
    Et une plage horaire d'ouverture de 9h à 18h

  Scénario: Réservation d'une salle disponible
    Étant donné une salle "S101" avec capacité de 4 personnes
    Et un utilisateur "Marie Curie" avec identifiant "MC001"
    Quand l'utilisateur réserve la salle pour demain de 14h à 16h
    Alors la réservation devrait être confirmée
    Et la salle devrait être indisponible pour cette plage horaire
    Et l'utilisateur devrait recevoir un code de réservation

  Scénario: Tentative de réservation sur un créneau déjà occupé
    Étant donné une salle "S102" avec capacité de 8 personnes
    Et la salle est déjà réservée pour demain de 10h à 12h
    Quand un utilisateur "Albert Einstein" avec identifiant "AE002" tente de réserver la même salle demain de 11h à 13h
    Alors la réservation devrait être refusée
    Et un message d'erreur indiquant "Créneau déjà occupé" devrait être généré

  Scénario: Annulation d'une réservation
    Étant donné une salle "S103" avec capacité de 6 personnes
    Et un utilisateur "Isaac Newton" avec identifiant "IN003" a réservé la salle pour demain de 9h à 11h
    Et le code de réservation est "RES12345"
    Quand l'utilisateur annule sa réservation avec le code "RES12345"
    Alors la réservation devrait être supprimée
    Et la salle devrait être disponible pour cette plage horaire