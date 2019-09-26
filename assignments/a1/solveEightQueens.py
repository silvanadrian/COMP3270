import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        #get the current board's square array
        currentBoardArray = self.squareArray
        #get the current costboard's square array to choose a lowest-cost decision
        costboardArray = self.getCostBoard().squareArray
        #initialize a minimum cost
        minCost = 10000
        #initialize a minimum cost list to store all positions which will cause minimum cost
        minCost_List = []
        for x in range(len(costboardArray)):
            for y in range(len(costboardArray[0])):
                if costboardArray[x][y] <= minCost:
                    minCost = costboardArray[x][y]
                    newRow = x
                    newCol = y
                    #store all the positions which have the same minimum cost
                    minCost_List.append(((newRow,newCol),minCost))
                for i in minCost_List:
                    if i[1] > minCost:
                        minCost_List.remove(i)
        #randomly select one minimum cost position of minCost_List
        newRow, newCol = minCost_List[random.randint(0,len(minCost_List)-1)][0]
        #set all the values of new column to 0
        for i in currentBoardArray:
            i[newCol] = 0
        #set the value of new queen position to 1
        currentBoardArray[newRow][newCol] = 1
        #assign betterBoard to be an instance of Board class
        #note the difference between class Board and its attribute 'squareArray'
        betterBoard = Board(currentBoardArray)
        minNumOfAttack = betterBoard.getNumberOfAttacks()

        return (betterBoard,minNumOfAttack,newRow,newCol)
        """
        newBoard = Board([[0 for _i in range(8)] for _j in range(8)])
        board = self.getCostBoard()
        min = 9000
        min_list = []
        for r in range(8):
            for c in range(8):
                if board.squareArray[r][c] < min:
                    min_list = []
                    min = board.squareArray[r][c]
                    row = r
                    col = c
                    min_list += [(row, col)]
                if board.squareArray[r][c] == min:
                    min_list += [(r, c)]
                if board.squareArray[r][c] == 9999:
                    newBoard.squareArray[r][c] = 1
        row, col = random.choice(min_list)
        for r in range(8):
            if newBoard.squareArray[r][col] == 1:
                newBoard.squareArray[r][col] = 0
        newBoard.squareArray[row][col] = 1
        attacks = min
        return (newBoard, attacks, row, col)
        """

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """


        numAttacks = 0
        board = self.squareArray
        queens = []

        for x in range(len(board[0])):
            for y in range(len(board)):
                if board[y][x] == 1:
                    queens.append((y,x))

        for i in range(len(queens)):

            for j in range(i+1,len(queens)):


                if queens[i][0] == queens[j][0]:
                    numAttacks += 1


                if abs(queens[i][0]-queens[j][0]) == abs(queens[i][1]-queens[j][1]):
                    numAttacks += 1


        return numAttacks

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
