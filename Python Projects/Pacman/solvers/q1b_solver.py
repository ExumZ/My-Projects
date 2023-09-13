import logging

import util
from problems.q1b_problem import q1b_problem
from pacman import GameState

def fourDotsHeuristic(state, problem):
    """
    A heuristic for the Four Dots Problem

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    foods = problem.goal # Goal = Food coordinates
    unvisited = [] # Unvisited foods
    node, visited = state # Current position, Visited positions
    heuristic = 0 # Initial heuristic value

    # Find and append all the foods that haven't been visited yet
    for food in foods:
        if not food in visited:
            unvisited.append(food)

    # Find the sum of the shortest distances between the unvisited dots using Manhattan Distance
    while unvisited:
        distance, food = min([(util.manhattanDistance(node, food), food) for food in unvisited])
        heuristic += distance
        node = food
        unvisited.remove(food)
    return heuristic

def q1b_solver(problem: q1b_problem, heuristic=fourDotsHeuristic):
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

