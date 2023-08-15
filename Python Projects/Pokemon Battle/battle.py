""" Implementation of the Battle class

Defines the Battle class. The code contains 3 main methods,
set_mode_battle(), rotating_mode_battle() and optimised_mode_battle(), that are implemented based on Task 3, 4 and 5
in the Assignment Specification

Contains 7 other methods used in the main functions mentioned above, the details are described in their respective methods:
_calculate_damage_with_speed(), _level_up(), _deduct_hp(), _update_pokemon_pos(), _return_results(), check_battled(), get_MissingNo_index()

Many of these methods are called in all 3 of the main methods mentioned above.

There are 2 redundant methods that are used for debugging purposes. They are used to print statements during each of the battle modes
_battle_outcome(), _battle_outcome_2()

"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

from poke_team import PokeTeam
from pokemon_base import PokemonBase
from glitchmon import GlitchMon


class Battle:
    # constructor
    def __init__(self, trainer_one_name: str, trainer_two_name: str):
        self.trainer_one_name = trainer_one_name
        self.trainer_two_name = trainer_two_name

        # extra instance variable
        self.battle_mode = None

        # creating empty teams
        self.team1 = PokeTeam(trainer_one_name)
        self.team2 = PokeTeam(trainer_two_name)

    def set_mode_battle(self) -> str:
        """
        Task 3:
        battle mode where each pokemon battle until any or all teams loses all their pokemon

        :pre: none, all preconditions checked prior to execution
        :Complexity:
                    Both Best and Worst Case Complexity: O(n)
        :return: str, "(name of winning team)" or "Draw"
        """
        # setting battle mode to 0 : O(n)/O(nlogn)
        self.team1.choose_team(0)
        self.team2.choose_team(0)
        # user input for teams

        t1 = self.team1.team_content
        t2 = self.team2.team_content

        # check if teams are empty : O(n)
        while not t1.is_empty() and not t2.is_empty():  # make sure both teams are not empty before battle

            # accessing the current pokemon : O(1)
            unit1 = t1.access(0)
            unit2 = t2.access(0)

            # calculates the damage of pokemon using speed of each pokemon : O(1)
            self._calculate_damage_with_speed(unit1, unit2)
            # calculates damage taken after the battle, and which pokemon has fainted : O(1)
            self._deduct_hp(unit1, unit2)

            # update if pokemon has battled : O(1)
            unit1.has_battled()
            unit2.has_battled()

            # get boolean of surviving pokemon : O(1)
            unit1_survived = unit1.get_hp() > 0
            unit2_survived = unit2.get_hp() > 0

            # prints the battle outcome of each battle (uncomment to use for debugging)
            # self._battle_outcome(unit1_survived, unit2_survived, unit1, unit2)
            # levels up pokemon : O(1)
            self._level_up(unit1_survived, unit2_survived, unit1, unit2)

            # removes dead pokemon : O(1)
            if not unit1_survived:
                t1.pop()
            if not unit2_survived:
                t2.pop()

        # return result of battle : O(1)
        return self._return_results(t1, t2, self.trainer_one_name, self.trainer_two_name)

    def rotating_mode_battle(self) -> str:
        """
        Task 4:
        Battle mode where each pokemon battle for 1 round, and return to team if they survived, until any or all teams loses all their pokemon

        :pre: none, all preconditions checked prior to execution
        :complexity:
            best case and worst case complexity: O(n)
                - most expensive code is the while loop and choose_team() which are both O(n)

        :return: str, "(name of winning team)" or "Draw"
        """
        # setting battle mode to 1 : O(n)
        self.team1.choose_team(1)
        self.team2.choose_team(1)
        # user input for teams

        t1 = self.team1.team_content
        t2 = self.team2.team_content

        # check if teams are empty : O(n)
        while not t1.is_empty() and not t2.is_empty():  # make sure both teams are not empty before battle

            # accessing the current pokemon : O(1)
            unit1 = t1.serve()
            unit2 = t2.serve()

            # calculates the damage of pokemon using speed of each pokemon : O(1)
            self._calculate_damage_with_speed(unit1, unit2)
            # calculates damage taken after the battle, and which pokemon has fainted : O(1)
            self._deduct_hp(unit1, unit2)

            # update if pokemon has battled : O(1)
            unit1.has_battled()
            unit2.has_battled()

            # get boolean of surviving pokemon : O(1)
            unit1_survived = unit1.get_hp() > 0
            unit2_survived = unit2.get_hp() > 0

            # prints the battle outcome of each battle (uncomment to use for debugging)
            # self._battle_outcome(unit1_survived, unit2_survived, unit1, unit2)
            # levels up pokemon : O(1)
            self._level_up(unit1_survived, unit2_survived, unit1, unit2)

            # returns surviving pokemon : O(1)
            if unit1_survived:
                t1.append(unit1)
            if unit2_survived:
                t2.append(unit2)

        return self._return_results(t1, t2, self.trainer_one_name, self.trainer_two_name)

    def optimised_mode_battle(self, criterion_team1: str, criterion_team2: str) -> str:
        """
        Task 5:
        Battle mode where each pokemon battle for 1 round, and return to team if they survived, until any or all teams loses all their pokemon

        :pre: none, all preconditions checked prior to execution
        :complexity:
            best case complexity: O(nlogn), choose_team() is the most expensive code, if teams each have 1 pokemon
            worst case complexity: O(n^2), while loop contains O(n) code, so it is O(n^2)

        :return: str, "(name of winning team)" or "Draw"
        """
        # setting battle mode to 2 : O(nlogn)
        self.team1.choose_team(2, criterion_team1)
        self.team2.choose_team(2, criterion_team2)
        # user input for teams

        t1 = self.team1.team_content
        t2 = self.team2.team_content

        # check if teams are empty : O(n)
        while not t1.is_empty() and not t2.is_empty():  # make sure both teams are not empty before battle

            # check if all pokemon has battled : O(1)/O(n)
            t1_all_battled = self.check_battled(t1)
            t2_all_battled = self.check_battled(t2)

            # accessing the current pokemon : O(1)
            unit1 = t1[len(t1) - 1].value
            unit2 = t2[len(t2) - 1].value

            # Switch to MissingNo if all other pokemon has battled in team1 : O(n)
            if self.team1.has_MissingNo:
                if unit1.get_name() != "MissingNo":
                    if len(t1) > 1 and t1_all_battled:
                        index = self.get_MissingNo_index(t1)
                        unit1 = t1[index].value
                else:
                    if len(t1) > 1 and not t1_all_battled:
                        unit1 = t1[len(t1) - 2].value

            # Switch to MissingNo if all other pokemon has battled in team2 : O(n)
            if self.team2.has_MissingNo:
                if unit2.get_name() != "MissingNo":
                    if len(t2) > 1 and t2_all_battled:
                        index = self.get_MissingNo_index(t2)
                        unit2 = t2[index].value
                else:
                    if len(t2) > 1 and not t2_all_battled:
                        unit2 = t2[len(t2) - 2].value

            unit1.has_battled()
            unit2.has_battled()

            # calculates the damage of pokemon using speed of each pokemon : O(1)
            self._calculate_damage_with_speed(unit1, unit2)
            # calculates damage taken after the battle, and which pokemon has fainted : O(1)
            self._deduct_hp(unit1, unit2)

            # get boolean of surviving pokemon : O(1)
            unit1_survived = unit1.get_hp() > 0
            unit2_survived = unit2.get_hp() > 0

            # prints the battle outcome of each battle (uncomment to use for debugging)
            # self._battle_outcome(unit1_survived, unit2_survived, unit1, unit2)
            # levels up pokemon : O(1)
            self._level_up(unit1_survived, unit2_survived, unit1, unit2)

            # remove dead pokemon : O(n)
            self._update_pokemon_pos(unit1_survived, unit1, self.team1, criterion_team1)
            self._update_pokemon_pos(unit2_survived, unit2, self.team2, criterion_team2)

        return self._return_results(t1, t2, self.trainer_one_name, self.trainer_two_name)

    def _calculate_damage_with_speed(self, unit1: PokemonBase, unit2: PokemonBase) -> int:
        """
        This method takes the 2 current pokemon, unit1 and unit2, that is in battle and calculates the damage received by each of them.
        This method returns a tuple of 3 int values, which denotes:
            int 1 : damage received by unit1
            int 2 : damage received by unit2
            int 3 : speed of pokemon,
                if n=0, both pokemon attacks at the same time,
                if n=1, unit1 attacked first,
                if n=2 unit2 attacked first
        :param unit1: PokemonBase class, pokemon from team1
        :param unit2: PokemonBase class, pokemon from team2

        :return: damage1, damage2, spd3
            damage1: damage received by unit1,
            damage2 : damage received by unit2,
            spd : n in {n:0,1,2}
        """
        damage1 = 0
        damage2 = 0
        spd = 0
        # pokemon 2 attacks first
        if unit1.get_speed() < unit2.get_speed():
            damage1 = unit1.calculate_damage(unit2)
            # pokemon 1 attacks if not dead
            if unit1.get_hp() > 0:
                damage2 = unit2.calculate_damage(unit1)
                spd = 2

        # pokemon 1 attacks first
        elif unit1.get_speed() > unit2.get_speed():
            damage2 = unit2.calculate_damage(unit1)
            # pokemon 2 attacks if not dead
            if unit2.get_hp() > 0:
                damage1 = unit1.calculate_damage(unit2)
                spd = 1

        # if both pokemon have same speed, both attack and defend
        else:
            damage1 = unit2.calculate_damage(unit1)
            damage2 = unit1.calculate_damage(unit2)

        return damage1, damage2, spd

    def _level_up(self, bool1: bool, bool2: bool, unit1: PokemonBase, unit2: PokemonBase) -> None:
        """
        This method is called to level up a pokemon after a battle.
        This method checks if and only if 1 pokemon is alive, and if so, it will level up that respective pokemon

        :param bool1: Boolean for whether unit1 is alive, True if alive, else false
        :param bool2: Boolean for whether unit2 is alive, True if alive, else false
        :param unit1: PokemonBase class, pokemon from team1
        :param unit2: PokemonBase class, pokemon from team2
        :complexity:
            Best Case and Worst case:  O(1) , all lines are only called once
        :return: None

        """
        if bool1 and not bool2:
            unit1.set_level(unit1.get_level() + 1)
        elif bool2 and not bool1:
            unit2.set_level(unit2.get_level() + 1)
        else:
            return None

    def _deduct_hp(self, unit1: PokemonBase, unit2: PokemonBase) -> None:
        """
        This method is called after pokemon from each team, unit1 and unit2 has battled (attacked and defended each other) for 1 round
        This method will take unit1 and unit2 and check if they are still alive, if they are, it will deduct both their hp by 1.

        :param unit1: PokemonBase class, pokemon from team1
        :param unit2: PokemonBase class, pokemon from team2
        :complexity:
            Best Case and Worst case:  O(1) , all lines are only called once
        :return: None
        """

        # check if both pokemon are still alive after the battle
        if unit1.get_hp() > 0 and unit2.get_hp() > 0:
            # if they are both alive, remove 1 hp from each of them
            unit1.hp = (unit1.get_hp() - 1)
            unit2.hp = (unit2.get_hp() - 1)

    def _update_pokemon_pos(self, survived: bool, unit: PokemonBase, team, criterion) -> None:
        """
        This method is only used if battle has a criterion (e.g optimised_battle_mode())
        This method checks if the current pokemon has survived the battle or not.
            If it has, it will update the position of the pokemon in the team
            If it did not, it will delete the pokemon from the team

        NOTE:
        If MissingNo is the last pokemon in the team, this method will use the second-last index to search for the current pokemon
        And update the current pokemon properly

        :param survived: Boolean for whether pokemon is alive, True if alive, else false
        :param unit: PokemonBase class, battling pokemon from team
        :param team: The team the pokemon belongs to
        :param criterion: The criterion used to order the pokemon in the team
        :complexity:
            Best Case and Worst case:  O(n) , delete_at_index() is O(n), because _shuffle_left() is O(n)
        :return: None
        """
        t = team.team_content
        l = len(t)
        del_missing_no = False

        if l > 1 and t[l - 1].value.get_name() != unit.get_name():
            index = l - 2
        else:
            index = l - 1

        if t[index].value.get_name() == "MissingNo":
            del_missing_no = True

        if not survived:
            t.delete_at_index(index)
            if del_missing_no:
                team.has_MissingNo = False

        else:
            new_t = team._give_criterion(t[index].value, criterion)
            if t[index].key != new_t.key:
                t.delete_at_index(index)
                t.add(new_t)

    def _return_results(self, t1, t2, one: str, two: str) -> str:
        """
        This methods team1 and team2, and checks which team has won the battle, then returns their respective name
        If neither team has won, then it will output "Draw"

        :param t1: team1
        :param t2: team2
        :param one: The name of team1
        :param two: The name of team2
        :complexity:
            Best Case and Worst case:  O(1) , all lines are only called once
        :return: str : (Name of the winning team) or "Draw"
        """
        # return results
        draw_string = "Draw"
        results = ""
        if t1.is_empty() and t2.is_empty():
            results = draw_string
        elif t2.is_empty():
            results = one
        else:
            results = two
        return results

    def check_battled(self, team) -> bool:
        """
        This method checks any pokemon in the team hasn't battled, then returns False if found
        If not found, returns True

        :param team: get the team of pokemon that method should check
        :complexity:
            Best case : O(1), if the first pokemon checked has not battled
            Worst Case :  O(n), if all pokemon has battled
        :return: bool : whether all pokemon has battled or not
        """
        for i in range(len(team) - 1, -1, -1):
            unit = team[i].value
            if unit.get_battled() == False:
                return False
        return True

    def get_MissingNo_index(self, team) -> int:
        """
        This method takes a team of pokemon, and returns the index of MissingNo in that team

        :param team: get the team that MissingNo belongs to
        :complexity:
            best case : O(1) MissingNo is first in the team
            worst case : O(n) MissingNo is last in the list
        :return: int : The index of MissingNo

        """
        if len(team) == 1:
            return 1
        else:
            for i in range(len(team)):
                unit = team[i].value
                if unit.get_name() == "MissingNo":
                    return i

    def _battle_outcome(self, bool1, bool2, unit1, unit2) -> None:
        """
        Print function, only used for debugging
        :param bool1 (bool): Boolean for whether unit1 is alive, True if alive, else false
        :param bool2 (bool): Boolean for whether unit2 is alive, True if alive, else false
        :param unit1 (PokemonBase): PokemonBase class, pokemon from team1
        :param unit2 (PokemonBase): PokemonBase class, pokemon from team2
        :complexity:
            Best and Worst Case : O(1) , all lines are only called once, no concatenation involved
        :return: None
        """
        printstate = ""

        if bool1 and not bool2:
            printstate = "Team 1’s {} faints Team 2’s {}".format(unit1.get_name(), unit2.get_name())
        elif bool2 and not bool1:
            printstate = "Team 1’s {} is fainted by Team 2’s {}".format(unit1.get_name(), unit2.get_name())
        elif not bool1 and not bool2:
            printstate = "Both Team 1’s {} and Team 2’s {} fainted".format(unit1.get_name(), unit2.get_name())
        else:
            printstate = "Both alive"

        print(printstate)
        print("    {}\n    {}".format(str(unit1), str(unit2)))

    def _battle_outcome_2(self, bool1: bool, bool2: bool, spd: int, unit1:PokemonBase, unit2:PokemonBase, damage1:int, damage2:int) -> None:
        """
        Print function, only used for debugging
        :param bool1 (bool): Boolean for whether unit1 is alive, True if alive, else false
        :param bool2 (bool): Boolean for whether unit2 is alive, True if alive, else false
        :param spd (int): which pokemon has attacked first
        :param unit1 (PokemonBase): PokemonBase class, pokemon from team1
        :param unit2 (PokemonBase): PokemonBase class, pokemon from team2
        :param damage1 (int): the damage received by unit1
        :param damage2 (int): the damage received by unit2
        :complexity:
            Best and Worst Case : O(1) , all lines are only called once, no concatenation involved
        :return: None

        """
        printstate = ""

        if bool1 and not bool2:
            printstate = "Team 1’s {} faints Team 2’s {}".format(unit1.get_name(), unit2.get_name())
        elif bool2 and not bool1:
            printstate = "Team 1’s {} is fainted by Team 2’s {}".format(unit1.get_name(), unit2.get_name())

        elif damage1 == damage2:
            printstate = "Team 1’s {} attacks Team 2’s {}, and they both lose {} HP".format(unit1.get_name(),
                                                                                            unit2.get_name(), damage1)
        elif spd == 1 or spd == 0:
            printstate = "Team 1’s {} attacks Team 2’s {}, loses {} HP while Team 2’s {} loses {} HP".format(
                unit1.get_name(), unit2.get_name(), damage1, unit2.get_name(), damage2)
        elif spd == 2:
            printstate = "Team 2’s {} attacks Team 1’s {}, loses {} HP while Team 2’s {} loses {} HP".format(
                unit2.get_name(), unit1.get_name(), damage2, unit1.get_name(), damage1)

        else:
            printstate = "exception"

        print(printstate)
        print("    {}\n    {}".format(str(unit1), str(unit2)))
