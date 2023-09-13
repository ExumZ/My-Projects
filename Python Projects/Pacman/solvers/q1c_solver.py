import logging

import util
from problems.q1c_problem import q1c_problem
from problems.q1a_problem import q1a_problem

def weightedHeuristic(state, problem):
    foods = problem.goal # Goal = Food coordinates
    unvisited = [] # Unvisited foods
    node, visited = state # Current position, Visited positions
    heuristic = 0 # Initial heuristic value

    # Find and append all the foods that haven't been visited yet
    for food in foods:
        if not food in visited:
            unvisited.append(food)

    # Find the sum of the shortest distances between the unvisited foods using Manhattan Distance
    while unvisited:
        distance, food = min([(weighted_manhattan_distance(node, food, 2, problem), food) for food in unvisited])
        heuristic += distance
        node = food
        unvisited.remove(food)
    return heuristic

def q1c_solver(problem: q1c_problem, heuristic=weightedHeuristic):
    logger = logging.getLogger('root')
    logger.info('question 1c')

    # Use a priority queue, so the cost of actions is calculated with a provided heuristic
    frontier = util.PriorityQueue()
    # Make an empty list of explored nodes
    visited = []
    # Make an empty list of actions
    actionList = []
    # Initialize current state
    currentState = problem.getStartState()

    # Place the starting point in the priority queue
    frontier.push((currentState, actionList), heuristic(currentState, problem))

    while frontier:
        # While the fronter is not empty, pop out the node and actions
        node, actions = frontier.pop()
        # If node is not visited, append the node
        if not node in visited:
            visited.append(node)
            # Return the list of actions if node contains the food pellet
            if problem.isGoalState(node):
                return actions
            # Get successors after each action
            for successor in problem.getSuccessors(node):
                point, direction, cost = successor
                nextActions = actions + [direction]
                nextCost = cost + heuristic(point, problem)
                frontier.push((point, nextActions), nextCost)
    return []

def weighted_manhattan_distance(point1, point2, wall_cost, maze):
    """
        Increase in cost if there's a wall in the path
    """
    # Checks whether or not it's a clear path
    if is_clear_path(maze, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
        # If not, increase the cost of the path
    else:
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + wall_cost

def is_clear_path(problem: q1c_problem, point1, point2):
    """
        Variant of Bresenham's Line Algorithm
            - Helper function used to check whether or not there's a wall in the path

        Referenced the pseudocode in the attached link:
        https://www.baeldung.com/cs/bresenhams-line-algorithm#:~:text=Bresenham

    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the absolute difference between the x and y coordinates respectively
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Determines which direction to move
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    error = dx - dy

    # If target not reached, keep calculating
    while x1 != x2 or y1 != y2:
        # If there's a wall...
        if problem.walls[x1][y1]:
            return False
        
        e2 = 2 * error
        
        # Error adjustment
        if e2 > -dy:
            error -= dy
            x1 += sx

        if e2 < dx:
            error += dx
            y1 += sy

    return True
