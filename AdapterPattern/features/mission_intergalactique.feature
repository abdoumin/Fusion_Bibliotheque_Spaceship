# language: fr
Fonctionnalité: Emprunt de vaisseaux spatiaux pour missions intergalactiques
  En tant que membre de la Bibliothèque Spatiale
  Je veux pouvoir emprunter un vaisseau spatial pour une mission intergalactique
  Afin de partager des connaissances avec d'autres civilisations

  Contexte:
    Étant donné que la Bibliothèque Spatiale "Bibliothèque Intergalactique" existe
    Et que les vaisseaux suivants sont disponibles:
      | nom               | niveau_carburant |
      | Enterprise        | 100              |
      | Millennium Falcon | 150              |
      | Serenity          | 80               |
    Et que les livres suivants sont disponibles:
      | titre                      | isbn             |
      | Python Programming         | 978-0-13-513877-0 |
      | Space Travel Techniques    | 978-1-86197-876-9 |
      | Physics of Warp Drive      | 978-0-553-57548-0 |
    Et que "Jean-Luc Picard" est un membre pilote avec un niveau de qualification de 5

  Scénario: Préparation d'une mission réussie
    Quand "Jean-Luc Picard" prépare une mission vers "Alpha Centauri" avec le vaisseau "Enterprise"
    Et il sélectionne les livres suivants pour la mission:
      | titre                   |
      | Python Programming      |
      | Space Travel Techniques |
    Alors la mission doit être préparée avec succès
    Et le vaisseau "Enterprise" doit être assigné à "Jean-Luc Picard"
    Et les livres sélectionnés doivent être réservés pour la mission

  Scénario: Lancement d'une mission
    Étant donné que "Jean-Luc Picard" a préparé une mission vers "Alpha Centauri" avec le vaisseau "Enterprise"
    Et qu'il a sélectionné les livres "Python Programming" et "Space Travel Techniques"
    Quand il lance la mission
    Alors la mission doit être en cours
    Et le niveau de carburant du vaisseau "Enterprise" doit être réduit
    Et les heures de vol de "Jean-Luc Picard" doivent augmenter

  Scénario: Emprunt de vaisseau échoué par manque de qualification
    Étant donné que "Wesley Crusher" est un membre pilote avec un niveau de qualification de 1
    Quand "Wesley Crusher" prépare une mission vers "Alpha Centauri" avec le vaisseau "Enterprise"
    Alors la préparation de la mission doit échouer
    Et un message d'erreur doit indiquer "Niveau de qualification insuffisant"

  Scénario: Retour de mission réussie
    Étant donné que "Jean-Luc Picard" a une mission en cours vers "Alpha Centauri"
    Quand il complète la mission
    Alors le vaisseau "Enterprise" doit être retourné à la bibliothèque
    Et le vaisseau doit être disponible pour emprunt
    Et les livres doivent être retournés avec des notes sur leur voyage
    Et l'expérience de pilotage de "Jean-Luc Picard" doit être enregistrée