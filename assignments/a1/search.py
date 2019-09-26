"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from heapq import heappush, heappop

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def search(problem, frontier, directions, explored_set):
    while frontier:
        node = frontier.pop()
        direct = directions.pop()
        if problem.isGoalState(node[-1]):
            return direct
        if node[-1] not in explored_set:
            if isinstance(explored_set, list):
                explored_set.append(node[-1])
            else:
                explored_set.add(node[-1])
            for child in problem.getSuccessors(node[-1]):
                temp1 = list(node)
                temp1.append(child[0])
                frontier.push(temp1)
                temp2 = list(direct)
                temp2.append(child[1])
                directions.push(temp2)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    directions = util.Stack()
    frontier.push([problem.getStartState()])
    directions.push([])
    explored_set = set()
    return search(problem, frontier, directions, explored_set)

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    directions = util.Queue()
    frontier.push([problem.getStartState()])
    directions.push([])
    explored_set = []
    return search(problem, frontier, directions, explored_set)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    frontier = []
    heappush(frontier, (0, [problem.getStartState()], []))
    explored_set = set()
    while frontier:
        node = heappop(frontier)
        if (problem.isGoalState(node[1][-1])):
            return node[2]
        if node[1][-1] not in explored_set:
            explored_set.add(node[1][-1])
            for child in problem.getSuccessors(node[1][-1]):
                temp1 = list(node[1])
                temp1.append(child[0])
                temp2 = list(node[2])
                temp2.append(child[1])
                heappush(frontier, (node[0] + child[2], temp1, temp2))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    frontier = []
    heappush(frontier, (heuristic(problem.getStartState(), problem), [problem.getStartState()], []))
    explored_set = []
    while frontier:
        node = heappop(frontier)
        if problem.isGoalState(node[1][-1]):
            return node[2]
        if node[1][-1] not in explored_set:
            explored_set.append(node[1][-1])
            for child in problem.getSuccessors(node[1][-1]):
                temp1 = list(node[1])
                temp1.append(child[0])
                temp2 = list(node[2])
                temp2.append(child[1])
                heappush(frontier, ((node[0] + child[2] - heuristic(node[1][-1], problem) + heuristic(child[0], problem)), temp1, temp2))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
