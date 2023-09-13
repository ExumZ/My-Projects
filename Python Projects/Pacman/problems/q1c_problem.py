import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()

        # Set the list of positions of the Food as the goal_state
        self.goal = gameState.getFood().asList()

        # Cost for each action is always 1
        self.cost = 1

    @log_function
    def getStartState(self):
        visited = []
        return (self.startState, visited)

    def isGoalState(self, state):
        # The goal state is reached when all food pellets have been visited
        return len(state[1]) == len(self.goal)

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        currentPosition, foundFood = state
        successors = []
        # Checks all directions
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if not hitsWall:
                nextState = (nextx, nexty)
                # If the next position contains a food pellet AND has not been visited...
                if nextState in self.goal and nextState not in foundFood:
                    # Create a new list of visited positions by concatenating the current position with foundFood
                    visited = foundFood + [nextState]
                    # Append the list of visited positions to the list of successors
                    successors.append(( (nextState, visited), action, self.cost ))
                # If the next position is not a goal state OR has already been visited...
                else:
                    # Just append to the list of successors
                    successors.append(( (nextState, foundFood), action, self.cost ))

        return successors

