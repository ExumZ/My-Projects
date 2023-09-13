import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance
import numpy as np
import random

class Q2A_Agent(Agent):

    def __init__(self, evalFn = 'evaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always pacmanAgent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def alphaBetaSearch(self, pacmanAgent, depth, gameState, alphaMax, betaMin):
        # Check for three termination conditions
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)
        
        # Pacman's turn to maximize the score
        if pacmanAgent == 0:
            # Stores the max score Pacman can achieve
            value = -696969
            # Iterate over all the legal actions Pacman can take
            for action in getFilteredActions(pacmanAgent, gameState):
                # The function is called recursively with the updated pacmanAgent as Pacman tries to maximize his score
                value = max(value, self.alphaBetaSearch(1, depth, gameState.generateSuccessor(pacmanAgent, action), alphaMax, betaMin))
                alphaMax = max(alphaMax, value)
                # Alpha-Beta Pruning step: If betaMin <= alphaMax, then the current branch does not need exploration
                if betaMin <= alphaMax:
                    break
            # Return the true max value
            return value
        
        # Ghosts' turn to minimize the score
        else:
            # Iterate through the ghostAgents (Ex. Ghost1, Ghost2, etc.)
            ghostAgents = pacmanAgent + 1
            # Reset pacmanAgent turn
            if gameState.getNumAgents() == ghostAgents:
                ghostAgents = 0
            # Increment the depth to go deeper after each turn
            if ghostAgents == 0:
                depth += 1
                # Iterate over all the legal actions the ghosts can take
            for action in getFilteredActions(pacmanAgent, gameState):
                # Stores the min score Pacman can achieve
                value = 696969
                # The function is called recursively with the updated pacmanAgent as the ghosts tries to minimize their score
                value = min(value, self.alphaBetaSearch(ghostAgents, depth, gameState.generateSuccessor(pacmanAgent, action), alphaMax, betaMin))
                betaMin = min(betaMin, value)
                # Alpha-Beta Pruning
                if betaMin <= alphaMax:
                    break
            return value

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction using alpha-beta pruning.
        """
        # Contains a list of all the legal actions Pacman can take in the current game state
        possibleActions = getFilteredActions(0, gameState)

        # Instantiate alphaMax and betaMin values to their initial upper and lower bound
        alphaMax = -696969
        betaMin = 696969

        # Calculates the scores for each possible action by performing minimax search with alpha-beta pruning
        #  - Generates a successor game state for each action and calculates a score for it
        action_scores = [self.alphaBetaSearch(0, 0, gameState.generateSuccessor(0, action), alphaMax, betaMin) for action in possibleActions]

        # Take the max of the action_scores and randomly choose from the list of actions to tie break multiple of the same max values
        max_action = max(action_scores)
        max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
        chosenIndex = random.choice(max_indices)
        return possibleActions[chosenIndex]
    
def evaluationFunction(currentGameState):
    # Initialize the variables
    currentPosition = currentGameState.getPacmanPosition()
    currentFoodState = currentGameState.getFood()
    currentGhostState = currentGameState.getGhostStates()
    ghostScaredTimer = [ghostState.scaredTimer for ghostState in currentGhostState]

    """ Calculate distance to the nearest food """
    # Converts the layout of food pellets into a list of food positions
    currentFoodGrid = np.array(currentFoodState.asList())
    # Calculates the Manhattan distance between Pacman's position and each food position in the list
    distanceToFood = [manhattanDistance(currentPosition, food) for food in currentFoodGrid]
    minFoodDistance = 0
    # If there are any food pellets in the game, calculate the min distance to the food pellet(s)
    if len(currentFoodGrid) > 0:
        minFoodDistance = distanceToFood[np.argmin(distanceToFood)]

    """Calculate the distance to nearest ghost"""
    # Converts the positions of ghosts into a list of ghost positions
    ghostPositions = np.array(currentGameState.getGhostPositions())
    # Calculates the Manhattan distance between Pacman's position and each ghost position in the list
    distanceToGhost = [manhattanDistance(currentPosition, ghost) for ghost in ghostPositions]

    minGhostDistance = distanceToGhost[np.argmin(distanceToGhost)]
    nearestGhostScaredTime = ghostScaredTimer[np.argmin(distanceToGhost)]

    """ Priorities """
    # Avoid certain death if ghosts are near and they aren't scared
    if minGhostDistance <= 1 and nearestGhostScaredTime <= 0:
        return -696969
    
    # Prioritize eating scared ghosts
    if minGhostDistance <= 1 and nearestGhostScaredTime > 0:
        return 696969

    # Prioritize higher scores and closer food
    return currentGameState.getScore() * 5 - minFoodDistance

def getFilteredActions(index, gameState):
    """
        Filters out STOP action from all possible actions
    """
    possibleActions = gameState.getLegalActions(index)
    if Directions.STOP in possibleActions:
        possibleActions.remove(Directions.STOP)
    return possibleActions

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()