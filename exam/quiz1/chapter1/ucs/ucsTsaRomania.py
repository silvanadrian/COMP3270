from heapq import heappush, heappop
def ucsTsa(stateSpaceGraph, startState, goalState): 
    frontier = []
    heappush(frontier, (0, startState))
    print('Initial frontier:',list(frontier)); input()
    while frontier:
        node = heappop(frontier)
        if (node[1].endswith(goalState)): return node
        print('Exploring:',node[1][-1],'at cost',node[0])
        for child in stateSpaceGraph[node[1][-1]]:
            heappush(frontier, (node[0]+child[0], node[1]+child[1]))
        print(list(frontier)); input()
romania = {
    'A':[(140,'S'),(118,'T'),(75,'Z')],'Z':[(75,'A'),(71,'O')],'O':[(151,'S'),(71,'Z')],
    'T':[(118,'A'),(111,'L')],'L':[(70,'M'),(111,'T')],'M':[(75,'D'),(70,'L')],
    'D':[(120,'C'),(75,'M')],'S':[(140,'A'),(99,'F'),(151,'O'),(80,'R')],
    'R':[(146,'C'),(97,'P'),(80,'S')],'C':[(120,'D'),(138,'P'),(146,'R')],
    'F':[(211,'B'),(99,'S')],'P':[(101,'B'),(138,'C'),(97,'R')],'B':[]
    }
print('Solution path:',ucsTsa(romania, 'A', 'B'))






