__author__ = "Lee Zhi Yong"

"""

    ########################################################################################################
    #                                                                                                      #
    #                           Assignment 1 Question 1: (Should I give a ride?)                           #
    #                                            Final Version                                             #
    #                                                                                                      #
    ########################################################################################################
    
"""
def optimalRoute(start, end, passengers, roads):

    """
        Function description: 
            This function is used to find the optimal route from the start location to end location. You can choose whether to pick up a passenger or not 
            (to use the carpool lane) to reach the destination. In my implementation, I essentially created a two-layered graph that is connected via
            the passenger vertices with a zero weight edge. The first layer would only have non-carpool lanes while the second layer would only have
            carpool lanes. First, it will call Dijkstra's algorithm to run through the first graph with only one layer. Then, it will call Dijkstra's again 
            to run through both the first and second layers in the second graph until it reaches that mirrored destination in the second layer. If the time 
            taken in the first call is greater than the time taken in the second call of Dijkstra's, then it will return the route taken in the second 
            of call of Dijkstra's.

        :Input:
        argv1: start location
        argv2: end location
        argv3: list of locations where the passengers are at
        argv4: list of roads [start, end, time it takes when using non-carpool lane, time it takes when using carpool lane]

        :Preconditions:
            1. The start and end locations are valid and exist in the list of locations in the graph
            2. The list of passengers is either empty of contains valid locations in the graph
            3. The list of roads contains valid information (start location, end location, weight of non-carpool lane, weight of carpool lane)

        :Output, return or postcondition: Returns the optimal route (with least time taken) used to reach the destination

        :Time complexity: O(R log L) where P is the number of passengers, R is the number of roads, and L is the number of locations in the graph.

            This function runs Dijkstra's algorithm twice, which takes O(R log L) time for each call = 2 * O(R log L).

            While the more accurate time complexity is 2 * O((R+L)log L), we know that R is always greater than L and the constant of 2 can be
            simplified to just O((R+L)log L). Thus, the overall time complexity becomes O(R log L).

        :Aux space complexity: O(L+R), where L is the number of locations and R is the number of roads in the graph

            Since we are storing the graphs in the functions and taking into account that the space complexity of Dijkstra's algorithm is O(L), 
            we will be using an overall space complexity of O(L+R). This is simplified from 2*O(L+R) as we will create 2 graphs.

    """

    # Finds the end vertex with the largest value and + 1 to get the number of vertices
    no_vertex = max([road[1] for road in roads]) + 1
    # end if the destination in the first layer of the graph
    # end1 is the mirrored end destination in the second layer (carpool lanes) of the graph
    end1 = end + no_vertex

    #Initialize the graphs
    graph = Graph(no_vertex)
    graph1 = Graph(no_vertex)

    # Find the passenger vertices and set the passenger attribute for the vertex with a passenger to True
    passenger_vertices = [0] * len(passengers)
    for i in range(len(passengers)):
        graph.vertices[i].passenger = True
        passenger_vertices[i] = passengers[i]
        graph.passenger_vertices = passenger_vertices

    # Add the edges in the first layer
    graph.add_edges([[road[0], road[1], road[2]] for road in roads])

    # Run only through the first layer
    non_carpool_path = graph.dijkstra(start, end)

    # If there's no passenger vertices, just return the non-carpool path (Algorithm stops here in this case)
    if graph.passenger_vertices == []:
        return non_carpool_path[1]
    
    # Add the edges in the first layer
    graph1.add_edges([[road[0], road[1], road[2]] for road in roads])

    # Add the edges in the second layer
    graph1.add_edges([[road[0]+no_vertex, road[1]+no_vertex, road[3]] for road in roads])

    # Connect the two layers via the passenger vertices
    for vertex in graph.passenger_vertices:
        graph1.vertices[vertex].add_edge(Edge(graph1.vertices[vertex].id, graph1.vertices[vertex].id+no_vertex, 0))
    
    # Run starting from the start vertex in the first layer and end at the mirrored destination in the second layer
    carpool_path = graph1.dijkstra(start, end1)

    # Update the vertex numbers for the vertices in the second layer to match the vertex numbers in the first layer
    carpool_path[1] = [path - no_vertex if path >= no_vertex else path for path in carpool_path[1]]

    # Remove any duplicates (path it took from first layer to second layer via passenger vertices)
    carpool_path[1] = remove_consecutive_duplicates(carpool_path[1])

    # Returns the path with the shorter time taken
    if non_carpool_path[0] < carpool_path[0]:
        return non_carpool_path[1]
    return carpool_path[1]

"""

    ########################################################################################################
    #                                                                                                      #
    #                      Assignment 1 Question 2: (Repurposing Underused Workspace)                      #
    #                                            Final Version                                             #
    #                                                                                                      #
    ########################################################################################################
    
"""

def select_sections(occupancy_probability):

    """
        Function description: 
            This function is used to identify the list of locations (i, j) for n sections in an office which has the lowest total occupancy rate.
            Specifically, it removes only one section from each of the n rows and the sections selected for removal in two adjacent rows must be
            in the same or adjacent columns. The final output would be the list of indices of n sections from top down that has the total
            minimum occupancy rate.

            To be consistent, i = row ; j = column

        :Input:
        argv1: A list of lists (2D matrix) of occupancy probabilities

        :Precondition: The input is a list of lists (2D Matrix) of occupancy probabilities

        :Output, return or postcondition: Returns the total minimum occupancy rate of the selected elements in each row and the list of indices of n 
                                            sections from top down that contains the value that adds up to the total minimum occupancy rate

        :Time complexity: O(nm), where n is the number of rows and m is the number of columns in the input, occupancy_probability list (matrix).

            The functions iterates through each value of the list exactly once to fill in the occupancy matrix before backtracking through the
            matrix again to find the route with the loweset total occupancy.

        :Aux space complexity: O(nm), where n is the number of rows and m is the number of columns in the input, occupancy probability list (matrix).

            The function will create a new occupancy matrix that is the same size as the input, occupancy_probability. Furthermore, it stores the
            section_location list that will have at most n elements, technically making it O(nm + n). However, it can be simplified to O(nm)

    """

    # The number of rows
    n = len(occupancy_probability)
    # The number of columns
    m = len(occupancy_probability[0])

    # Initialize the matrix and set the values as 0
    occupancy_matrix = [[0] * m for i in range(n)]

    # Fill in the matrix
    for i in range(n):
        for j in range(m):
            
            # If the rate is at the far left side of the row
            if j == 0:
                #  There are no rates to its left (Only 2 rates to consider: middle and right)
                rates = [occupancy_matrix[i-1][0], occupancy_matrix[i-1][1]]

            # If the rate is at the far right side of the row
            elif j == m-1:
                #  There are no rates to its right (Only 2 rates to consider: middle and left)
                rates = [occupancy_matrix[i-1][m-1], occupancy_matrix[i-1][m-2]]

            # If the rate is anywhere else in the row
            else:
                # The three rates immediately to the left, right, and at the current rate in the previous row
                rates = [occupancy_matrix[i-1][j-1], occupancy_matrix[i-1][j], occupancy_matrix[i-1][j+1]]
                
            # The sum of the current rate's occupancy probability and the minimum occupancy probability of the rates in the previous row
            occupancy_matrix[i][j] = occupancy_probability[i][j] + min(rates)

    # Initialize variables to track the minimum total occupancy and its index
    min_total_occupancy = float('inf')
    lowest_occupancy_index = None

    # Iterate over the last row of the occupancy matrix and update the minimum total occupancy and index as necessary
    for i in range(len(occupancy_matrix[-1])):
        if occupancy_matrix[-1][i] < min_total_occupancy:
            min_total_occupancy = occupancy_matrix[-1][i]
            lowest_occupancy_index = i

    # Initialize the sections_location by the number of rows
    sections_location = [(0,0)] * n

    # Update the last section
    sections_location[n-1] = (n-1, lowest_occupancy_index)
    
    # Used to store the occupancy probabilities for when we backtrack later
    occupancy = occupancy_probability[n-1][lowest_occupancy_index]

    # Backtrack to find the route we came from to find the lowest total occupancy
    for i in range(n-2, -1, -1):
        # Find the adjacent columns with the lowest total occupancy
        rates = []

        # If there's only one column
        if m == 1:
            rate = (occupancy_matrix[i][0], 0)
            rates = [rate]

        # If the rate is on the far left side
        elif lowest_occupancy_index == 0:
            # Initialize the rates list since we know the size is always 2
            rates = [[] for i in range(2)]
            count = 0
            for k in range(2):
                rate = (occupancy_matrix[i][k], k)
                rates[count] = rate
                count += 1

         # If the rate is on the far right side
        elif lowest_occupancy_index == m-1:
            # Initialize the rates list since we know the size is always 2
            rates = [[] for i in range(2)]
            count = 0
            for k in range(m-2, m):
                rate = (occupancy_matrix[i][k], k)
                rates[count] = rate
                count += 1

        # If the rate is anywhere else
        else:
            # Initialize the rates list since we know the size is always 3
            rates = [[] for i in range(3)]
            count = 0
            for k in range(lowest_occupancy_index-1, lowest_occupancy_index+2):
                rate = (occupancy_matrix[i][k], k)
                rates[count] = rate
                count += 1

        # Backtrack and update
        lowest_occupancy_index = min(rates)[1]
        sections_location[i] = (i, lowest_occupancy_index)
        occupancy += occupancy_probability[i][lowest_occupancy_index]

    # Return the result
    return [occupancy, sections_location]

"""

    ########################################################################################################
    #                                                                                                      #
    #              All the classes and methods written below are only used by optimalRoute()               #
    #                                                                                                      #
    ########################################################################################################


"""

"""
This MinHeap is a modified version of the MinHeap from the PASS session
"""
class MinHeap():
    def __init__(self, max_size):
        """
        Constructor for MinHeap
        """
        # (Distance, Vertex)
        self.array = [(float('inf'), None)] * (max_size)
        self.length = 0
        self.index_map = [0] * max_size
    
    def insert(self, distance, vertex):
        """
        Add a vertex and its distance to MinHeap's array
        Time Complexity: O(log V), where V is the number of elements in the MinHeap
        """
        # Check if heap is full (For testing purposes)
        if self.length == len(self.array) - 1:
            raise Exception("Heap is full")

        self.length += 1 
        self.array[self.length] = (distance, vertex)
        self.index_map[vertex.id-1] = self.length
        self.rise(self.length)
    
    def serve(self):
        """
        Removes and returns the vertex with the smallest distance in the MinHeap's array
        Time Complexity: O(log V), where V is the number of elements in the MinHeap
        """
        # Check if heap is empty (For testing purposes)
        if self.length == 0:
            raise Exception("Heap is empty")
            
        min_vertex = self.array[1]
        self.array[1] = self.array[self.length]
        self.array[self.length] = (float('inf'), None)
        self.length -= 1 
        self.sink(1)
        return min_vertex

    def swap(self, x, y):
        """
        Swap two vertices' position and their index in the minheap array
        Time Complexity: O(1)
        """
        self.array[x], self.array[y] = self.array[y], self.array[x]
        self.index_map[self.array[x][1].id], self.index_map[self.array[y][1].id] = self.index_map[self.array[y][1].id], self.index_map[self.array[x][1].id]
    
    def rise(self, element):
        """
        Adjusts the position of the element accordingly
        Time Complexity: O(log V), where V is the number of elements in the MinHeap
        """
        parent = element // 2 
        while parent >= 1:
            if self.array[parent][1] > self.array[element][1]:
                self.swap(parent, element)
                element = parent 
                parent = element // 2
            else:
                break
    
    def sink(self, element):
        """
        Adjusts the position of the element accordingly
        Time Complexity: O(log V), where V is the number of elements in the MinHeap
        """
        child = 2*element 
        while child <= self.length: 
            if child < self.length and self.array[child+1][1] < self.array[child][1]:
                child += 1 
            if self.array[element][1] > self.array[child][1]:
                self.swap(element, child)
                element = child 
                child = 2*element 
            else:
                break

    def update(self, new_distance, vertex):
        """
        Updates the vertex and its distance in the MinHeap's array
        Time Complexity: O(log V), where V is the number of elements in the MinHeap
        """
        index = self.index_map[vertex.id-1]
        self.array[index] = (new_distance, vertex)
        self.rise(index)

class Graph:
    def __init__(self, vertices_count):
        self.vertices = [None] * vertices_count*2
        # Create enough space for two layers of the same set of vertices
        for i in range(vertices_count):
            self.vertices[i] = Vertex(i)
            self.vertices[i+vertices_count] = Vertex(i+vertices_count)
        self.passenger_vertices = []

    def __str__(self):
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "Vertex " + str(vertex) + "\n"
        return return_string

    def add_edges(self, edges):
        for edge in edges:
            u = edge[0]
            v = edge[1]
            w = edge[2] 
            current_edge = Edge(u,v,w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)

    def dijkstra(self, source, destination):
        """
            Function description: 
                Slightly modified Dijkstra's Algorithm using Adjacency List
                    - Finds the shortest route it takes to get from the start vertex to end vertex

            Reference:
                I referred to the outline for Dijkstra's algorithm from the FIT2004 Tutorial for Graphs.

            :Input:
            argv1: source (Start Vertex)
            argv2: destination (End Vertex)

            :Output, return or postcondition: Returns both the shortest distance from the source to destination and the route it took

            :Time complexity: O(R log L), where R is the number of edges and L is the number of vertices in the graph.

                The algorithm uses a Fixed MinHeap data structure (Priority Queue) to keep track of the discovered vertices, where each 
                vertex is added to the heap only once. Therefore, the while loop runs for a maximum of L iterations. Each iteration 
                serves the vertex with the smallest distance from the heap, which takes log L time. Then, the algorithm performs edge 
                relaxation on all adjacent vertices, which takes approximately O(R) time. 
                
                The total time complexity of the algorithm is O(R log L).

            :Aux space complexity: O(L)

                The algorithm uses the 'discovered' list to keep track of the vertices that have been discovered but not yet 
                visited, and a heap data structure is used to efficiently find the vertex with the smallest distance. 
                The heap and list discovered can contain at most L vertices, hence the space complexity is O(L). Additionally, 
                each vertex stores its own distance, path, visited, and previous attributes, which also contribute to the 
                auxiliary space complexity.

        """
        # Set the source vertex's distance to 0 and add it to the heap
        source_vertex = self.vertices[source]
        source_vertex.distance = 0
        source_vertex.path.append(source_vertex.id)
        
        # Fixed MinHeap(Number of Vertices)
        discovered = MinHeap(len(self.vertices))
        discovered.insert(source_vertex.distance, source_vertex)

        # Continue until the heap is empty
        # O(L): each vertex is placed in the min heap only once
        while discovered.length > 0:

            # Serve from the top of the heap
            # Always get the vertex with the shortest distance from the source that has not been visited
            # O(log L): serving from min heap
            u_distance, u = discovered.serve()

            # We know that no matter how many vertices we visit in the future, 
            # the distance of the served vertex will always be of this minimum distance
            u.visited = True 

            # Check if we've reached the destination
            if u == self.vertices[destination]:
                break

            # Perform edge relaxation on all adjacent vertices
            for edge in u.edges:
                # O(L): the max nuymber of edges from a vertex is L-1
                v = self.vertices[edge.v]
                if v.discovered == False:                   # Means distance is still infinity since it's not discovered yet
                    v.discovered = True                     # Means I have discovered v and added it into the queue
                    v.distance = u.distance + edge.w
                    v.path = u.path.copy()
                    v.path.append(v.id)
                    v.previous = u
                    discovered.insert(v.distance, v)         
                # Otherwise, update v's distance if necessary            
                elif not v.visited:
                    # If there's a shorter distance, update it
                    if v.distance > u.distance + edge.w:
                        v.distance = u.distance + edge.w
                        v.path = u.path.copy()
                        v.path.append(v.id)
                        v.previous = u
                        # Update heap
                        # O(log L): when updating the min heap, we need to make sure the vertex rises to the correct position
                        discovered.update(v.distance, v)     # Update vertex v in heap with distance v.distance (shorter path); perform upheap

        # Returns the distance and path taken
        return [self.vertices[destination].distance, self.vertices[destination].path]

class Vertex:
    def __init__(self, id):
        self.edges = []
        self.id = id
        self.discovered = False
        self.visited = False
        self.distance = float('inf')
        self.path = []
        self.passenger = False
        self.previous = 0
    
    # Added to compare the vertex distances
    def __lt__(self, other):
        return self.distance < other.distance

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self) -> str:
        return_string = str(self.id)
        for edge in self.edges:
            return_string = return_string + "\n with edges " + str(edge)
        return return_string
    
    def added_to_queue(self):
        self.discovered = True

    def visit_node(self):
        self.visited = True

class Edge:
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return_string = "(" + str(self.u) + ", " + str(self.v) + ", " + str(self.w) + ")"
        return return_string

def remove_consecutive_duplicates(arr):

    """
        Function description: 
            Removes consecutive same numbers in an array.

        :Input:
        argv1: The input array

        :Output, return or postcondition: A new array with consecutive duplicates removed.

        :Time complexity: O(L) where L is the length of the input array.

            The function iterates through the entire array once to check for consecutive duplicates.

        :Aux space complexity: O(L)

            The size of the new array created to store the non-consecutive duplicates will be less than or equal 
            to the size the original array, and therefore requires the same amount of space. Additionally, the 
            function initializes a variable to store the previous number, which takes up a constant amount of space, 
            and does not depend on the size of the input array.

    """

    new_arr = [0] * (len(arr)-1)
    prev_num = None
    count = 0
    # For each number in the array, if the number != the previous number, new_arr[count] = num
    for num in arr:
        if num != prev_num:
            new_arr[count] = num
            # count only increments if the number != the previous number
            count += 1
        prev_num = num
    return new_arr
 