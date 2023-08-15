from __future__ import annotations
# ^ In case you aren't on Python 3.10

""" Implementation of Game class

Defines Game class. Code contains 5 instance methods.
instance methods in Class():
    - __init__() : contructor, assigns seed to the RandomGen() class imported from random_gen.py()
    - self.set_total_potion_data() : stores potion data into the Game() object
    - self.add_potions_to_inventory() : updates quantities of potions in Game() object
    - self.choose_potions_for_vendors() : chooses n number of potions for vendors
    - self.solve_game() : takes a list of starting money the player has, then calculates the most profit earned by selling to adventurers.
    
:ADTs used:
    -> LinearProbePotionTable() => self.inventory, self.adventurer
        -   This ADT is used as it enables O(1) complexity when searching for potion data of any potion. 
            All potions have unique names, so a hash table is optimal for storing data.
    -> AVLTree() => self.inv_search(), price_range, weights
        -   This ADT is used for searching values if searches must be made with largest to smallest value.
            This enables searches to be log(n) complexity.
    -> LinkedStack() => temp
        -   This ADT is used for temporarily storing potion data. Since operations are O(1) 
            when pop() and push() are used, it enables for more efficient data management in choose_potions_for_vendors() function

"""
__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'


from typing import Tuple, List, Any
from random_gen import RandomGen
from linked_stack import LinkedStack
from potion import Potion
from hash_table import LinearProbePotionTable
from avl import AVLTree

class Game:

    def __init__(self, seed=0) -> None:
        """
        This constructor takes the seed and creates a RandomGen() class object using the seed, assigns it to self.rand.
        :param seed: any number
        :return: None
        """
        self.rand = RandomGen(seed=seed)

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Takes a list, potion_data and creates a hash table containing elements of Potion class. This function does not return anything.

        :ADTs used:
            self.inventory
                -> LinearProbePotionTable(),    Contains all potion data in the form of a hash table.
                                                Since all potions are stored and never deleted, a static hash table
                                                is optimal to allows O(1) operations when searching for data regarding each
                                                potion, making most operations function more efficiently.

            self.inv_search() -> AVLTree(), initialised here but to be used in choose_potions_for_vendor(),
                                            description of choice written in there.

        self.inv_search() is initialised here as a search tree would not be needed if no potions are added into the class.

        :param potion_data (list):  a list containing tuples of 3 (potion_type, potion_name, buy_price) that is data used
                                    to create each potion in self.inventory, and self.vendors.
        :return: None
        """
        self.inventory = LinearProbePotionTable(len(potion_data), True)
        self.inv_search = AVLTree()

        #Goes through the potion_data and assigns an empty potion for each list created. :complexity: O(n)/O(nlogn)
        for i in potion_data:
            new_type = i[0] #gets the potion_type
            new_price = i[2] #gets the buy_price

            #sets potion in vendor inventory for all potions, and set quantity to 0
            new_potion = Potion.create_empty(new_type,i[1],new_price)
            self.inventory[new_type] = new_potion

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Takes a list containing tuples of 2 (potion_type, quantity) and updates the quantity of all stored potions in self.inventory.
        This function does not return anything.

        :complexity: O(C X log(N))
                    C -> the length of potion_name_amount_pairs
                    N -> the length of the list of tuples
        Complexity Explanation:
            - O(C X log(N)) :   for each item(C), we add item into self.inv_search (log(N)). This is the most expensive part of the code.

        :param (list[tuple]):   a list of tuples containing (potion_type:str and quantity:float)
                                potion_type is the name of the potion.
                                quantity is the amount of stock(in Litres) the potion will have.
        :return: None
        """
        #:complexity: O(C)
        for i in potion_name_amount_pairs:
            cur_item = self.inventory[i[0]]
            cur_item.quantity = i[1] #O(1)
            #:complexity: log(N)
            self.inv_search[cur_item.buy_price] = i[0]

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Takes any integer, num_vendors=n and creates n number of vendors.
        For each vendor, randomly generates a number, k in range of total potions(inclusive) in stock, then chooses
        the kth most expensive potion, and assigns it to the respective vendor.

        Each potion is removed if the potion has been chosen for a vendor.
        All removed potions are added back into the search tree after operation.

        :complexity: O(C X log(N))
                    C -> the length of num_vendors
                    N -> the length of self.inv_search

        Complexity Explanation:
            - O(C X log(N)) :   for each item(C), we search using kth_largest (log(N)). This is the most expensive part of the code.

        :ADTs used:
            temp -> LinkedStack(),  used to temporarily store potions already added to the vendors, as push and pop are O(1) operations.
                                    Potions are popped off when returning them back into the search tree.

            self.inv_search -> AVLTree(),   the tree used to search nth most expensive potion in the inventory. This is because the search tree has
                                            log(n) :complexity: when searching for nth largest item.

        :pre: num_vendors must be any number in range of total potions in stock.
        :param (int): any int value that is less than

        :return (list): returns list containing all vendors that chose potions, by the order in which potions were distributed.
        """
        #precondition :complexity: O(1)
        if num_vendors > len(self.inv_search) or num_vendors<=0:
            raise ValueError("num_vendor must be any number 1-{} inclusive".format((len(self.inv_search))))

        res = []
        temp = LinkedStack()

        #:complexity: O(C x log(N))
        for i in range(num_vendors):
            random = self.rand.randint(num_vendors-i)
            #:complexity: O(log(N))
            x = self.inv_search.kth_largest(random)

            #:complexity: O(1)
            temp.push((x.key, x.item))

            res.append((x.item, x.key))
            del self.inv_search[x.key]

        # adds items back into the search tree self.inv_search
        #:complexity: O(C x log(N))
        for i in range(num_vendors):
            x = temp.pop()
            self.inv_search[x[0]] = x[1]

        return res

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[float]) -> list[float]:
        """
        This function takes 2 lists, potion_valuations and starting_money, then calculates the total amount of profit that can be made
        buying potions from vendors, then selling to adventurers(potion_valuations). Returns a list containing all profits made in order
        of starting money provided.

        Players must buy in the order of (cheapest_price, most profit) to (most_expensive_price, least_profit).
        2 important local AVLTree() ADTs are used to determine this buying order of potions.

        After potions are organised in a buy_list, for each money in starting_money, the function will buy all potions
        based on this buy_list in ascending order(0-end_of_list),
        buying will end abruptly should the money be insufficient.

        :complexity: O(N x log(N) + M x N)
            N -> length of potion_valuations
            M -> length of starting_money

        Complexity Explanation:
            - O(N X log(N)) :   For each item in [potion_valuations](N), Add the item into [price_range] (log(N)).
                                Then for each item in [potion_valuations](N), we search (least to most) expensive item and add into [weights] (log(N))
                                The complexity is due to kth_largest() function which is log(n)
                                These 2 are separate iterations, constants are ignored.
                                As they are the most expensive code for the first part of the complexity, the complexity is as stated.
                                a [buy_list] is generated at the end of this process, which is (N)

            - O(M X N) :    for each item in [starting_money](M), we derive the total profit from [buy_list](N)

        :param potion_valuations:   a list containing tuples of 2 (potion_type, sell_price)
                                    which is the amount adventurers would pay to buy the potions
        :param starting_money:  a list containing amount of starting money.

        :ADTs used:
            self.adventurer
                -> LinearProbePotionTable(),    This is a mirrored hash_table containing all potions that adventurers would buy,
                                                derived from potion_valuations. This enables search for each sales amount with O(1)
                                                complexity.
            price_range
                -> AVLTree(),   price_range is used to sort buy price of all potions. each node stores a list containing all potions
                                with the same buy price. This enables a search for any buying price with log(n) complexity.
                                The reason for this search is so we can buy potions in (lowest price -> highest price) order.
            weights
                -> AVLTree(),   weights enables search of potions by (most value -> least value) using log(n) complexity.
                                This is because players would need to buy potions by (most weight -> least weight) when deciding
                                what potion to buy for maximum profit.


        :return: a list containing all profit made (type float).
        """
        #store values of all the prices adventurers buy the potions for
        if potion_valuations:
            self.adventurer = LinearProbePotionTable(len(potion_valuations), True)

        #dictionary containing all names for potions
        potion_vals = dict()

        #:complexity: O(N)
        for i in range(len(potion_valuations)):
            name = potion_valuations[i][0]
            price = potion_valuations[i][1]
            potion_vals[i] = potion_valuations[i][0]
            new_potion = Potion.create_empty(name,"null0",price)
            self.adventurer[name] = new_potion

        if potion_vals:
            #AVLTree for price_range
            price_range = AVLTree()
            #price check and order in price range :complexity: O(N x log(N))
            for i in potion_vals:
                name = potion_vals[i]
                max_price = self.inventory[name].buy_price*self.inventory[name].quantity
                # O(log(N))
                price_range[max_price] = name

            #AVLTree for weights
            weights = AVLTree()
            #order in terms of weight O(N x log(N))
            for i in range(len(price_range)):
                name = price_range.kth_largest(len(price_range)-i).item
                # O(log(N))
                weight = self.adventurer[name].buy_price - self.inventory[name].buy_price
                if weight in weights:
                    weights[weight].append(name)
                else:
                    weights[weight] = [name]

            #create order of buying potions :complexity: O(N)
            buy_list_w = []
            for i in range(len(weights)):
                weight = weights.kth_largest(i+1).item
                for j in weight:
                    buy_list_w.append(j)

            #convert to dictionary :complexity: O(N)/O(N X log(N))
            buy_list = dict()
            for i in range(len(buy_list_w)):
                buy_list[i] = buy_list_w[i]

        #if potion_valuations is empty, returns 0 as a solution
        else:
            return [0]

        #Local helper functions:
        #--------------------------------------------------------------------------------------------------

        #O(1) as single operations
        def _find_max_profit(starting_money:float, name:str) -> tuple[float | int, float | int]:
            """
            Takes the starting money and name of a potion, then returns a tuple containing 2 variables:
                profit_made -> the total money player has made from selling potions to adventurers
                excess_money -> the remaining money (excluding profit) after purchase

            :param starting_money (float): the amount of money player currently has
            :param name: the potion_type of the Potion class
            :complexity: O(1) as single operations

            :return: a tuple of 2, of type float or int
                quantity_bought: int/float
                excess_money: int/float
            """
            buy_price = self.inventory[name].buy_price
            quantity = self.inventory[name].quantity
            sell_price = self.adventurer[name].buy_price
            total_buy_price = quantity*buy_price

            #if player does not have enough money to buy out the shop, excess money=0
            if total_buy_price > starting_money:
                quantity_bought = (starting_money/total_buy_price)*quantity
                excess_money = 0
            #if player has enough money to buy out the shop, excess money is calculated
            else:
                quantity_bought = quantity
                excess_money = starting_money-total_buy_price

            profit_made = quantity_bought*sell_price

            return profit_made, excess_money

        #O(n) as n is the length of the buy_list. all operations are O(1) but this is a recursive function
        def recurse(starting_money:float=0,position=0, buy_list=buy_list):
            """
            This recursive function takes the money of the player, starting_money, and calculates profit based on all
            items bought from the buy_list. Returns a float value of the profit made.

            :param starting_money: the amount of money player currently has
            :param position: the potion player is currently buying
            :param buy_list: the list of all potions player will buy
            :return: the total profit made by the player
            """
            #base case : if player is out of money or all items in the store is bought out. (player will never buy potions where player loses money)
            if not starting_money or position>=len(buy_list):
                return 0
            else:
                new_profit, new_money = _find_max_profit(starting_money,buy_list[position])
                new_position = position+1
                return new_profit + recurse(new_money, new_position)

        #--------------------------------------------------------------------------------------------------

        res = []
        # M->len(starting_money), N ->len(buy_list)[where length can end prematurely] :complexity:O(M x N),
        # recurse() stops as long as starting_money is used up, so it is mostly <MxN
        for i in starting_money:
            res += [recurse(i)]

        return res