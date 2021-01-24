import unittest

from text.numbers_ca import normalize_numbers_ca


class NumbersCa(unittest.TestCase):
    def test_cardinals(self):
        """
        Converteix cardinals simples en una frase
        """
        self.assertEqual(normalize_numbers_ca("Va nèixer el 23 de desembre de 1988"), "Va nèixer el vint-i-tres de desembre de mil nou-cents vuitanta-vuit")
        self.assertEqual(normalize_numbers_ca("tinc 3 preguntes"), "tinc tres preguntes")
    
    def test_separador_milers(self):
        """
        Ignora separadors de milers
        """
        self.assertEqual(normalize_numbers_ca("1.000"), "mil")
        self.assertEqual(normalize_numbers_ca("323.400"), "tres-cents vint-i-tres mil quatre-cents")
        self.assertEqual(normalize_numbers_ca("900.323.400"), "nou-cents milions tres-cents vint-i-tres mil quatre-cents")
    
    def test_decimals(self):
        """
        Converteix decimals
        """
        self.assertEqual(normalize_numbers_ca("1,33"), "u coma tres tres")
        self.assertEqual(normalize_numbers_ca("75,5"), "setanta-cinc coma cinc")
        self.assertEqual(normalize_numbers_ca("999.999.999,99"), "nou-cents noranta-nou milions nou-cents noranta-nou mil nou-cents noranta-nou coma nou nou")
        self.assertEqual(normalize_numbers_ca("1,12345678900"), "u coma u dos tres quatre cinc sis set vuit nou zero zero")

    def test_decimals_2(self):
        """
        Ignora comes que no pertànyen a un número decimal
        """
        self.assertEqual(normalize_numbers_ca("Va comprar pa, vi i llonganisses"), "Va comprar pa, vi i llonganisses")
        self.assertEqual(normalize_numbers_ca("El número guanyador és 1, 23, 55, 34"), "El número guanyador és u, vint-i-tres, cinquanta-cinc, trenta-quatre")


if __name__ == '__main__':
    unittest.main()
