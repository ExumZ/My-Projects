""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, modified by (Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn)'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    #insert_aux implementation
    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
            :complexity: O(1)
        """

        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left)) # update the current height

        current.num_of_left_nodes = self.recalculate_left_nodes(current) #update number of left nodes
        current.num_of_right_nodes=self.recalculate_right_nodes(current) #update number of right nodes
        return self.rebalance(current)

    #helper functions:
    #-------------------------------------------
    #_recalculate_left_node implementation
    def recalculate_left_nodes(self,current):
        """
        Calculate the number of nodes in left subtree
        :param current: the current mode
        :return: number of nodes in left subtree
        :complexity : O(1)
        """
        if current.left is None:
            return 0
        return current.left.num_of_left_nodes + current.left.num_of_right_nodes + 1

    #_recalculate_right_node implementation
    def recalculate_right_nodes(self,current):
        """
        Calculate the number of nodes in right subtree
        :param current: the current mode
        :return: number of nodes in right subtree
        :complexity : O(1)
        """
        if current.right is None:
            return 0
        return current.right.num_of_left_nodes +current.right.num_of_right_nodes +1
    #-------------------------------------------

    #delete_aux implementation
    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.

            :complexity: O(n) from get_successor()
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left)) # increase the current height
        current.num_of_left_nodes = self.recalculate_left_nodes(current)
        current.num_of_right_nodes = self.recalculate_right_nodes(current)
        return self.rebalance(current)

    #left_rotate implementation
    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        child = current.right
        temp = child.left

        child.left = current
        current.right = temp

        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))#update current height
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))#update child height
        current.num_of_right_nodes = self.recalculate_right_nodes(current)#update number of nodes in right subtree of current
        child.num_of_left_nodes = self.recalculate_left_nodes(child) #update number of nodes in left subtree in child
        return child

    #right_rotate implementation
    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        child = current.left
        temp = child.right

        child.right = current
        current.left = temp

        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right)) #update current height
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right)) #update child height
        current.num_of_left_nodes = self.recalculate_left_nodes(current) #update number of nodes in left subtree of current
        child.num_of_right_nodes = self.recalculate_right_nodes(child) #update number of nodes in right subtree in child
        return child


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """
        Pre: Current is a node
        Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
            :complexity: O(1)
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    #kth_largest implementation
    def kth_largest(self, k: int) -> AVLTreeNode:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.
        :pre: K is larger than 0 and equal or less than the total number of nodes in the tree (length)
        :param k (int): the kth largest element to search
        :complexity:
            - Best Case Complexity: O(1), where kth largest node  is the root node, the complexity is from kth_largest_helper
            - Worst Case Complexity: O(log(n)), where kth is the smallest or largest node, the complexity is from kth_largest_helper
        """
        current=self.root #take root as current node
        return self.kth_largest_helper(current,k) #start search for kth  largest from root

    #helper functions:
    #-------------------------------------------
    #_kth_largest_helper implementation
    def kth_largest_helper(self,current: AVLTreeNode, k:int) -> AVLTreeNode:
        """
        This helper function is called to return the kth largest node in the tree
        :pre: K is larger than 0 and equal or less than the total number of nodes in the tree (length), (done in kth_largest)
        :complexity:
            Best Case Complexity: O(1), where kth largest node  is the root node
            Worst Case Complexity: O(log(n)), where kth is the smallest or largest node
        :param current (AVLTReeNode): the current node
        :param k (int): the kth largest node to search for
        :return (AVLTReeNode): the largest node in the tree
        """
        if current.num_of_right_nodes+1==k: # if current is kth largest,return current
            return current
        elif current.num_of_right_nodes+1<k: # if k is larger than nodes left of current, that means k is in left subtree of current
            k=k-(current.num_of_right_nodes+1)
            current=current.left
            return self.kth_largest_helper(current,k)
        else:# k is smaller than number of nodes left of right side of current, hence k will be in the right subtree
            current=current.right
            return self.kth_largest_helper(current,k)
    #-------------------------------------------









