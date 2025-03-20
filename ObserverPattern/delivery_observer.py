from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BookInfo:
    """Information about books that need delivery"""
    title: str
    destination: str
    priority: int = 1
    special_requirements: list = None

    def __post_init__(self):
        if self.special_requirements is None:
            self.special_requirements = []


class DeliveryObserver(ABC):
    """Observer interface for entities interested in book deliveries"""

    @abstractmethod
    def update(self, book_info: BookInfo) -> None:
        """Receive updates about new books that need delivery"""
        pass



