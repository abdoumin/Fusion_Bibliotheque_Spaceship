# biblio_test.py - Version améliorée
import unittest
from .bibliotheque import Bibliotheque
from .adresse import Adresse


class BibliothequeTestCase(unittest.TestCase):
    """
    Test class for Bibliotheque with comprehensive test coverage
    """

    def setUp(self):
        """
        Sets up the test fixture with a bibliotheque and adresse.
        Called before each test method.
        """
        self.biblio = Bibliotheque()
        self.biblio.nom = "BPU"
        self.biblio.nombre_de_livres = 1000

        self.adresse = Adresse()
        self.adresse.rue = "Chatelet des halles"
        self.adresse.code_postal = "75015"
        self.adresse.ville = "Paris"

        self.biblio.adresse = self.adresse

        # Create a library without address for edge case testing
        self.biblio_sans_adresse = Bibliotheque()
        self.biblio_sans_adresse.nom = "Petite Bibliothèque"
        self.biblio_sans_adresse.nombre_de_livres = 250

    def test_afficher_details(self):
        """
        Test the afficher_details method returns the correct string.
        """
        expected = f"Le nom : {self.biblio.nom} Le nombre de pages : {self.biblio.nombre_de_livres}"
        self.assertEqual(self.biblio.afficher_details(), expected)

    def test_get_description(self):
        """
        Test the get_description method returns the correct string with address.
        """
        expected = "Bibliothèque: BPU (1000 livres), Localisation: Chatelet des halles, Paris 75015"
        self.assertEqual(self.biblio.get_description(), expected)

    def test_get_description_sans_adresse(self):
        """
        Test the get_description method for a library without an address.
        """
        expected = "Bibliothèque: Petite Bibliothèque (250 livres), Pas d'adresse renseignée."
        self.assertEqual(self.biblio_sans_adresse.get_description(), expected)

    def test_modifier_adresse(self):
        """
        Test that changing address properties reflects in the library description.
        """
        self.adresse.ville = "Lyon"
        self.adresse.code_postal = "69000"
        expected = "Bibliothèque: BPU (1000 livres), Localisation: Chatelet des halles, Lyon 69000"
        self.assertEqual(self.biblio.get_description(), expected)



if __name__ == '__main__':
    unittest.main()