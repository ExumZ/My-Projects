""" Implementation of Potion class

Defines Potion class. Code contains 2 instance methods and 3 class methods.
instance methods:
    - __init__() : constructor for Potion class
    - __str__() : string methods returning all instance variables.

class methods:
    - create_empty() : creates an empty potion of class Potion()
    - good_hash() : generates a good hash key
    - bad_hash() : generates a bad hash key
"""

__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

class Potion:

    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        """
        Constructor of the class Potion. Does not return anything.

        :param potion_type: the potion type of the potion
        :param name: the name of the potion
        :param buy_price: the price of the potion
        :param quantity: the amount of stock the potion has in Litres
        :return: None
        """
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        This class method creates a potion of provided data and sets the quantity of the potion to 0.

        :param potion_type: the potion type of the potion
        :param name: the name of the potion
        :param buy_price: the price of the potion
        :return: Return a potion with 0 quantity
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        The function generates a hash key,
        a hash key is determined by a (prime*n*value)%prime operation.
        As such, occurence of repeated keys are very limited, so clustering does not happen very frequently.
        Since there is only 2 divisors, 1 or prime number used.
        Empty spaces are very limited.

        Here we choose 53 as the prime number because we assume that the potion would have a potion_type of
        any character(26) including capital letters(26)
        26+26 = 52 and we take the next biggest prime 53

        Example:
        [22,23,5,18,4,3,24,17,14,7]
        very sparce and separated, no repeated keys

        :complexity: O(n) where n is the length of the potion name

        :param potion_name (str): the name of the potion
        :param tablesize (int): the size of the hash table
        :return (int): the key generated
        """
        prime = 53
        value = 0
        #Horner's method of finding hash key
        for char in potion_name:
            value = (ord(char) + prime * value) % tablesize
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        The function generates a hash key using a number n, that is not a mod of a prime number.
        This means that when adding items into the hash table, elements can
        clump together (where spaces with said key is full, so added to next empty slot instead.)

        Additionally, since n is divisible by certain numbers, spaces that are not divisors of n will be largely left empty.

        Example:
        [14,14,16,16,18,10,14,14,8,10]
        all divisible by 2, many repeated keys.

        :complexity: O(1)

        :param potion_name (str): the name of the potion
        :param tablesize (int): the size of the hash table
        :return (int): the key generated
        """
        return ord(potion_name[0]) % (tablesize//2)*2

    def __str__(self):
        """
        A string method returns all instance variables assigned.
        :return: a string containing all instance variables
        """
        return "[Type = {}, Name = {}, Price = ${}, Quantity = {}Litres]".format(self.potion_type, self.name, self.buy_price, self.quantity)

if __name__ == '__main__':
    strings = ['a', 'aardgdvark', 'bilious', 'bandsaw', 'carnivorous', 'sdfsag',
               'adgadfv', 'ufymngsdm', 'rebse', 'ibveveb']
    hash_fun1 = Potion.good_hash
    for s in strings:
        print(f'{s} => {hash_fun1(s, 25)}')

    hash_fun2 = Potion.bad_hash
    for s in strings:
        print(f'{s} => {hash_fun2(s, 20)}')
