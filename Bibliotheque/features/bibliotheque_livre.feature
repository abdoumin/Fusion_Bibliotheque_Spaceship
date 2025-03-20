# language: fr
Fonctionnalité: Gestion des livres dans une bibliothèque
  En tant que bibliothécaire
  Je veux pouvoir gérer les emprunts de livres
  Afin de suivre les documents en circulation

  Contexte:
    Étant donné une bibliothèque avec des livres disponibles
    Et un système d'emprunt initialisé

  Scénario: Emprunter un livre disponible
    Étant donné un livre "Les Misérables" avec l'ISBN "9782253096344"
    Et un membre "Jean Martin" avec le numéro "M12345"
    Quand le membre emprunte le livre
    Alors le livre devrait être marqué comme "Emprunté"
    Et la date de retour prévue devrait être dans 21 jours
    Et le livre devrait être associé au membre "Jean Martin"

  Scénario: Retourner un livre emprunté
    Étant donné un livre "L'Étranger" avec l'ISBN "9782070360024" qui est emprunté
    Et un membre "Sophie Dupont" avec le numéro "M67890" qui a emprunté le livre
    Quand le livre est retourné
    Alors le livre devrait être marqué comme "Disponible"
    Et le livre ne devrait plus être associé à aucun membre