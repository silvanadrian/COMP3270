from heapq import heappush, heappop
def ucsGsa(stateSpaceGraph, startState, goalState): 
    frontier = []
    heappush(frontier, (0, startState))
    exploredSet = set()
    print('Initial frontier:',list(frontier)); input()
    while frontier:
        node = heappop(frontier)
        if (node[1].endswith(goalState)): return node
        if node[1][-1] not in exploredSet:
            print('Exploring:',node[1][-1],'at cost',node[0])
            exploredSet.add(node[1][-1])
            for child in stateSpaceGraph[node[1][-1]]:
                heappush(frontier, (node[0]+child[0], node[1]+child[1]))
            print(list(frontier)); print(exploredSet); input()
practice = {
    'S':[(3,'a'),(2,'d'),(10,'G')],'a':[(5,'b')],
    'd':[(1,'b'),(4,'e')],'G':[],'b':[(1,'e'),(2,'c')],
    'e':[(3,'G')],'c':[(4,'G')]}

quiz1 = {
    'S': [(3,'a'), (1,'c'), (3,'d')],
    'a' : [(1,'e')],
    'c' : [(1,'e')],
    'd' : [(1,'e'), (1,'G')],
    'e' : [(2,'f')],
    'f' : [(1,'b'), (1,'d')],
    'b' : [(1,'e'), (2,'G')]
}

quiz1_19 = {
    'A':[(1,'B'),(4,'C')],
    'B':[(1,'A'),(1,'C'),(5,'D')], 
    'C':[(4,'A'),(1,'B'),(3,'D')], 
    'D':[(5,'B'),(3,'C'),(8,'E'),(3,'F'),(9,'G')],
    'E':[(8,'D'),(2,'G')],
    'F':[(3,'D'),(5,'G')]
    }

print('Solution path:',ucsGsa(quiz1_19, 'A', 'G'))






