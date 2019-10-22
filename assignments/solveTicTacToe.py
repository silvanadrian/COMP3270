#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser
import math

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        self.nrOfAgents=2
        self.depth=1
        self.winningState = ["a", "bb", "bc", "a"]
        self.fp = {  # only includes in-play positions (not boards with three-in-a-row)
            "000000000": "c",
            "100000000": "",
            "010000000": "",
            "000010000": "cc",
            "110000000": "ad",
            "101000000": "b",
            "100010000": "b",
            "100001000": "b",
            "100000001": "a",
            "010100000": "a",
            "010010000": "b",
            "010000010": "a",
            "110100000": "b",
            "110010000": "ab",
            "110001000": "d",
            "110000100": "a",
            "110000010": "d",
            "110000001": "d",
            "101010000": "a",
            "101000100": "ab",
            "101000010": "a",
            "100011000": "a",
            "100001010": "",
            "010110000": "ab",
            "010101000": "b",
            "110110000": "a",
            "110101000": "a",
            "110100001": "a",
            "110011000": "b",
            "110010100": "b",
            "110001100": "b",
            "110001010": "ab",
            "110001001": "ab",
            "110000110": "b",
            "110000101": "b",
            "110000011": "a",
            "101010010": "b",
            "101000101": "a",
            "100011010": "b",
            "010101010": "a",
            "110101010": "b",
            "110101001": "b",
            "110011100": "a",
            "110001110": "a",
            "110001101": "a",
            "110101011": "a"}
        self.winningState= ["cc", "a", "bb", "bc"]

    def transferBoard(self, board):
        rboard = ""
        for i in board:
            if i:
                rboard += "1"
            else:
                rboard += "0"
        return rboard

    def rotate(self,board):
        ans = board.copy()
        for i in range(3):
            for j in range(3):
                ans[j * 3 + 2 - i] = board[i * 3 + j]
        return ans

    def reflect(self,board):
        ans = board.copy()
        for i in range(3):
            for j in range(3):
                ans[i * 3 + 2 - j] = board[i * 3 + j]
        return ans

    def getFingerPrint(self, board):
        for reflection in range(2):
            for rotation in range(4):
                if self.transferBoard(board) in self.fp.keys():
                    return self.transferBoard(board)
                board = self.rotate(board)
            board = self.reflect(board)


    def getFingerPrints(self, state):
        boards=state.boards
        f=[]
        for board in boards:
            fp=self.getFingerPrint(board)
            if fp != None:
                f.append(fp)
            else:
                f.append("100000000")
        return f


    def fpScore(self, fingerprints):
        return [self.fp[f] for f  in fingerprints]

    def multiplyFp(self,scores):
        scores.sort()
        ans = "".join(scores)
        return ans

    def evaluationFunction(self, state):

        f1,f2,f3 = self.getFingerPrints(state) # Get fingerprints for all boards
        #print(f1 + f2 + f3 )
        s1,s2,s3 = self.fpScore([f1,f2,f3])# Get scores for fingerprints found on boards
        if self.multiplyFp([s1,s2,s3]) in self.winningState:
            return 1
        return 0

    def getAction(self, gameState, gameRules):
        legalActions = gameState.getLegalActions(gameRules)
        succGameState = [gameState.generateSuccessor(action) for action in legalActions]

        ans = [self.minimax(gameState, gameRules, cnt=1) for gameState in succGameState]
        print(ans)
        #ans=[self.evaluationFunction(state) for state in succGameState]
        bestScore = max(ans)
        bestIndices = [ index for index in range(len(ans)) if ans[index]==bestScore]
        print(bestIndices)
        chosenIndex = random.choice(bestIndices)

        #pdb.set_trace()
        return legalActions[chosenIndex]


    def minimax(self, gameState,gameRules,cnt=0):
        terminal, utility = self.valueState(self,gameState, gameRules , cnt)
        print(terminal)
        print(utility)
        if terminal: return utility  # This Code construct makes no difference for minimax whther utility is a heuristic or real utiliyt
        states = [gameState.generateSuccessor(action) for action in gameState.getLegalActions(gameRules)]
        if cnt%self.nrOfAgents==0:
            return max(self.minimax(state, gameRules, cnt + 1) for state in states)
        else:
            return min(self.minimax(state, gameRules, cnt + 1) for state in states)


        # It super interesting to not, that here the EVALUATION FUNCTION DEPENDS on the turns
        # Ifa evaluation function returns


    def valueState(self , agent, gameState, gameRules, cnt):
        if gameRules.isGameOver(gameState.boards):# IN terminal
            # , the player 0 gets 0 if he is in dead test, otherwise he gets 1
            if cnt%2==0:
                return [True,1] # MEANS THAT AGENT 1 MADE THE MOVE, SO AGENT 0 IS DEAD
            else: #MEANS THAT AGENT 0 MADE THE MOVE, SO AGENT0 1 IS DEAD
                return[True,0]
        # cnt is assumed to start from 0 , therefore the second move is 1, third 2, thus the condition following
        if math.floor(cnt / self.nrOfAgents) >= agent.depth:

            # print(cnt, " ",self.nrOfAgents," ", cnt/self.nrOfAgents)

            if cnt%2==0:# AGENT 1 MADE THE MOVE, WHICH REACHED THIS STATE
                if agent.evaluationFunction(gameState) == 0: ## IF AGENT
                    return [True,1]
                else:
                    return [True,0]
            else:
                return [True,agent.evaluationFunction(gameState) ]



        return [False, -sys.maxsize]




class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
