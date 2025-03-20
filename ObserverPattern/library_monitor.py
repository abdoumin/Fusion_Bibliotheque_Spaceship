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

    def check_for_new_books(self) -> bool:
        """Check if new books have been added to the library

        Returns:
            bool: True if new books were detected, False otherwise
        """
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
            return True  # La méthode retourne maintenant True quand des livres sont détectés

        return False  # Et False quand aucun livre n'est détecté