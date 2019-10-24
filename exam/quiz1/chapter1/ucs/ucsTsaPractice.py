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
print('Solution path:',ucsTsa(practice, 'S', 'G'))






