from stack_adt import ArrayStack
from queue_adt import CircularQueue
from sorted_list import ListItem
from array_sorted_list import ArraySortedList

from pokemon_base import PokemonBase
from pokemon import Charmander
from pokemon import Bulbasaur
from pokemon import Squirtle
from glitchmon import GlitchMon
from pokemon import MissingNo
from poke_team import PokeTeam
from tester_base import TesterBase, captured_output
import unittest


class Test_poke_team(TesterBase):

    def test_limit(self):
        try:
            team = PokeTeam("Ash")
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("0 0 0 2\n1 1 1 1") as (inp, out, err):
                # 0 0 0 2 should fail. Too many missingos.
                # So 1 1 1 1 should be the correct team.
                team.choose_team(0, None)
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
            return
        output = out.getvalue().strip()
        try:
            assert str(team) == "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1, MissingNo's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_str_1(self):
        team = PokeTeam("Ash")
        try:
            with captured_output("1 0 0 2\n1 1 1 1") as (inp, out, err):
                # 1 0 0 2 should fail. Too many missingos.
                # So 1 1 1 1 should be the correct team.
                team.choose_team(0, None)
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1, MissingNo's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_str_2(self):
        team = PokeTeam("Ash")
        try:
            with captured_output("1 0 \n1 1 2") as (inp, out, err):
                # 1 0 should fail. Due to not enough inputs.
                # So 1 1 2 should be the correct team.
                team.choose_team(1, None)
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1, Squirtle's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_str_3(self):
        team = PokeTeam("Ash")
        try:
            with captured_output("1 0 \n1 1 1 1") as (inp, out, err):
                # 1 0 should fail. Too many missingos.
                # So 1 1 1 1 should be the correct team.
                team.choose_team(2, "hp")
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Bulbasaur's HP = 9 and level = 1, MissingNo's HP = 8 and level = 1, Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_choose_team_1(self):
        # tests if more than 6 pokemon will cause another prompt for input
        team=PokeTeam("Ash")
        try:
            with captured_output("7 0 0 \n1 1 1 1") as (inp, out, err):
                # 7 0 0 should fail. Too many pokemon
                # So 1 1 1 1 should be the correct team.
                team.choose_team(0, None)
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1, MissingNo's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_choose_team_2(self):
        # test if no input will prompt another input
        team=PokeTeam("Ash")
        try:
            with captured_output(" \n1 1 1") as (inp, out, err):
                #  should fail. There is no input
                # So 1 1 1 should be the correct team.
                team.choose_team(2, "hp")
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1, Charmander's HP = 7 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_set_battle_mode_1(self):
        # not initialise by user, will get default value which is 0
        team=PokeTeam("Ash")

        self.assertEqual(team.battle_mode, 0)

    def test_set_battle_mode_2(self):
        # when user initialise battle_mode to 1
        team=PokeTeam("Ash",1)

        self.assertEqual(team.battle_mode, 1)

    def test_set_battle_mode_3(self):
        # when user initialise battle_mode to 2
        team=PokeTeam("Ash",2)

        self.assertEqual(team.battle_mode, 2)

    def test_assign_team(self):
        # assign_team() is a method called inside choose_team() and is not explicitly called by the user
        team=PokeTeam("Ash")
        try:
            with captured_output("0 0 0\n1 1 1") as (inp, out, err):
                #  should fail. There is no input
                # So 1 1 1 should be the correct team.
                team.choose_team(0)
        except Exception as e:
            self.verificationErrors.append(f"Ash's team could not be chosen: {str(e)}.")
        try:
            assert str(team) == "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1"
        except AssertionError:
            self.verificationErrors.append(f"PokeTeam does not handle limit correctly. {str(team)}")

    def test_give_criterion_1(self):
        # when criteria is HP
        c=Charmander()
        team=PokeTeam("Ash",2)
        self.assertEqual(team._give_criterion(c,"HP").value, ListItem(c, c.get_hp()).value)

    def test_give_criterion_2(self):
        # when criterion is Speed
        b=Bulbasaur()
        team=PokeTeam("Ash",2)
        self.assertEqual(team._give_criterion(b,"Speed").value, ListItem(b, b.get_speed()).value)

    def test_give_criterion_3(self):
        # when criterion is None
        s=Squirtle()
        team=PokeTeam("Ash",2)
        self.assertEqual(team._give_criterion(s).value, ListItem(s, 0).value)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_poke_team)
    unittest.TextTestRunner(verbosity=0).run(suite)
