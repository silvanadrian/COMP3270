from heapq import heappush, heappop  
def aStarTsa(stateSpaceGraph, h, startState, goalState): 
    frontier = []
    heappush(frontier, (h[startState], startState))
    print('Initial frontier:',list(frontier)); input()
    while frontier:
        node = heappop(frontier)
        if (node[1].endswith(goalState)): return node
        print('Exploring:',node[1][-1],'at cost',node[0])
        for child in stateSpaceGraph[node[1][-1]]:
            heappush(frontier, (node[0]+child[0]-h[node[1][-1]]+h[child[1]], node[1]+child[1]))
        print(list(frontier)); input()
practice = {
    'S':[(3,'a'),(2,'d'),(10,'G')],'a':[(5,'b')],
    'd':[(1,'b'),(4,'e')],'G':[],'b':[(1,'e'),(2,'c')],
    'e':[(3,'G')],'c':[(4,'G')]}
practiceH = {'S':7,'a':9,'b':4,'c':2,'d':5,'e':3,'G':0}
print('Solution path:',aStarTsa(practice, practiceH, 'S', 'G'))






