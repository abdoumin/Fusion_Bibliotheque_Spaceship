class Adresse:
    """
    Class representing an address
    """

    def __init__(self, rue: str = "", ville: str = "", code_postal: str = ""):
        """
        Constructor for objects of class Adresse

        Args:
            rue: The street name
            ville: The city name
            code_postal: The postal code
        """
        self._rue: str = rue
        self._ville: str = ville
        self._code_postal: str = code_postal

    @property
    def rue(self) -> str:
        """Get the street name"""
        return self._rue

    @rue.setter
    def rue(self, value: str) -> None:
        """Set the street name"""
        self._rue = value

    @property
    def ville(self) -> str:
        """Get the city name"""
        return self._ville

    @ville.setter
    def ville(self, value: str) -> None:
        """Set the city name"""
        self._ville = value

    @property
    def code_postal(self) -> str:
        """Get the postal code"""
        return self._code_postal

    @code_postal.setter
    def code_postal(self, value: str) -> None:
        """Set the postal code"""
        self._code_postal = value

    def get_full_address(self) -> str:
        """
        Get the complete formatted address

        Returns:
            The full address as a formatted string
        """
        return f"{self._rue}, {self._ville} {self._code_postal}"