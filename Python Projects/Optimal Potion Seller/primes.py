__author__ = "Zhi Yong Lee, Terenia Lee Leh Yi, Yu Wen Liew, Jeremy Koh Chi Minn"
__docformat__ = 'reStructuredText'

def largest_prime(k: int) -> int:
    """
    This methods return the  largest prime number strictly less than k
    :pre: k is an integer larger or equal to 2
    :complexity: O(nlogn)
    :param k
    :return: Return the largest prime number less than k
    """
    prime_numbers = []
    is_prime=[]
    for i in range(2,k):
        is_prime+=[True]

    starting_prime = 2
    while ((starting_prime * starting_prime) < k):
        if (is_prime[starting_prime - 2] == True):
            for i in range(starting_prime * starting_prime, k , starting_prime):
                is_prime[i - 2] = False
        starting_prime += 1
    for i in range(2, k ):# loop through is_prime and insert numbers if is_prime[i] is True (which means that number is prime)
        if is_prime[i - 2]:
            prime_numbers += [i]# add prime number into list

    return prime_numbers[-1] #return largest prime number
