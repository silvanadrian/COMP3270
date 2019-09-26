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

def search(prob, f, dirs, explored, type):
    while f:
        node = f.pop()
        dir = dirs.pop()
        if prob.isGoalState(node[-1]):
            return dir
        if node[-1] not in explored:
            if type == 'bfs':
                explored.append(node[-1])
            if type == 'dfs':
                explored.add(node[-1])
            for child in prob.getSuccessors(node[-1]):
                list1 = list(node)
                list1.append(child[0])
                f.push(list1)
                list2 = list(dir)
                list2.append(child[1])
                dirs.push(list2)

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
    return search(problem, frontier, directions, explored_set,'dfs')

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    directions = util.Queue()
    frontier.push([problem.getStartState()])
    directions.push([])
    explored_list = []
    return search(problem, frontier, directions, explored_list,'bfs')

def search2(prob,explored, h, type):
    frontier = []
    if type == 'ucs':
        heappush(frontier, (0, [prob.getStartState()], []))
    if type == 'astar':
        heappush(frontier, (h(prob.getStartState(), prob), [prob.getStartState()], []))
    while frontier:
        node = heappop(frontier)
        if prob.isGoalState(node[1][-1]):
            return node[2]
        if node[1][-1] not in explored:
            if type == 'ucs':
                explored.add(node[1][-1])
            if type == 'astar':
                explored.append(node[1][-1])
            for child in prob.getSuccessors(node[1][-1]):
                list1 = list(node[1])
                list1.append(child[0])
                list2 = list(node[2])
                list2.append(child[1])
                if type == 'ucs':
                    heappush(frontier, (node[0] + child[2], list1, list2))
                if type == 'astar':
                    heappush(frontier, ((node[0] + child[2] - h(node[1][-1], prob) + h(child[0], prob)), list1, list2))

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    explored = set()
    return search2(problem,explored, 0, 'ucs')

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    explored = []
    return search2(problem, explored, heuristic, 'astar')

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
