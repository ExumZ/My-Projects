""" Implementation of the  GlitchMon class

Defines the  GlitchMon class. GlitchMon is a child class of PokemonBase class
The GlitchMon class are base classes of the Pokemon that will be implemented in pokemon.py
The class contain one or several abstract methods inherited will be implemented in their respective child classes

"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

from pokemon_base import PokemonBase
import random
class GlitchMon(PokemonBase):

    def __init__(self):
        PokemonBase.__init__(self,(7+9+8)//3,"None")

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def increase_hp(self):
        self.hp=self.hp+1

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def increase_lvl(self):
        self.level=self.level+1
        self.hp = self.hp + 1

    """
    Both Best and Worst Case Complexity: O(1)
    This function has a random chance to choose increase hp,increase level or both
    """
    def superpower(self):
        random_number=random.randint(0,2)
        if random_number==0:
            self.increase_lvl()
        elif random_number==1:
            self.increase_hp()
        elif random_number==2:
            self.increase_hp()
            self.increase_lvl()

    """
    Both Best and Worst Case Complexity: O(n^2) due to string concatenation in the __str__ method
    """
    def __str__(self):
        return  PokemonBase.__str__(self)

