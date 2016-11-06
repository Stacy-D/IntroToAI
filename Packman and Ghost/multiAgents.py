# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        total_agents = gameState.getNumAgents()

        def calculate_max_value(gamestate, current_depth):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), None

            successor_cost = []
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                successor_cost.append((calculate_min_value(successor, 1, current_depth), action))

            return max(successor_cost)

        def calculate_min_value(gamestate, agent_index, current_depth):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), None

            successors = [gamestate.generateSuccessor(agent_index, action) for action in actions_for_ghost]

            if agent_index == total_agents - 1:
                successor_cost = []
                for successor in successors:
                    successor_cost.append(calculate_max_value(successor, current_depth + 1))
            else:
                successor_cost = []
                for successor in successors:
                    successor_cost.append(calculate_min_value(successor, agent_index + 1, current_depth))

            return min(successor_cost)

        return calculate_max_value(gameState, 1)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        total_agents = gameState.getNumAgents()

        def calculate_max_value(gamestate, current_depth, alpha, beta):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), Directions.STOP

            v = float('-inf')
            bestAction = Directions.STOP
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                cost = calculate_min_value(successor, 1, current_depth, alpha, beta)[0]
                if cost > v:
                    v = cost
                    bestAction = action
                if v > beta:
                    return v, bestAction
                alpha = max(alpha, v)

            return v, bestAction

        def calculate_min_value(gamestate, agent_index, current_depth, alpha, beta):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), Directions.STOP

            v = float('inf')
            bestAction = Directions.STOP
            isPacman = agent_index == total_agents - 1
            for action in actions_for_ghost:
                successor = gamestate.generateSuccessor(agent_index, action)
                if isPacman:
                    cost = calculate_max_value(successor, current_depth + 1, alpha, beta)[0]
                else:
                    cost = calculate_min_value(successor, agent_index + 1, current_depth, alpha, beta)[0]

                if cost < v:
                    v = cost
                    bestAction = action
                if v < alpha:
                    return v, bestAction
                beta = min(beta, v)

            return v, bestAction

        defaultAlpha = float('-inf')
        defaultBeta = float('inf')
        return calculate_max_value(gameState, 1, defaultAlpha, defaultBeta)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        total_agents = gameState.getNumAgents()

        def calculate_max_value(gamestate, current_depth):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), None

            successors_score = []
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                successors_score.append((calculate_min_value(successor, 1, current_depth)[0], action))

            return max(successors_score)

        def calculate_min_value(gamestate, agent_index, current_depth):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), None

            successors = [gamestate.generateSuccessor(agent_index, action) for action in actions_for_ghost]

            successors_score = []
            isPacman = agent_index == total_agents - 1
            for successor in successors:
                if isPacman:
                    successors_score.append(calculate_max_value(successor, current_depth + 1))
                else:
                    successors_score.append(calculate_min_value(successor, agent_index + 1, current_depth))

            averageScore = sum(map(lambda x: float(x[0]) / len(successors_score), successors_score))
            return averageScore, None

        return calculate_max_value(gameState, 1)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

