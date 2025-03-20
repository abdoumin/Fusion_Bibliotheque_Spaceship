# language: fr

Fonctionnalité: Système de Livraison Intergalactique de Livres
  En tant que Gardien du Savoir aux Archives Galactiques
  Je veux livrer des livres rares vers des systèmes stellaires lointains
  Afin que le savoir puisse être partagé à travers l'univers

  Contexte:
    Étant donné que la bibliothèque des Archives Galactiques est opérationnelle
    Et que les vaisseaux spatiaux suivants sont disponibles:
      | Nom                | Carburant |
      | USS Enterprise     | 200       |
      | Faucon Millennium  | 150       |
    Et que les pilotes suivants sont en service:
      | Nom        | Vaisseau          |
      | James Kirk | USS Enterprise    |
      | Han Solo   | Faucon Millennium |

  Scénario: Attribution automatique des livraisons de livres à haute priorité
    Quand un nouveau manuscrit rare "Poésie Klingon Ancienne" arrive à la bibliothèque
    Et qu'il est classé comme niveau de priorité 5
    Et qu'il doit être livré à "l'Académie des Sciences de Vulcain"
    Alors le système de surveillance de la bibliothèque devrait détecter le nouveau livre
    Et une alerte devrait être envoyée à tous les vaisseaux disponibles
    Et la livraison devrait être automatiquement attribuée au vaisseau le plus adapté


  Scénario: Ravitaillement d'un vaisseau en carburant
    Étant donné que le "Faucon Millennium" a 50 unités de carburant
    Quand le pilote demande un ravitaillement de 100 unités
    Alors le niveau de carburant devrait être de 150 unités

  Scénario: Fin de mission et retour de livre
    Étant donné que le "USS Enterprise" est assigné à livrer "L'Encyclopédie Galactique"
    Et que le système a enregistré cette mission
    Quand le pilote marque la mission comme terminée
    Alors le livre devrait être enregistré comme livré dans le système
    Et le vaisseau devrait être disponible pour de nouvelles missions