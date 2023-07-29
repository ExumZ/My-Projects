__author__ = "Lee Zhi Yong"

"""

    #########################################################################################################
    #                                                                                                       #
    #                                Assignment 2 Question 1: Fast Backups                                  #
    #                                            Final Version                                              #
    #                                                                                                       #
    #########################################################################################################
    
"""
class Graph:
    """
        This Graph class is a modified version of the Graph class I used in Assignment 1 Q1
    
    """
    def __init__(self, vertices_count):
        self.vertices = [None] * (vertices_count * 2 + 2)
        for i in range(vertices_count * 2 + 2):
            self.vertices[i] = Vertex(i)

    def __str__(self):
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "Vertex " + str(vertex) + "\n"
        return return_string

    def add_edges(self, edges):
        for edge in edges:
            u = edge[0]
            v = edge[1]
            capacity = edge[2]
            current_edge = Edge(u, v, capacity)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)

    def bfs(self, start_vertex, end_vertex):
        """
            Note:
                This BFS is a modified version of the BFS given to us in our lecture slides.
            
            Function description: 
                Breadth First Search Algorithm that is used in the Ford Fulkerson Method later on to traverse through the graph to check whether or not 
                any paths still exist from the start vertex to the end vertex.

            :Input:
            argv1: The start vertex
            argv2: The end vertex

            :Preconditions:
                1. The start and end vertex must be given and valid

            :Output, return or postcondition: Returns true is a path does exist from start to end vertex; returns false is no path is found.

            :Time complexity: O(D+C), where D is the number of data centres, and C is the number of communication channels

                We will be traversing through the vertices, the worst case being all the vertices, so it would result in a time complexity of O(D) in this
                loop. Then, we will also perform constant time operations for each edge going out from the current vertex, the worst case be O(C). Thus,
                the final time complexity for this function is O(D+C)

            :Aux space complexity: O(C), where C is the number of communication channels

                Since we will be using a queue in the BFS to keep track of the vertices visited and previous vertices, we will need a constant amount of
                space for each vertex, which results in a space complexity of O(C)

        """
        # Create a queue for BFS traversal
        queue = []
        start = self.vertices[start_vertex]
        queue.append(start)
        start.visited = True

        while queue:
            current_vertex = queue.pop(0)

            # Check if the current vertex is the end vertex
            if current_vertex.id == end_vertex:
                break

            # Traverse all adjacent vertices of the current vertex
            for edge in current_vertex.edges:
                next_vertex = self.vertices[edge.v]

                # If the next vertex has not been visited and the residual capacity is greater than 0
                if not next_vertex.visited and edge.get_residual_capacity() > 0:
                    queue.append(next_vertex)
                    next_vertex.visited = True
                    next_vertex.previous = current_vertex.id

        # Return True if there is a path from start_vertex to end_vertex, False otherwise
        return self.vertices[end_vertex].visited
    
    def ford_fulkerson(self, source, sink):
        """
            Function description: 
                Ford Fulkerson Method used to find the max flow within the flow network. It generates a residual graph using the original graph before
                finding the augmented paths and updating the flow until the BFS algorithm can no longer find a path from the source to the sink.

            :Input:
            argv1: The source
            argv2: The sink

            :Preconditions:
                1. The source and sink must be given and valid

            :Output, return or postcondition: Returns the max flow of the flow network

            :Time complexity: O(|D|*|C|^2), where D is the number of data centres, and C is the number of communication channels

                The outer loop will keep running until no more augmented paths exist. In the worst case, the number of iterations of this while loop can
                go up to O(D) since the size of the graph is the number of data centres * 2 + 2 in this implementation which simplifies back down to O(D).

                Then, the first inner while loop is responsible for finding the minimum residual capacity along the augmented path, which can iterate up
                to a total of C times since there can be at most C number of edges in the path.

                Next, the second inner while loop updates the flow along the augmented path, which can also iterate up to a total of C times.

                Thus, the time complexity is O(|D|*|C|^2).

            :Aux space complexity: O(C+D), where C is the number of communication channels

                Since we are using an adjacency list, it will require space proportional to the number of communication channels and data centres to store
                their values.

        """
        # Initialize the flow to 0
        max_flow = 0

        # Find augmenting paths and update the flow until no more paths exist
        while self.bfs(source, sink):
            # Initialize the path flow to infinity
            path_flow = float("inf")

            # Find the minimum residual capacity along the augmenting path
            v = sink
            while v != source:
                u = self.vertices[v].previous
                edge = self.find_edge(u, v)
                path_flow = min(path_flow, edge.get_residual_capacity())
                v = u

            # Update the flow along the augmenting path
            v = sink
            while v != source:
                u = self.vertices[v].previous
                edge = self.find_edge(u, v)
                edge.flow += path_flow
                v = u

            # Add the path flow to the overall max flow
            max_flow += path_flow

            # Reset the visited flags and previous pointers for the next iteration
            self.reset_visited()

        # Return the maximum flow
        return max_flow

    def reset_visited(self):
        """
            Function used to reset the visited vertices back to false
        
        """
        for vertex in self.vertices:
            if vertex:
                vertex.visited = False
                vertex.previous = 0

    def find_edge(self, u, v):
        """
            Function used to find the specific edge, given u and v
        
        """
        vertex = self.vertices[u]
        for edge in vertex.edges:
            if edge.v == v:
                return edge
        return None

class Vertex:
    """
        This Vertex class is a modified version of the Vertex class I used in Assignment 1 Q1
    
    """
    def __init__(self, id):
        self.edges = []
        self.id = id
        self.discovered = False
        self.visited = False
        self.previous = 0

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self) -> str:
        return_string = str(self.id)
        for edge in self.edges:
            return_string = return_string + "\n with edges " + str(edge)
        return return_string

class Edge:
    """
        This Edge class is a modified version of the Edge class I used in Assignment 1 Q1
    
    """
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def __str__(self):
        return_string = "(" + str(self.u) + ", " + str(self.v) + ", " + str(self.capacity) + ", " + str(self.flow) + ")"
        return return_string
    
    def get_residual_capacity(self):
        """
            Function used to calculate the residual capacity
        
        """
        return self.capacity - self.flow
    
def maxThroughput(connections, maxIn, maxOut, origin, targets):
    """
            Function description: 
                This function is used to the find the max throughput of the flow network given all the necessary information. It updates the graph accordingly
                so that we can use the Ford Fulkerson method to find the max flow.

            :Input:
            argv1: The list of connections
            argv2: The list of maxIn for each respective data centres
            argv3: The list of maxOut for each respective data centres
            argv4: The source vertex
            argv5: The list of targets

            :Preconditions:
                1. All the given inputs must be valid.

            :Output, return or postcondition: Returns the max flow of the flow network

            :Time complexity: O(|D|*|C|^2), where D is the number of data centres, and C is the number of communication channels

                The main part of the complexity comes from the Ford-Fulkerson method, which dominates the complexity of the other parts of the function.

            :Aux space complexity: O(C+D), where C is the number of communication channels

                Since we are using an adjacency list, it will require space proportional to the number of communication channels and data centres to store
                their values. We are technically using O((C*2+2) + D), but it simplifies back to O(C+D).

        """
    # Determine the number of data centers
    data_center_count = len(maxIn)

    capacity = []
    for i in range(len(maxIn)):
        capacity.append(min(maxIn[i], maxOut[i]))

    # Create a graph instance
    graph = Graph(data_center_count)

    # Add the communication channels to the graph
    graph.add_edges([[i, i+data_center_count, maxOut[i]] for i in range(data_center_count)])
    graph.add_edges([[connection[0]+data_center_count, connection[1], min(connection[2], capacity[connection[1]])] for connection in connections])

    # Create supersource and supersink vertices
    supersource = data_center_count * 2
    supersink = data_center_count * 2 + 1

    # Connect targets to supersink
    for target in targets:
        graph.add_edges([(target, supersink, maxOut[target])])

    # Connect supersource to origin
    graph.add_edges([(supersource, origin, maxOut[origin])])

    # Compute the maximum flow using Ford-Fulkerson algorithm
    max_flow = graph.ford_fulkerson(supersource, supersink)

    return max_flow

"""

    #########################################################################################################
    #                                                                                                       #
    #                                   Assignment 2 Question 2: catGPT                                     #
    #                                            Final Version                                              #
    #                                                                                                       #
    #########################################################################################################
    
"""
class Node:
    """
    Node Class for Q2
     - Each node will depict a char

    """
    def __init__(self, char=None, size=27):
        """
        Init for the Node class
         - Initializes the variables for each node
         - Note: max_frequency is the max frequency of the leaf node that will be saved in each node

        """
        self.char = char
        self.link = [None] * size
        self.frequency = 0
        self.last = False
        self.max_frequency = 0

class CatsTrie:
    """
    Trie Class for Q2
     - A trie class that encapsulates all of the cat sentences.

    """
    def __init__(self, sentences):
        """
            Function description: 
                Initializes the CatsTrie by inserting and linking the nodes. During this process, it will update the nodes with their frequencies
                and also note down whether it is the leaf node or not. It does so by first create the root node before building the rest of the
                Trie using the build() function.

            :Input:
            argv1: The list of sentences

            :Preconditions:
                1. The list of sentences must contain at least one sentence.

            :Output, return or postcondition: Builds a Trie that contains all the sentences, characters, and their frequencies.

            :Time complexity: O(NM), where N is the number of sentence in sentences and M is the number of characters in the longest sentence.

                During the initialization process, we will be inserting/updating the Trie at least N*M times. To be more accurate, we will be updating
                the Trie N*T times, where T is the number of characters in each sentence.

            :Aux space complexity: O(NM), where N is the number of sentence in sentences and M is the number of characters in the longest sentence.

                Similarly, we will also need approximately N*M amount of space to store all the information of the Trie. 

        """
        self.root = Node()
        self.build(sentences)

    def build(self, sentences):
        """
            Function description: 
                For each sentence in sentences, it will insert them one by one into the Trie. Everything else, is explained in the documentation
                for __init__.

            :Input:
            argv1: The list of sentences

            :Preconditions:
                1. The list of sentences must contain at least one sentence.

            :Time complexity: O(NM), where N is the number of sentence in sentences and M is the number of characters in the longest sentence.

                Calls insert for each sentence in sentences.

        """
        for sentence in sentences:
            self.insert(sentence)

    def insert(self, key):
        """
            Function description: 
                Recursively calls itself to insert each characters of a sentence.

        """
        self.insert_recursive(key, self.root, 0)

    def insert_recursive(self, key, current, key_pos):
        """
            Function description: 
                Recursive function used by insert to create the nodes and update them until it reaches the base case (leaf node) and sets last as true
                for that particular node. It will also update the max_frequency on the way up the recursion with the frequency of the leaf node with
                the highest frequency. This will be used later on to traverse down the trie to obtain the most frequency word that can autocomplete
                the prompt given to us.

            :Input:
            argv1: The key that needs to be inserted into the trie data structure
            argv2: The current node of the trie where the insertion is being performed
            argv3: The integer keeping track of the current position of the key 

            :Time complexity: O(M), M is the length of the sentence.
                Inserts or updates the nodes depending of which character it reads M times.

        """
        if key_pos == len(key):
            current.frequency += 1
            current.last = True
            current.max_frequency = current.frequency
            return

        char = key[key_pos]
        index = ord(char) - 97 + 1

        if current.link[index] is None:
            current.link[index] = Node(char)

        child = current.link[index]
        self.insert_recursive(key, child, key_pos + 1)
        current.max_frequency = child.max_frequency
        
    def findHighestFrequencyWord(self, current, prefix, highest_freq, highest_word):
        """
            Function description: 
                Finds the highest frequency word for the autoComplete method. This function checks through every child starting from the children of the prefix
                node for the max_frequency. If the max frequency of the child is greater than the current max frequency, we will traverse down the direction of
                that child node. By referring to this max_frequency variable, we can effectively traverse down the path that will lead us to the most frequent
                sentence in sentences that can autocomplete the given prompt.

            :Input:
            argv1: The current node
            argv2: The entire prefix
            argv3: The highest frequency so far
            argv4: The word with the highest frequency so far

            :Preconditions:
                1. There needs to be at least one node.
                2. There needs to be some prefix.
                3. It needs to be given the highest recorded frequency so far.
                4. It needs to be given the word with the highest frequency so far.

            :Output, return or postcondition: Returns either the prefix or the prefix + the rest of the characters that makes up the most frequent sentence
                                                in sentences.

            :Time complexity: O(Y), where Y is the length of the most frequent sentence in sentences that begins with the prompt, unless such a prompt does not 
                                        exist (in which case findHighestFrequencyWord() should have a time complexity of O(1)). Thus, this is an output sensitive 
                                        complexity.

                This function will always assume the trie traversal is already at the desired prefix node. By only storing the max_frequency amongst all leaf
                nodes below the prefix node, we can easily traverse down only the children with the highest max_frequency. Since we previously updated the
                max_frequency variable to be the highest frequency of a particular leaf node, we can easily traverse down to obtain characters that make up
                the most frequent sentence in sentences by simply following the one child node with the highest max_frequency rather than manually traversing down 
                to each leaf node from the children of the prefix node.

        """
        if current.last and current.frequency > highest_freq:
            highest_freq = current.frequency
            highest_word = prefix

        max_child_freq = 0
        max_child_index = -1

        for index in range(len(current.link)):
            child = current.link[index]
            if child is not None:
                if child.max_frequency > max_child_freq:
                    max_child_freq = child.max_frequency
                    max_child_index = index

        if max_child_index != -1:
            child = current.link[max_child_index]
            char = chr(max_child_index + 97 - 1)
            word = prefix + char
            highest_freq, highest_word = self.findHighestFrequencyWord(child, word, highest_freq, highest_word)

        return highest_freq, highest_word

    def autoComplete(self, prompt):
        """
            Function description: 
                Given a prompt, this function will auto-complete the sentence with the most frequent sentence in sentences. There may be cases where the prompt
                itself is the most frequent sentence in sentences.

            :Input:
            argv1: The prompt

            :Preconditions:
                1. It needs to be given a prompt.

            :Output, return or postcondition: Returns the auto-completed sentence based on the prompt given.

            :Time complexity: O(X+Y), where X is the length of the prompt and Y is the length of the most frequent sentence in sentences that begins with the 
                                        prompt, unless such a prompt does not exist (in which case autoComplete() should have a time complexity of O(X)). Thus,
                                        this is an output sensitive complexity.

                This function will first traverse to the prefix node in O(X) time before calling the findHighestFrequencyWord() function, which runs in O(Y) time. 
                However, if such a prompt does not exist, findHighestFrequencyWord() should then have a time complexity of O(1). Thus, this is an output sensitive 
                complexity.

        """
        current = self.root

        for char in prompt:
            index = ord(char) - 97 + 1
            if current.link[index] is None:
                return None
            current = current.link[index]

        highest_freq = -1
        highest_word = None

        highest_freq, highest_word = self.findHighestFrequencyWord(current, prompt, highest_freq, highest_word)

        return highest_word