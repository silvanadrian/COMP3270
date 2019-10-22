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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #  A capable reflex agent will have to consider both food locations and ghost locations to perform well.
        # return successorGameState.getScore()
        capsules = currentGameState.getCapsules()
        prevFoodList = prevFood.asList()
        score = currentGameState.getScore()
        distThreshold = 3  # when distance between Pacman and Ghost has some threshold reached

        # Scores I set as Base scores by playing around with them I found those values work ok
        scores = {
            "scaredGhost": 3000,
            "ghost": 300,
            "capsule": 200,
            "food": 100,
            "stop": 80
        }

        # Don't do moves into wrong directions
        if action == Directions.STOP:
            score -= scores["stop"]

        # handle Capsules
        for capsule in capsules:
            distance = manhattanDistance(capsule, newPos)
            if distance < 1:
                # if there is a capsule take it
                score += scores["capsule"]
            else:
                # make it dependent on distance and since
                # capsule give more points then food, try to get more capsules
                score += 10.0 / distance

        # handle Food
        for food in prevFoodList:
            distance = manhattanDistance(food, newPos)
            if distance < 1:
                # nearby food give a higher score
                score += scores["food"]
            else:
                # give score dependent on distance
                score += 1.0 / (distance ** 2)

        # handle ghosts (can be more then one, even as I see it in the tests only single Ghost is used)
        # use the distance from Pacman to ghost as indicator for score and if ghost is scared (eatable)
        for ghost in newGhostStates:
            distance = manhattanDistance(newPos, ghost.getPosition())
            if distance <= distThreshold:
                if ghost.scaredTimer > 0:
                    # ghost give high score for that
                    score += scores["scaredGhost"]
                else:
                    # stay away from not scared ghosts
                    score -= scores["ghost"]

        # works quite well even with 2 ghosts but pacman of course still dies quite often
        return score
        

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
    """
      Your minimax agent (question 2)
    """

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # get either min or max action back
        cost, action = self.minimax(gameState, 0, self.depth)

        return action

    def minMaxValue(self, state, agentIndex, depth,max):
        actions = state.getLegalActions(agentIndex)
        tempAction = Directions.STOP
        if max:
            # set - big value, compare and set new max for all possible  actions
            tempCost = -9999
        else:
            # set + big value compare and set new min for all possible actions
            tempCost = 9999
        for action in actions:
            cost = self.minimax(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]
            if max:
                # if max take max
                if cost > tempCost:
                    tempCost = cost
                    tempAction = action
            else:
                # else = min, take min
                if cost < tempCost:
                    tempCost = cost
                    tempAction = action

        # return tuple (cost, action)
        return tempCost, tempAction

    def minimax(self, state, index, depth):
        index = index % state.getNumAgents()

        if state.isWin() or state.isLose() or depth == 0:
            # Stop condition
            return self.evaluationFunction(state), Directions.STOP

        # whenever we went through all agents (0,1,2) for the case of the test
        if index == state.getNumAgents() - 1:
            depth -= 1

        # if agent is Pacman get max value otherwise min value
        if index % state.getNumAgents() == 0:
            return self.minMaxValue(state, index, depth, True)
        else:
            return self.minMaxValue(state, index, depth, False)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        cost, action = self.alphaBeta(gameState, 0, self.depth)
        return action

    def minMaxValuePrunning(self, state, index, depth, alpha, beta, isMax):
        actions = state.getLegalActions(index)
        tempAction = Directions.STOP
        if isMax:
            # set - big value, compare and set new max for all possible  actions
            tempCost = -9999
        else:
            # set + big value compare and set new min for all possible actions
            tempCost = 9999
        for action in actions:
            cost = self.alphaBeta(state.generateSuccessor(index, action), index + 1, depth, alpha, beta)[0]
            if isMax:
                # if max take max
                if cost > beta:
                    return cost, action
                if cost > tempCost:
                    tempCost = cost
                    tempAction = action
                alpha = max(alpha, cost)
            else:
                # else = min, take min
                if cost < alpha:
                    return cost, action
                if cost < tempCost:
                    tempCost = cost
                    tempAction = action
                beta = min(beta,cost)

        # return tuple (cost, action)
        return tempCost, tempAction

    def alphaBeta(self, state, index, depth, alpha = float("-inf"), beta = float("inf")):

        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), Directions.STOP

        index = index % state.getNumAgents()

        if index == state.getNumAgents() - 1:
            depth -= 1

        if index % state.getNumAgents() == 0:
            return self.minMaxValuePrunning(state, index, depth, alpha, beta, True)
        else:
            return self.minMaxValuePrunning(state, index, depth, alpha, beta, False)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        cost, action = self.expectimax(gameState, 0, self.depth)
        return action

    def minMaxValue(self, state, agentIndex, depth,isMax):
        actions = state.getLegalActions(agentIndex)
        tempAction = Directions.STOP
        total = 0
        if isMax:
            # set - big value, compare and set new max for all possible  actions
            tempCost = -9999
        else:
            # set + big value compare and set new min for all possible actions
            tempCost = 9999
        for action in actions:
            cost = self.expectimax(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]
            if isMax:
                # if max take max
                if cost > tempCost:
                    tempCost = cost
                    tempAction = action
            else:
                total += cost
                # else = min, take min
                tempAction = action
                tempCost = total/len(actions)

        return tempCost, tempAction

    def expectimax(self, state, index, depth):

        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), Directions.STOP

        index = index % state.getNumAgents()

        if index == state.getNumAgents() - 1:
            depth -= 1

        if index % state.getNumAgents() == 0:
            return self.minMaxValue(state, index, depth, True)
        else:
            return self.minMaxValue(state, index, depth, False)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    current_score = currentGameState.getScore()

    # set initial score
    score = 0.0

    #get the distances to the food in perspect to the pacman, store in list
    food_dists = []
    for food in foods:
        food_dists.append(manhattanDistance(newPos,food))

    # get all distances to ghosts
    ghost_dists = []
    for ghost in ghosts:
        ghost_dists.append(manhattanDistance(newPos, ghost.getPosition()))
        scared = ghost.scaredTimer
        if scared > 0:
            score += scared

    nearest_ghost = min(ghost_dists)
    # make score dependent on distance like in reflex agent
    food_Score = 0
    if len(food_dists) > 0:
        food_Score = 1.0/(min(food_dists))

    score += nearest_ghost * food_Score + current_score

    return score

# Abbreviation
better = betterEvaluationFunction

