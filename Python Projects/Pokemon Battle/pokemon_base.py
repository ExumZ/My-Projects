""" Implementation of the PokemonBase and GlitchMon class

Defines the PokemonBase and GlitchMon classes. GlitchMon is a child class of PokemonBase class
The PokemonBase class and GlitchMon class are base classes of the Pokemon that will be implemented in pokemon.py
These classes contain one or several abstract methods will be implemented in their respective child classes

"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'


from abc import ABC, abstractmethod



class PokemonBase(ABC):
    # Constructor
    def __init__(self, hp: int, poke_type: str):
        self.hp = hp
        self.poke_type = poke_type
        self.level = 1
        
    """
    Pre: newHP must be an integer that's greater than or equal to 0
    Raises TypeError if input is not an integer
    Raises ValueError if input is a negative integer
    Complexity: O(1)
    
    """
    def set_hp(self, newHP) -> int:
        if not isinstance(newHP, int):
            raise TypeError("Expect an integer")
        elif newHP < 0:
            raise ValueError("HP needs to be a positive integer")
        self.hp = newHP

    """
    Pre: newLevel must be an integer that's greater than 0
    Raises TypeError if input is not an integer
    Raises ValueError if input is not a positive integer
    Complexity: O(1)
    
    """
    def set_level(self, newLevel) -> int:
        if not isinstance(newLevel, int):
            raise TypeError("Expect an integer")
        elif newLevel <= 0:
            raise ValueError("Level needs to be greater than 0")
        self.level = newLevel

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_hp(self) -> int:
        return self.hp

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_level(self) -> int:
        return self.level

    """
    Both Best and Worst Case Complexity: O(1)
    """
    def get_pokeType(self) -> str:
        return self.poke_type

    """
    Both Best and Worst Case Complexity: O(n^2) due to string concatenation
    """
    def __str__(self):
        return  "HP = " + str(self.hp) + " and level = " + str(self.level)

    @abstractmethod
    def get_name(self) -> int:
        pass

    @abstractmethod
    def get_attack(self) -> int:
        pass

    @abstractmethod
    def get_defense(self) -> int:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def calculate_damage(self, opponent):
        pass

    def type_effectiveness(self, typeself:str, typeopponent:str, damage:int) -> int:
        """
        Takes the pokemon types of opponent and self to determine type effectiveness.
        then multiplies the opponents damage based on type effectiveness of the opponent's pokemon
        returns an integer value of the damage multiplied by the type effectiveness multiplier

        Best-case Complexity: O(1) if the code runs the first if statement
        Worst-case Complexity: O(n) where n is the total length of the output if code runs the else
        """
        res = damage

        if typeself=="MissingNo" or typeopponent=="MissingNo":
            return res
        else:
            pokeType = [typeself, typeopponent]
            types = "".join(pokeType)
            if types in {"FireGrass", "WaterFire", "GrassWater"}:
                res //= 2
            elif types in {"FireWater", "WaterGrass", "GrassFire"}:
                res *= 2

        return res


