""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
_linear_probe() is updated to record conflict_count,probe_max,probe_total

"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner, modified by (Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn)'
__docformat__ = 'reStructuredText'
__modified__ = '29/05/2022'
__since__ = '14/05/2020, 21/05/2020'

from referential_array import ArrayR
from typing import TypeVar, Generic
from potion import Potion
from primes import largest_prime
T = TypeVar('T')


class LinearProbePotionTable(Generic[T]):
    """
    Linear Probe Potion Table

    This potion table does not support deletion.

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        table_size: current size of the hash table
    """

    #__init__ implementation
    def __init__(self, max_potions: int, good_hash: bool, tablesize_override: int=-1) -> None:
        # Statistic setting
        """
        Initialise a Linear Probe Potion Table.

        :complexity : O(n) where n is length of table
        :param max_potions (int): the max amount of potions
        :param good_hash (bool): whether to use good hash or not
        :param tablesize_override: an override to change table size
        """

        self.conflict_count = 0
        self.probe_max = 0
        self.probe_total = 0
        self.good_hash = good_hash

        #if override exists, use that for making table, else makes a table with (max_potion*2~=largest prime number)
        if tablesize_override == -1:
            self.initalise_with_tablesize(largest_prime(max_potions*2))
        else:
            self.initalise_with_tablesize(tablesize_override)

    #hash implementation
    def hash(self, potion_name: str) -> int:
        """
        Takes a potion, potion_name, and creates a hash key using potion_name
        :complexity: O(nlogn) due to good_hash or bad_hash
        :param potion_name (str): the potion
        :return: a hash value
        """

        if self.good_hash:
            return Potion.good_hash(potion_name,len(self.table))
        else :
            return Potion.bad_hash(potion_name,len(self.table))

    #statistics implementation
    def statistics(self) -> tuple:
        """
        Provides statistics. Returns conflict_count,probe_total,probed_max
        :complexity: O(1)
        :return: a tuple containing conflict_count, probe_total and probe_max
        """
        return (self.conflict_count,self.probe_total,self.probe_max)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self.count

    #_linear_probe modified
    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing
        Record the number of probes for this key and add it to total probe distance
        :complexity : O(nlogn), from hash(key)
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)

        probed=False # whether or not this key has been probed
        num_of_probes = 0 # record the number of probes for this key

        for _ in range(len(self.table)):  # start traversing

            if self.table[position] is None:  # found empty slot
                self.probe_total += num_of_probes # add the number of probes to total distance of probes
                if num_of_probes > self.probe_max: # if current number of probes is more than maximum, set next maximum
                    self.probe_max = num_of_probes
                is_insert = True # set is_insert to true here

                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                if not probed: # if first time probing, then increase conflict count by 1
                    self.conflict_count += 1
                    probed=True

                position = (position + 1) % len(self.table)
                num_of_probes += 1

        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        :see: #self.__getitem__(self, key: str)
        :complexity: O(1)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist
        :complexity: O(1)
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set an (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__contains__(key: str)
        :complexity: O(nlog(n))
        """
        if len(self) == len(self.table) and key not in self:
            raise ValueError("Cannot insert into a full table.")
        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)

    def initalise_with_tablesize(self, tablesize: int) -> None:
        """
        Initialise a new array, with table size given by tablesize.
        :complexity: O(n), where n is len(tablesize)
        """
        self.count = 0
        self.table = ArrayR(tablesize)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)
        :complexity: O(nlog(n)), from __setitem__(key,data)
        """
        self.__setitem__(key, data)

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

# Statistics Test
if __name__ == '__main__':

    string1 = ['a', 'aardgdvark', 'bilious', 'bandsaw', 'carnivorous', 'sdfsag',
               'adgadfv', 'ufymngsdm', 'rebse', 'ibveveb']

    string2 = ['abcdef', 'athens', 'apple', 'beach', 'billiards', 'bunny', 'ball', 'carrot',
               'car', 'donkey', 'dinner', 'bread', 'custard', 'death', 'dimples', 'elephant']

    string3 = ['afsagdr', 'ebay', 'height', 'friend', 'csgo', 'vase', 'zebra', 'open', 'baby',
               'name', 'made', 'inn', 'java', 'python', 'umbrella', 'kale', 'diva', 'good']

    print("Example 1: ")

    # Good Hash
    p1 = LinearProbePotionTable(20, True)

    for s in string1:
        print(f'{s} => {Potion.good_hash(s, len(p1.table))}')
        p1.insert(s, 5) # 5 is just place holder for data
    stats1 = p1.statistics()
    print(f'Statistics for Good Hash => {stats1}\n')

    # Bad Hash
    p2 = LinearProbePotionTable(20, False)

    for s in string1:
        print(f'{s} => {Potion.bad_hash(s, len(p2.table))}')
        p2.insert(s, 5)
    stats2 = p2.statistics()
    print(f'Statistics for Bad Hash => {stats2}\n')
    print('----------------------------------------------------------------------\n')

    print("Example 2: ")

    # Good Hash
    p1 = LinearProbePotionTable(20, True)

    for s in string2:
        print(f'{s} => {Potion.good_hash(s, len(p1.table))}')
        p1.insert(s, 5) # 5 is just place holder for data
    stats1 = p1.statistics()
    print(f'Statistics for Good Hash => {stats1}\n')

    # Bad Hash
    p2 = LinearProbePotionTable(20, False)

    for s in string2:
        print(f'{s} => {Potion.bad_hash(s, len(p2.table))}')
        p2.insert(s, 5)
    stats2 = p2.statistics()
    print(f'Statistics for Bad Hash => {stats2}\n')
    print('----------------------------------------------------------------------\n')

    print("Example 3: ")

    # Good Hash
    p1 = LinearProbePotionTable(20, True)

    for s in string3:
        print(f'{s} => {Potion.good_hash(s, len(p1.table))}')
        p1.insert(s, 5) # 5 is just place holder for data
    stats1 = p1.statistics()
    print(f'Statistics for Good Hash => {stats1}\n')

    # Bad Hash
    p2 = LinearProbePotionTable(20, False)

    for s in string3:
        print(f'{s} => {Potion.bad_hash(s, len(p2.table))}')
        p2.insert(s, 5)
    stats2 = p2.statistics()
    print(f'Statistics for Bad Hash => {stats2}\n')
    print('----------------------------------------------------------------------\n')

