Feature: US_001 Gestion des pilotes et vaisseaux spatiaux

En tant que Commandant de mission
Je veux pouvoir assigner des pilotes à des vaisseaux
Afin de garantir que chaque mission dispose d'un équipage qualifié

Scenario Outline: Assignation d'un pilote à un vaisseau
Given un vaisseau spatial "<vaisseau>" avec une capacité de "<capacité>" pilotes
When un pilote "<pilote>" est assigné à ce vaisseau
Then le pilote doit apparaître dans la liste des pilotes du vaisseau

Examples:
| vaisseau          | capacité | pilote       |
| Enterprise        | 5        | Jean-Luc     |
| Millennium Falcon | 2        | Han Solo     |
| Discovery         | 3        | Dave Bowman  |

Scenario Outline: Gestion du carburant lors d'un voyage
Given un vaisseau spatial "<vaisseau>" avec un niveau de carburant de "<carburant>" unités
When il tente de voyager en consommant "<consommation>" unités
Then il doit afficher le message "<résultat>"

Examples:
| vaisseau          | carburant | consommation | résultat                       |
| Enterprise        | 100       | 50           | Voyage réussi, reste 50 unités |
| Millennium Falcon | 20        | 30           | Carburant insuffisant          |
| Discovery         | 75        | 25           | Voyage réussi, reste 50 unités |

Scenario Outline: Refus d'affectation d'un pilote déjà assigné
Given un pilote "<pilote>" déjà assigné au vaisseau "<vaisseau1>"
When on tente de l'assigner à un autre vaisseau "<vaisseau2>"
Then le système refuse avec le message "<messageErreur>"

Examples:
| pilote      | vaisseau1        | vaisseau2      | messageErreur        |
| Jean-Luc    | Enterprise       | Discovery      | Pilote déjà assigné  |
| Han Solo    | Millennium Falcon| Star Destroyer | Pilote déjà assigné  |
| Dave Bowman | Discovery        | Odyssey        | Pilote déjà assigné  |