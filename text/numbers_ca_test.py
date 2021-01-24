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
        self.assertEqual(normalize_numbers_ca("1,33"), "u coma trenta-tres")
        self.assertEqual(normalize_numbers_ca("75,5"), "setanta-cinc coma cinc")
        self.assertEqual(normalize_numbers_ca("75,555"), "setanta-cinc coma cinc-cents cinquanta-cinc")
        self.assertEqual(normalize_numbers_ca("999.999.999,99"), "nou-cents noranta-nou milions nou-cents noranta-nou mil nou-cents noranta-nou coma noranta-nou")
        self.assertEqual(normalize_numbers_ca("1,12345678900"), "u coma dotze trenta-quatre cinquanta-sis set-cents vuitanta-nou")

    def test_decimals_2(self):
        """
        Ignora comes que no pertànyen a un número decimal
        """
        self.assertEqual(normalize_numbers_ca("Va comprar pa, vi i llonganisses"), "Va comprar pa, vi i llonganisses")
        self.assertEqual(normalize_numbers_ca("El número guanyador és 1, 23, 55, 34"), "El número guanyador és u, vint-i-tres, cinquanta-cinc, trenta-quatre")

    def test_ordinals_ms(self):
        """
        Converteix ordinals masculins singulars
        """
        self.assertEqual(normalize_numbers_ca("Va arribar 4t de 5"), "Va arribar quart de cinc")
        self.assertEqual(normalize_numbers_ca("el 1r va ser ell"), "el primer va ser ell")
        self.assertEqual(normalize_numbers_ca("el 3er, no va aguantar"), "el tercer, no va aguantar")
        self.assertEqual(normalize_numbers_ca("2n"), "segon")
        self.assertEqual(normalize_numbers_ca("2on"), "segon")
        self.assertEqual(normalize_numbers_ca("4t"), "quart")
        self.assertEqual(normalize_numbers_ca("4rt"), "quart")
        self.assertEqual(normalize_numbers_ca("5è: remogueu la barreja"), "cinquè: remogueu la barreja")
        self.assertEqual(normalize_numbers_ca("6e"), "sisè")
        self.assertEqual(normalize_numbers_ca("6e"), "sisè")
        self.assertEqual(normalize_numbers_ca("21nè"), "vint-i-unè")
        self.assertEqual(normalize_numbers_ca("un 81ne de Palamós"), "un vuitanta-unè de Palamós")

    def test_ordinals_fs(self):
        """
        Converteix ordinals femenins singulars
        """
        self.assertEqual(normalize_numbers_ca("1a"), "primera")
        self.assertEqual(normalize_numbers_ca("3ra"), "tercera")
        self.assertEqual(normalize_numbers_ca("2a"), "segona")
        self.assertEqual(normalize_numbers_ca("2na"), "segona")
        self.assertEqual(normalize_numbers_ca("4a."), "quarta.")
        self.assertEqual(normalize_numbers_ca("pugi a la 4ta, després giri a l'esquerra"), "pugi a la quarta, després giri a l'esquerra")
        self.assertEqual(normalize_numbers_ca("va quedar 5a en la classificació"), "va quedar cinquena en la classificació")
        self.assertEqual(normalize_numbers_ca("la 5na vegada"), "la cinquena vegada")

    def test_ordinals_mp(self):
        """
        Converteix ordinals masculins plurals
        """
        self.assertEqual(normalize_numbers_ca("1rs"), "primers")
        self.assertEqual(normalize_numbers_ca("van arribar 2ns"), "van arribar segons")
    
    @unittest.skip("Encara no ha estat implementat a soros")
    def test_ordinals_fp(self):
        """
        Converteix ordinals femenins plurals
        """
        self.assertEqual(normalize_numbers_ca("1es"), "primeres")
    
    def test_fraccions_s(self):
        """
        Converteix fraccions singulars
        """
        self.assertEqual(normalize_numbers_ca("1/2 got de vi"), "mig got de vi")
        self.assertEqual(normalize_numbers_ca("1/3 de farina"), "un terç de farina")
        self.assertEqual(normalize_numbers_ca("1/8"), "un vuitè")
        
    def test_fraccions_p(self):
        """
        Converteix fraccions plurals
        """
        self.assertEqual(normalize_numbers_ca("4/2 gots de vi"), "quatre migs gots de vi")
        self.assertEqual(normalize_numbers_ca("2/3 de farina"), "dos terços de farina")
        self.assertEqual(normalize_numbers_ca("3/8"), "tres vuitens")
        
if __name__ == '__main__':
    unittest.main()
