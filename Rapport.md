
### **Un Voyage Intergalactique du Savoir🚀**
Dans un avenir lointain, la Bibliothèque Intergalactique permet aux civilisations éloignées d'accéder à la connaissance universelle. Des vaisseaux spatiaux spécialement conçus parcourent l'univers pour livrer des manuscrits rares et récupérer de nouveaux ouvrages. Pour garantir la fluidité des missions, un système informatique avancé gère les emprunts et les livraisons des livres ainsi que l'affectation des pilotes.


---

### **Design Patterns Utilisés**

#### **a. Adapter Pattern (Pattern d'Adaptation)**
- **Problème** : Les vaisseaux spatiaux ne sont pas initialement conçus pour être gérés comme des livres dans une bibliothèque.
- **Solution** : Un `SpaceshipAdapter` permet d'utiliser les vaisseaux comme des livres empruntables.

➡ **Code associé :**  
`AdapterPattern/spaceship_adapter.py` qui adapte un vaisseau pour être géré comme un livre.
```Python
from Bibliotheque.livre import Livre
from SpaceShip.spaceship_model import Spaceship
from Bibliotheque.membre import Membre


class SpaceshipAdapter(Livre):
    """Adapter transforming a Spaceship into a borrowable book-like object"""

    def __init__(self, spaceship: Spaceship):
        super().__init__(isbn=spaceship.name, titre=f"Vaisseau: {spaceship.name}")
        self.spaceship = spaceship
        self.emprunteur = None  # Membre qui a emprunté le vaisseau

    def est_disponible(self) -> bool:
        """Check if the spaceship is available for borrowing"""
        return self.emprunteur is None

    def emprunter(self, membre: Membre) -> bool:
        """Allow a member to borrow the spaceship"""
        if self.est_disponible():
            self.emprunteur = membre
            self.statut = "Emprunté"
            return True
        return False

    def retourner(self) -> bool:
        """Return the spaceship and reset borrower"""
        if self.emprunteur:
            self.emprunteur = None
            self.statut = "Disponible"
            return True
        return False

```
---

#### **b. Observer Pattern (Pattern d'Observation)**
- **Problème** : Lorsqu'un nouveau livre arrive dans la bibliothèque, les vaisseaux spatiaux doivent être informés pour organiser leur transport.
- **Solution** : Un `LibraryMonitor` surveille les ajouts de livres et notifie les vaisseaux disponibles.

➡ **Code associé :**  
- `ObserverPattern/library_monitor.py` qui implémente le pattern Observer en surveillant les nouveaux livres.  
```python
from ObserverPattern.delivery_observer import DeliveryObserver, BookInfo


class LibraryMonitor:
    """Monitors a library and notifies observers about new books"""

    def __init__(self, bibliotheque):
        self._bibliotheque = bibliotheque
        self._observers = []
        self._last_book_count = bibliotheque.nombre_de_livres

    def add_observer(self, observer: DeliveryObserver) -> None:
        """Add an observer to the notification list"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: DeliveryObserver) -> None:
        """Remove an observer from the notification list"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, book_info: BookInfo) -> None:
        """Notify all observers about new books"""
        for observer in self._observers:
            observer.update(book_info)

    def check_for_new_books(self) -> None:
        """Check if new books have been added to the library"""
        current_count = self._bibliotheque.nombre_de_livres
        if current_count > self._last_book_count:
            # In a real implementation, we would get details about the new books
            # For now, we'll use a placeholder BookInfo
            new_books_count = current_count - self._last_book_count
            book_info = BookInfo(
                title=f"{new_books_count} new books",
                destination="Various destinations",
                priority=2
            )
            self.notify_observers(book_info)
            self._last_book_count = current_count
```
- `ObserverPattern/delivery_system.py` qui enregistre les vaisseaux comme observateurs.
```Python
from ObserverPattern.library_monitor import LibraryMonitor
from ObserverPattern.spaceship import Spaceship


class DeliverySystem:
    """Facade for setting up the entire observer system"""

    @staticmethod
    def initialize(bibliotheque) -> LibraryMonitor:
        """Initialize the library monitoring system"""
        monitor = LibraryMonitor(bibliotheque)
        print(f"Monitoring initialized for library: {bibliotheque.nom}")
        return monitor

    @staticmethod
    def register_spaceship(monitor: LibraryMonitor, ship: Spaceship) -> None:
        """Register a spaceship with the library monitor"""
        monitor.add_observer(ship)
        print(f"Spaceship {ship.name} registered for delivery missions")
```
---

### **Diagramme de Classe Simplifié**


➡ **Code associé :**  
Les classes de `Bibliotheque`, `SpaceshipAdapter`, `LibraryMonitor`, `Spaceship` et `Pilot` sont définies dans les fichiers suivants :  
- `Bibliotheque/bibliotheque.py`
- `AdapterPattern/spaceship_adapter.py`
- `ObserverPattern/library_monitor.py`
- `SpaceShip/spaceship_model.py`
- `SpaceShip/pilot_model.py`

---

### **User Stories et Critères d'Acceptance**

#### **US_001: En tant que pilote, je veux emprunter un vaisseau pour une mission**
**Critères d'acceptance**:
- Le pilote doit être qualifié pour le vaisseau.
- Le vaisseau doit avoir du carburant.
- Le vaisseau doit être disponible.

➡ **Code associé :**  
- `AdapterPattern/member_pilote.py` qui vérifie si un pilote peut emprunter un vaisseau.  
```Python
# bibliotheque/models.py
from Bibliotheque.membre import Membre


class MembrePilote(Membre):
    """Extended member class with piloting capabilities"""

    def __init__(self, nom, numero):
        super().__init__(nom, numero)
        self._qualification_level = 0
        self._flight_hours = 0

    @property
    def qualification_level(self):
        return self._qualification_level

    @qualification_level.setter
    def qualification_level(self, level):
        if 0 <= level <= 5:  # 5 levels of qualification
            self._qualification_level = level

    @property
    def flight_hours(self):
        return self._flight_hours

    def log_flight_hours(self, hours):
        """Add flight hours to the member's record"""
        if hours > 0:
            self._flight_hours += hours
            # Automatically upgrade qualification if enough hours
            if self._flight_hours > 100 and self._qualification_level < 5:
                self._qualification_level += 1

    def can_pilot(self, spaceship_adapter):
        """Check if the member can pilot a particular spaceship"""
        # Règle simple : Enterprise et Millennium Falcon nécessitent un niveau 4+
        spaceship_name = spaceship_adapter.spaceship.name
        if spaceship_name in ["Enterprise", "Millennium Falcon"]:
            required_level = 4
        else:  # Les autres vaisseaux nécessitent un niveau 2+
            required_level = 2

        return self._qualification_level >= required_level
```

- `AdapterPattern/intergalactic_mission_service.py` qui gère l'affectation des vaisseaux aux pilotes.
```Python
def prepare_mission(self, spaceship_name: str, pilot_membre: MembrePilote, destination: str,
                    books_to_transport: list) -> Optional[int]:
    """
    Prepare an intergalactic knowledge exchange mission
    Returns mission ID if successful, None otherwise
    """
    # Reset last error
    self.last_error = None

    # Check if spaceship is available
    spaceship_adapter = self.bibliotheque.get_spaceship(spaceship_name)
    if not spaceship_adapter or not spaceship_adapter.est_disponible():
        self.last_error = "Vaisseau non disponible"
        return None

    # Check if member is qualified
    if not pilot_membre.can_pilot(spaceship_adapter):
        self.last_error = "Niveau de qualification insuffisant"
        return None

    # Borrow spaceship and books
    if not self.bibliotheque.borrow_spaceship(spaceship_name, pilot_membre):
        self.last_error = "Échec de l'emprunt du vaisseau"
        return None

```
---

#### **US_002: En tant que bibliothécaire, je veux que les vaisseaux soient alertés d'un nouveau livre**
**Critères d'acceptance**:
- Lorsqu'un livre est ajouté, les vaisseaux disponibles reçoivent une notification.
- Les vaisseaux peuvent accepter ou refuser la mission.

➡ **Code associé :**  
- `ObserverPattern/library_monitor.py` qui envoie une notification aux vaisseaux.
```Python
```
- `ObserverPattern/spaceship.py` qui reçoit les notifications et décide d'accepter ou non la mission.

---

### **Tests Fonctionnels et Unitaires**

#### **Tests fonctionnels : Scénarios d'utilisation avec Behave (BDD)**
- Simulation de mission intergalactique.
- Test de la gestion des réservations de vaisseaux.

➡ **Code associé :**  
- `AdapterPattern/features/mission_intergalactique.feature` qui définit des scénarios de test pour l'emprunt de vaisseaux.  
- `AdapterPattern/features/steps/mission_steps.py` qui implémente ces scénarios avec Behave.

#### **Tests unitaires : Unittest pour tester les classes et leurs méthodes**
- `Spaceship.travel()` pour valider la consommation de carburant.
- `LibraryMonitor.check_for_new_books()` pour la détection des nouveaux livres.

➡ **Code associé :**  
- `SpaceShip/test_spaceship.py` qui teste les méthodes du vaisseau spatial.  
- `Bibliotheque/biblio_test.py` qui teste la gestion des bibliothèques.

---

### **Escalade des Tests et Couverture**
**Escalade :**
- Unitaires → Intégration → Fonctionnels.

**Couverture :**
- Code analysé avec un outil comme Coverage.py.
- Objectif : 90% de couverture des classes critiques.

➡ **Code associé :**  
- `SpaceShip/test_spaceship.py` pour les tests unitaires.  
- `AdapterPattern/features/steps/mission_steps.py` pour les tests fonctionnels.

---

### **Gestion du Projet avec Git**
**Organisation :**
- `main` : Branche stable.
- `dev` : Branche de développement.
- `feature/xxx` : Branches par fonctionnalité.

**Bonnes pratiques :**
- Commits clairs et concis.
- PR avec revue de code.
- Utilisation de GitHub Actions pour l'intégration continue.

