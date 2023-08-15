import unittest

from sorted_list import ListItem

from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
from poke_team import PokeTeam
from glitchmon import GlitchMon
from tester_base import TesterBase, captured_output

class Test_pokemon(TesterBase):

    # Tester for get_name method
    def test_get_name(self):
        charm = Charmander()

        self.assertEqual(charm.get_name(), charm.name)

    # Tester for get_attack method
    def test_get_attack(self):
        charm = Charmander()

        self.assertEqual(charm.get_attack(), (charm.level + 6))

    # Tester for get_defense method
    def test_get_defense(self):
        charm = Charmander()

        self.assertEqual(charm.get_defense(), 4)

    # Tester for get_speed method
    def test_get_speed(self):
        charm = Charmander()

        self.assertEqual(charm.get_speed(), (charm.level + 7))

    # Tester for calculate_damage method
    def test_calculate_damage(self):
        charm = Charmander()
        squirt = Squirtle()

        self.assertEqual(charm.calculate_damage(squirt), 8)

    # Tester for type_effectiveness method
    def test_type_effectiveness(self):
        charm = Charmander()
        squirt = Squirtle()

        self.assertEqual(charm.type_effectiveness(charm.poke_type, squirt.poke_type, squirt.get_attack()), 8)

    # Tester for get_battled method
    def test_get_battled(self):
        charm = Charmander()

        self.assertEqual(charm.get_battled(), False)

    # Tester for has_battled method
    def test_has_battled(self):
        charm = Charmander()
        charm.has_battled()

        self.assertEqual(charm.get_battled(), True)

    # Tester for __str__ method
    def test_str(self):
        charm = Charmander()
        string = charm.__str__()
        self.assertEqual(string, "Charmander's HP = 7 and level = 1")

    def test_charmander_string(self):
        try:
            c = Charmander()
        except Exception as e:
            self.verificationErrors.append(f"Charmander could not be instantiated: {str(e)}.")
            return
        try:
            s = str(c)
            if s != "Charmander's HP = 7 and level = 1":
                self.verificationErrors.append(f"String method did not return correct string: {s}")
        except Exception as e:
            self.verificationErrors.append(f"String method failed. {e}")

    def test_squirtle_string(self):
        try:
            c = Squirtle()
        except Exception as e:
            self.verificationErrors.append(f"Squirtle could not be instantiated: {str(e)}.")
            return
        try:
            s = str(c)
            if s != "Squirtle's HP = 8 and level = 1":
                self.verificationErrors.append(f"String method did not return correct string: {s}")
        except Exception as e:
            self.verificationErrors.append(f"String method failed. {e}")

    def test_bulbasaur_string(self):
        try:
            c = Bulbasaur()
        except Exception as e:
            self.verificationErrors.append(f"Bulbasaur could not be instantiated: {str(e)}.")
            return
        try:
            s = str(c)
            if s != "Bulbasaur's HP = 9 and level = 1":
                self.verificationErrors.append(f"String method did not return correct string: {s}")
        except Exception as e:
            self.verificationErrors.append(f"String method failed. {e}")

    def test_missingno_string(self):
        try:
            miss = MissingNo()
        except Exception as e:
            self.verificationErrors.append(f"MissingNo could not be instantiated: {str(e)}.")
            return
        try:
            s = str(miss)
            if s != "MissingNo's HP = 8 and level = 1":
                self.verificationErrors.append(f"String method did not return correct string: {s}")
        except Exception as e:
            self.verificationErrors.append(f"String method failed. {e}")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_pokemon)
    unittest.TextTestRunner(verbosity=0).run(suite)
