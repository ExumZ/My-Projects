import unittest
from tester_base import TesterBase
from pokemon import Charmander, Squirtle, Bulbasaur, MissingNo


class Test_PokemonBase(TesterBase):

    # Tester for set_hp method
    def test_set_hp(self):
        charm = Charmander()

        with self.assertRaises(ValueError):
            charm.set_hp(-1)

        with self.assertRaises(TypeError):
            charm.set_hp("a")

    # Tester for set_level method
    def test_set_level(self):
        charm = Charmander()

        with self.assertRaises(ValueError):
            charm.set_level(-1)

        with self.assertRaises(TypeError):
            charm.set_level("a")

    # Tester for get_hp method
    def test_get_hp(self):
        charm = Charmander()

        self.assertEqual(charm.get_hp(), charm.hp)

    # Tester for get_level method
    def test_get_level(self):
        charm = Charmander()

        self.assertEqual(charm.get_level(), charm.level)

    # Tester for get_pokeType method
    def test_get_pokeType(self):
        charm = Charmander()

        self.assertEqual(charm.get_pokeType(), charm.poke_type)


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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_PokemonBase)
    unittest.TextTestRunner(verbosity=0).run(suite)
