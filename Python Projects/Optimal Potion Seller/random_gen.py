"""Implementation of RandomGen Class

Defines the RandomGen class. Code contains 3 instance methods and 1 local function
instance methods in RandomGen():
    - __init__() : class constructor, assigns a seed to lcg()
    - self.randint() : generates a random number using lcg(seed)
    - self.__count_ones() : a helper function used in randint()

local methods:
    - lcg() : this function is a lineor congruential generator, which has been provided by the original file.
"""

__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

from typing import Generator

def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed

class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        """
        This constructor takes a seed (seed=0 if none assigned) and initialises an
        instance variable containing a generator created using lcg() function.
        :param seed: integer value of any kind
        """
        self.random_num = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        This method takes any integer k and generates a random number in the range of 1 to k, inclusive.

        This method does this by generating 5 numbers using the generator in self.random_num, and assign them into a list.
        Then takes the 16 most significant bits of each number (removing 16 least significant bits).
        Then creates a new number from the count of all 1s of each column (if total 1s in that column >=3, then bit=1, else bit=0)

        :param k (int): any integer value
        :return (int): a random number between 1 to k inclusive
        """
        numbers = []

        # append random numbers generated into numbers list
        for num in self.random_num:
            numbers.append(num)
            if len(numbers) == 5:
                break

        # bitwise shift to the right to drop 16 sig bits
        for i in range(5):
            numbers[i] = numbers[i] >> 16

        temp = 0
        # current_bit = 2^0
        current_bit = 1
        # adds current bit if needed to temp number then increases exponential regardless aka moving on to the next bit
        for i in range(16): # 16bits
            if self.__count_ones(numbers) >= 3:
                temp += current_bit
            #multiply by 2 to move to next bit
            current_bit *= 2

        # forming the new number
        new_number = (temp % k) + 1
        return new_number

    # decimal to binary conversion and count the ones
    def __count_ones(self, numbers: list) -> int:
        """
        This helper function iterates through the first 5 numbers in a list, for each number divides by 2 and counts all remainders that are 1.
        Then modifies the first 5 numbers in the lists to its floor division of 2.

        :param numbers (list): list containing all numbers to count
        :return (int): total number of 1s after iteration
        """
        count = 0
        for i in range(5):
            # for each number, divide by 2, check if remainder is 1 and count it
            if numbers[i] % 2 == 1:
                count += 1

            # continue floor dividing the numbers
            numbers[i] = numbers[i] // 2

        return count


if __name__ == "__main__":
    Random_gen = lcg(pow(2, 32), 134775813, 1, 0)
