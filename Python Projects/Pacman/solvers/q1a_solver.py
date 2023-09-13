import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
    logger = logging.getLogger('root')
    logger.info('question 1a')

    # Use a priority queue for easier future implementations (Knows what to prioritize)
    frontier = util.PriorityQueue()
    # Make an empty list of explored nodes
    visited = []
    # Make an empty list of possible actions
    actionList = []
    # Initialize current state
    currentState = problem.getStartState()

    # Place the starting point in the priority queue
    frontier.push((currentState, actionList), 0)
    
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
                nextCost = cost
                frontier.push((point, nextActions), nextCost)
    return []
