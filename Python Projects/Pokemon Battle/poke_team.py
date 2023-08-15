""" Implementation of the PokeTeam class

Defines the PokeTeam class and implements the choose_team() and set_battle_mode() functions
Contains 2 local methods, _assign_team() and _give_criterion() which are used in implemented function
as well as called after instantiation of this class.

The PokeTeam class should contain the team name (self.team_name) and battle mode (self.battle_mode)

The function choose_team() should prompt user to input a team of pokemon described in the assignment task.
The format of input is N N N N, where N is any number ranging to 0-6, and the sum of all N=6

The function set_battle_mode() lets user to set a battle mode for the PokeTeam object. Preconditions are described below

"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

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


class PokeTeam:
    LIMIT: int = 6

    def __init__(self,team_name:str,input_battle_mode: int=0):
        self.team_name=team_name
        self.set_battle_mode(input_battle_mode)
        self.num_of_pokemon = 0
        self.has_MissingNo = False


    def __str__(self):
        """
            Both Best and Worst Complexity: O(n^2) due to string concatenation
            """
        #depends on ADT
        ret_string=""
        if self.battle_mode==0 : #stack
            for i in range(len(self.team_content)):
                ret_string+=str(self.team_content.access(i)) + ", "

        elif self.battle_mode==1: #circular queue
            for i in range(len(self.team_content)):
                x = self.team_content.serve()
                ret_string+=str(x) + ", "
                self.team_content.append(x)
        else:
            for i in range(len(self.team_content)-1, -1, -1):
                x = self.team_content[i].value
                ret_string+=str(x) + ", "

        return ret_string[0:-2]


    def choose_team(self,battle_mode:int = 0, criterion: str =None) -> None:
        """
            Pre: battle_mode must be 0,1,2 or None, which will cause battle_mode to have default value=0,criterion is a string and if no criterion it defaults to None
            Raises value error if input is not a number
            The function will ask for a team input, and will keep asking until the input is correct
            Best case complexity= O(n) when battle_mode = 0 or 1 
            Worst case complexity= O(nlogn) when battle_mode =2 due to assign_team()

            """
        if self.battle_mode != battle_mode:
            self.set_battle_mode(battle_mode)

        valid = False
        input_contents=[]
        while not valid:
            user_input=input("Howdy Trainer! Choose your team as C B S\nwhere C is the number of Charmanders\n"
                             "      B is the number of Bulbasaurs\n      S is the number of Squirtles\n")
            input_contents=user_input.split(" ")
            is_number=True
            for i in range(0, len(input_contents)): # check if is a number entered
                try:
                    input_contents[i] = int(input_contents[i])
                except ValueError:
                    print("Input must be a number")
                    is_number = False
            if is_number: #if the input string is a number string, then count the sum of these numbers
                for i in range(0, len(input_contents)):
                    input_contents[i] = int(input_contents[i])
                sum = 0
                for i in range(len(input_contents)):
                    sum += input_contents[i]
                if sum > 0 and sum <= 6 : # if the sum of these number is less than 6 but greater than 0, the entered input is valid,if not it will ask for input again
                    if len(input_contents)==3 :
                        valid =True
                        self.num_of_pokemon=sum
                        self.has_MissingNo=False
                    elif len(input_contents)==4:
                        if (input_contents[3]==1):
                            valid = True
                            self.num_of_pokemon = sum
                            self.has_MissingNo=True
                        elif (input_contents[3]==0):
                            valid = True
                            self.num_of_pokemon = sum
                            self.has_MissingNo=False

                    else:
                        print("The input has only one Pokemon type specified!")
                elif sum > 6:
                    print("Error! There is more than 6 Pokemons! The maximum is 6 Pokemons")
                else:
                    print("Error! There must be at least 1 Pokemons!")

        self._assign_team(input_contents[0],input_contents[1],input_contents[2], criterion)



    def set_battle_mode(self, battle_mode: int=0) -> None:
        """
            :pre: battle_mode must be any value of {0,1,2}
            :raises:
                TypeError if battle_mode is not an integer
                ValueError if battle_mode is outside of {0,1,2}
            :complexity: O(1) where all lines is only passed once
            :return: None
            """

        if not isinstance(battle_mode, int):
            raise TypeError ("Input must be an integer!")
        elif battle_mode not in {0,1,2}: # ensure battle_mode is only 0,1 or 2
            raise ValueError("Input can only be an integer of 0,1 or 2")
        else:
            self.battle_mode=battle_mode



    def _assign_team(self,charm:int,bulb:int,squir:int, criterion:str=None)->None:
        # depends on ADT which depends on battle_mode
        """
        The function will create the team with the suitable ADT based on the battle mode entered
        :param: charm, bulb, squir
        Pre: Sum of charm,bulb and squir is more than 0 and less than or equal to 6

        Best complexity= O(n) when battle_mode =0 or 1
        Worst complexity=O(nlogn)  when battle mode=2, add() has time complexity of O(logn) due to _index_to_add() which has complexity of O(logn).

        Pre condition is enforced in choose_team() before being called
        :return: None
        """
        if self.battle_mode==0:
            self.team_content=ArrayStack(PokeTeam.LIMIT)
            if self.has_MissingNo:
                self.team_content.push(MissingNo())
            for i in range(squir):
                self.team_content.push(Squirtle())
            for i in range(bulb):
                self.team_content.push(Bulbasaur())
            for i in range(charm):
                self.team_content.push(Charmander())

        
        elif self.battle_mode==1:
            self.team_content=CircularQueue(PokeTeam.LIMIT)
            for i in range(charm):
                self.team_content.append(Charmander())
            for i in range(bulb):
                self.team_content.append(Bulbasaur())
            for i in range(squir):
                self.team_content.append(Squirtle())
            if self.has_MissingNo:
                self.team_content.append(MissingNo())



        else:
            self.team_content=ArraySortedList(PokeTeam.LIMIT)
            if self.has_MissingNo:
                self.team_content.add(self._give_criterion(MissingNo(),criterion))
            for i in range(charm):
                self.team_content.add(self._give_criterion(Charmander(),criterion))
            for i in range(bulb):
                self.team_content.add(self._give_criterion(Bulbasaur(),criterion))
            for i in range(squir):
                self.team_content.add(self._give_criterion(Squirtle(),criterion))


    def _give_criterion(self, pokemon:PokemonBase, criterion:str=None) -> ListItem:
        """
            The function will create a ListItem from the given pokemon and criterion
            :param: pokemon,criterion
            Pre: pokemon must be a instance of one of three pokemon ( Charmander, Bulbasaur and Squirtle)

            Best and worst complexity= O(1)

            :return: None
        """
        if criterion == "hp":
            do = ListItem(pokemon, pokemon.get_hp())
        elif criterion == "spd":
            do = ListItem(pokemon, pokemon.get_speed())
        elif criterion == "def":
            do = ListItem(pokemon, pokemon.get_defense())
        elif criterion == "atk":
            do = ListItem(pokemon, pokemon.get_attack())
        elif criterion == "lvl":
            do = ListItem(pokemon, pokemon.get_level())
        else:
            do = ListItem(pokemon, 0)

        return do
