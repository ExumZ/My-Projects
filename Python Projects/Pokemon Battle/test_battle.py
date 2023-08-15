
from tester_base import TesterBase, captured_output
from battle import Battle
import unittest

class Test_battle(TesterBase):
    def test_battle_team_1_win_mode0(self):
        """
        Tests for input Ash : 2 2 2 and Misty : 3 0 0,
        return result = Misty
        """
        from battle import Battle

        try:
            b = Battle("Ash", "Misty")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 2 2\n3 0 0") as (inp, out, err):
                # testing team2 outnumbered, team1 should win
                result = b.set_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Ash"
        except AssertionError:
            self.verificationErrors.append(f"Misty should win: {result}.")

    def test_battle_team_2_win_mode0(self):
        """
        Tests for input Ash : 3 0 0 and Misty : 2 2 2,
        return result = Ash
        """
        from battle import Battle

        try:
            b = Battle("Ash", "Misty")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("3 0 0\n2 2 2") as (inp, out, err):
                # testing team1 outnumbered, team2 should win
                result = b.set_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Misty"
        except AssertionError:
            self.verificationErrors.append(f"Ash should win: {result}.")

    def test_battle_draw_mode0(self):
        """
        Tests for input Ash : 3 0 0 and Misty : 2 2 2,
        return result = Draw
        """
        from battle import Battle

        try:
            b = Battle("Ash", "Misty")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("0 0 6\n0 0 6") as (inp, out, err):
                # testing results for a draw match
                result = b.set_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Draw"
        except AssertionError:
            self.verificationErrors.append(f"It should be a Draw: {result}.")

    def test_battle_team_1_win_mode1(self):
        """
        Tests for input Brock: 2 2 1 and Gary: 0 2 1,
        return result = Brock
        Brock's team after battle = Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 2, Charmander's HP = 7 and level = 2, Bulbasaur's HP = 7 and level = 1, Bulbasaur's HP = 8 and level = 2
        """
        from battle import Battle
        try:
            b = Battle("Brock", "Gary")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 2 1\n0 2 1") as (inp, out, err):
                result = b.rotating_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Brock"
        except AssertionError:
            self.verificationErrors.append(f"Brock should win: {result}.")
        try:
            assert str(b.team1) == "Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 2, Charmander's HP = 7 and level = 2, Bulbasaur's HP = 7 and level = 1, Bulbasaur's HP = 8 and level = 2"
        except AssertionError:
            self.verificationErrors.append(f"Team 1 is not correct after battle: {str(b.team1)}")

    def test_battle_team_2_win_mode1(self):
        """
        Tests for input Brock: 0 2 1 and Gary: 2 2 1,
        return result = Gary
        Gary's team after battle = Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 2, Charmander's HP = 7 and level = 2, Bulbasaur's HP = 7 and level = 1, Bulbasaur's HP = 8 and level = 2
        """
        from battle import Battle
        try:
            b = Battle("Brock", "Gary")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("0 2 1\n2 2 1") as (inp, out, err):
                result = b.rotating_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Gary"
        except AssertionError:
            self.verificationErrors.append(f"Gary should win: {result}.")
        try:
            assert str(b.team2) == "Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 2, Charmander's HP = 7 and level = 2, Bulbasaur's HP = 7 and level = 1, Bulbasaur's HP = 8 and level = 2"
        except AssertionError:
            self.verificationErrors.append(f"Team 2 is not correct after battle: {str(b.team1)}")

    def test_battle_Draw_mode1(self):
        """
        Tests for input Brock: 2 2 2 and Gary: 2 2 2,
        return result = Draw
        Teams after battle = ""
        """
        from battle import Battle
        try:
            b = Battle("Brock", "Gary")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 2 2\n2 2 2") as (inp, out, err):
                result = b.rotating_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Draw"
        except AssertionError:
            self.verificationErrors.append(f" It should be a Draw: {result}.")
        try:
            assert str(b.team1) == ""
        except AssertionError:
            self.verificationErrors.append(f"Team 1 should be empty: {str(b.team1)}")
        try:
            assert str(b.team2) == ""
        except AssertionError:
            self.verificationErrors.append(f"Team 2 should be empty: {str(b.team2)}")

    def test_battle_random_numbers_114_312(self):
        """
        Tests for input Brock: 1 1 4 and Gary: 3 1 2,
        return result = Gary
        Teams after battle = Bulbasaur's HP = 6 and level = 3
        """
        from battle import Battle
        try:
            b = Battle("Brock", "Gary")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("1 1 4\n3 1 2") as (inp, out, err):
                result = b.rotating_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Gary"
        except AssertionError:
            self.verificationErrors.append(f"Gary should win: {result}.")
        try:
            assert str(b.team2) == "Bulbasaur's HP = 6 and level = 3"
        except AssertionError:
            self.verificationErrors.append(f"Team 2 is not correct after battle: {str(b.team1)}")

    def test_battle_team_1_win_mode2(self):
        """
        Tests for input Cynthia: 2 2 1 and Steven: 0 2 1,
        return result = Cynthia
        Cynthia's team after battle = Bulbasaur's HP = 6 and level = 1, Bulbasaur's HP = 5 and level = 2, Squirtle's HP = 2 and level = 1
        """
        from battle import Battle
        try:
            b = Battle("Cynthia", "Steven")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 2 1\n0 2 1") as (inp, out, err):
                result = b.optimised_mode_battle("hp", "lvl")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Cynthia"
        except AssertionError:
            self.verificationErrors.append(f"Cynthia should win: {result}.")
        try:
            assert str(b.team1) == "Bulbasaur's HP = 6 and level = 1, Bulbasaur's HP = 5 and level = 2, Squirtle's HP = 2 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"Team 1 is not correct after battle: {str(b.team1)}")

    def test_battle_team_2_win_mode2(self):
        """
        Tests for input Cynthia: 0 2 1 and Steven: 2 2 1,
        return result = Steven
        Steven's team after battle = Bulbasaur's HP = 8 and level = 2, Squirtle's HP = 8 and level = 1, Bulbasaur's HP = 9 and level = 1
        """
        from battle import Battle

        try:
            b = Battle("Cynthia", "Steven")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("0 2 1\n2 2 1") as (inp, out, err):
                result = b.optimised_mode_battle("hp", "lvl")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Steven"
        except AssertionError:
            self.verificationErrors.append(f"Steven should win: {result}.")
        try:
            assert str(b.team2) == "Bulbasaur's HP = 8 and level = 2, Squirtle's HP = 8 and level = 1, Bulbasaur's HP = 9 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"Team 2 is not correct after battle: {str(b.team1)}")

    def test_battle_Draw_mode2(self):
        """
        Tests for input Cynthia: 2 2 2 and Steven: 2 2 2,
        return result = Draw
        Teams after battle = ""
        """
        from battle import Battle

        try:
            b = Battle("Cynthia", "Steven")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 2 2\n2 2 2") as (inp, out, err):
                result = b.optimised_mode_battle("hp", "hp")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Draw"
        except AssertionError:
            self.verificationErrors.append(f"It should be a Draw: {result}.")
        try:
            assert str(b.team1) == ""
        except AssertionError:
            self.verificationErrors.append(f"Team 1 should be empty: {str(b.team1)}")
        try:
            assert str(b.team2) == ""
        except AssertionError:
            self.verificationErrors.append(f"Team 2 should be empty: {str(b.team2)}")

    def test_battle_spd_def_212_123(self):
        """
        Test for speed and defense criterion in optimised battle mode
        Tests for input Cynthia: 2 1 2 and Steven: 1 2 3,
        return result = Steven
        Teams after battle = Bulbasaur's HP = 2 and level = 4, Bulbasaur's HP = 9 and level = 1, Charmander's HP = 7 and level = 1
        """
        from battle import Battle
        try:
            b = Battle("Cynthia", "Steven")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 1 2\n1 2 3") as (inp, out, err):
                result = b.optimised_mode_battle("spd", "def")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Steven"
        except AssertionError:
            self.verificationErrors.append(f"Steven should win: {result}.")
        try:
            assert str(b.team2) == "Bulbasaur's HP = 2 and level = 4, Bulbasaur's HP = 9 and level = 1, Charmander's HP = 7 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"Team 2 is not correct after battle: {str(b.team1)}")

    def test_battle_atk_spd_411_033(self):
        """
        Test for attack and speed criterion in optimised battle mode
        Tests for input Cynthia: 4 1 1 and Steven: 0 3 3,
        return result = Steven
        Teams after battle = Bulbasaur's HP = 2 and level = 3
        """
        from battle import Battle
        try:
            b = Battle("Cynthia", "Steven")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("4 1 1\n0 3 3") as (inp, out, err):
                result = b.optimised_mode_battle("atk", "spd")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Steven"
        except AssertionError:
            self.verificationErrors.append(f"Steven should win: {result}.")
        try:
            assert str(b.team2) == "Bulbasaur's HP = 2 and level = 3"
        except AssertionError:
            self.verificationErrors.append(f"Team 2 is not correct after battle: {str(b.team1)}")

    def test_set_mode_battle_missingno(self):
        """
        Tests MissingNo in set_mode_battle(), and checks if MissingNo is the last pokemon in the battle
        Tests for input Ash: 1 1 1 1 and Brock: 1 1 1 0,
        return result = Ash
        Teams after battle = MissingNo's HP = 8 and level = 1
        """
        from battle import Battle
        try:
            b = Battle("Ash", "Brock")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("1 1 1 1\n1 1 1 0") as (inp, out, err):
                result = b.set_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Ash"
        except AssertionError:
            self.verificationErrors.append(f"Ash should win: {result}.")
        try:
            assert str(b.team1) == "MissingNo's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"Team 1 is not correct after battle: {str(b.team1)}")

    def test_rotating_mode_battle_missingno(self):
        """
        Tests MissingNo in rotation_mode_battle(), and checks if MissingNo properly battles
        Since all pokemon would only battle once, and the stats for MissingNo varies, this will only check if Ash wins.

        Tests for input Ash: 2 1 2 1 and Brock: 2 1 2 0,
        return result = Ash
        """
        from battle import Battle
        try:
            b = Battle("Ash", "Brock")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 1 2 1\n2 1 2 0") as (inp, out, err):
                result = b.rotating_mode_battle()
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Ash"
        except AssertionError:
            self.verificationErrors.append(f"Ash should win: {result}.")

    def test_optimised_mode_battle_missingno(self):
        """
        Tests MissingNo in optimised_mode_battle(), and checks if MissingNo properly battles
        Since all pokemon would only battle once, and the stats for MissingNo varies, this will only check if Ash wins.

        Tests for input Ash: 2 1 2 1 and Brock: 2 1 2 0,
        return result = Ash
        """
        from battle import Battle
        try:
            b = Battle("Ash", "Brock")
        except Exception as e:
            self.verificationErrors.append(f"Battle could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("2 1 2 1\n2 1 2 0") as (inp, out, err):
                result = b.optimised_mode_battle("hp","spd")
        except Exception as e:
            self.verificationErrors.append(f"Battle failed to execute: {str(e)}.")
            return
        try:
            assert result == "Ash"
        except AssertionError:
            self.verificationErrors.append(f"Ash should win: {result}.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_battle)
    unittest.TextTestRunner(verbosity=0).run(suite)
