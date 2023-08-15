import unittest
from tester_base import TesterBase, captured_output
from glitchmon import GlitchMon
from pokemon import MissingNo

class Test_GlitchMon(TesterBase):

    # Tester for superpower method
    def test_superpower(self):
        miss = MissingNo()
        miss.superpower()

        # After superpower(), MissingNo's hp and level should add up to be greater than 9
        self.assertGreater((miss.get_hp() + miss.get_level()), 9, "superpower() did not work")

        # Tester for increase_lvl method
    def test_increase_lvl(self):
        miss = MissingNo()
        miss.increase_lvl()

        self.assertEqual(miss.get_level(), 2)

        # Tester for increase_hp method
    def test_increase_hp(self):
        miss = MissingNo()
        miss.increase_hp()

        self.assertEqual(miss.get_hp(), 9)

    def test_MissingNo_string(self):
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
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_GlitchMon)
    unittest.TextTestRunner(verbosity=0).run(suite)
