""" Implementation of the Charmander, Squirtle, Bulbasaur and MissingNo classes

Defines the classes Charmader, Squirtle and Bulbasaur as child classes of PokemonBase.
Defines the class MissingNo as the child class of GlitchMon.
Abstract methods are implemented here.
"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

from pokemon_base import PokemonBase
from glitchmon import GlitchMon
import random

class Charmander(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 7, "Fire")
        self.name = "Charmander"
        self.battled=False

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_name(self) -> str:
        return self.name

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_attack(self) -> int:
        return 6 + self.level

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_defense(self) -> int:
        return 4

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_speed(self) -> int:
        return 7 + self.level

    """
    type_effectiveness() method is O(n) for this class
    Best Case Complexity: O(n)
    Worst Case Complexity: O(n)
    """
    def calculate_damage(self, opponent) -> int:

        damage = self.type_effectiveness(self.poke_type, opponent.poke_type, opponent.get_attack())
        # Calculates opponent damage based on their attack and your defense
        if damage > self.get_defense():
            pass
        else:
            damage //= 2
        self.hp -= damage

        return damage

    """
    Both Best and Worst Complexity: O(n^2) due to string concatenation
    """
    def __str__(self):
        return self.name + "'s " + PokemonBase.__str__(self)

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def has_battled(self):
        self.battled=True

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_battled(self)-> bool:
        return self.battled

class Bulbasaur(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 9, "Grass")
        self.name = "Bulbasaur"
        self.battled = False

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_name(self) -> str:
        return self.name

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_attack(self) -> int:
        return 5

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_defense(self) -> int:
        return 5

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_speed(self) -> int:
        return  7 + (self.level // 2)

    """
    type_effectiveness() method is O(n) for this class
    Best Case Complexity: O(n)
    Worst Case Complexity: O(n)
    """
    def calculate_damage(self, opponent) -> int:

        damage = self.type_effectiveness(self.poke_type, opponent.poke_type, opponent.get_attack())
        # Calculates opponent damage based on their attack and your defense
        if damage > (self.get_defense() + 5):
            pass
        else:
            damage //= 2

        self.hp -= damage

        return damage

    """
    Both Best and Worst Case Complexity: O(n^2) due to string concatenation
    """
    def __str__(self):
        return self.name + "'s " + PokemonBase.__str__(self)

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def has_battled(self):
        self.battled=True

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_battled(self)-> bool:
        return self.battled


class Squirtle(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self, 8, "Water")
        self.name = "Squirtle"
        self.battled = False

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_name(self) -> str:
        return self.name

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_attack(self) -> int:
        return 4 + (self.level // 2)

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_defense(self) -> int:
        return 6 + self.level

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_speed(self) -> int:
        return 7

    """
    type_effectiveness() method is O(n) for this class
    Best Case Complexity: O(n)
    Worst Case Complexity: O(n)
    """
    def calculate_damage(self, opponent) -> int:

        damage = self.type_effectiveness(self.poke_type, opponent.poke_type, opponent.get_attack())
        # Calculates opponent damage based on their attack and your defense
        if damage > (self.get_defense() * 2):
            pass
        else:
            damage //= 2

        self.hp -= damage

        return damage

    """
    Both Best and Worst Case Complexity: O(n^2) due to string concatenation
    """
    def __str__(self):
        return self.name + "'s " + PokemonBase.__str__(self)

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def has_battled(self):
        self.battled=True

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_battled(self)-> bool:
        return self.battled

class MissingNo(GlitchMon):

    def __init__(self):
        GlitchMon.__init__(self)
        self.name="MissingNo"
        self.battled=True

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_name(self) -> str:
        return self.name

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def has_battled(self):
        self.battled=True

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_battled(self)-> bool:
        return self.battled

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_attack(self) -> int:
        return (7+5+4)//3 +self.level-1

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_defense(self) -> int:
        return ((4+5+7)//3 +self.level-1)

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_speed(self) -> int:
        return (8+7+7)//3 +self.level-1

    """
    
    Both Best and Worst Case Complexity: O(1)
    Pre: opponent is an instance of PokemonBase
    The method will calculate damage inflicted on the pokemon
    """
    def calculate_damage(self, opponent) -> int:
        if not isinstance(opponent,PokemonBase):
            raise TypeError("Expected a pokemon")
        random_number=random.randint(0,2)
        damage=opponent.get_attack()
        if random_number==0:
            if damage > (self.get_defense()):
                pass
            else:
                damage //= 2
        elif random_number==1 :
            if damage > (self.get_defense() + 5):
                pass
            else:
                damage //= 2
        elif random_number==2:
            if damage > (self.get_defense() * 2):
                pass
            else:
                damage //= 2

        self.hp -= damage
        if random.random() <= 0.25:
            self.superpower()

        return damage

    """
    Both Best and Worst Case Complexity: O(n^2) due to string concatenation
    """
    def __str__(self):
        return self.name + "'s " + GlitchMon.__str__(self)
