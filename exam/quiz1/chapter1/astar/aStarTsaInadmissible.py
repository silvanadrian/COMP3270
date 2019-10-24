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
inadmissible = {
    'S':[(1,'a'),(5,'G')],'a':[(3,'G')], 'G':[]}
h = {'S':7,'a':6,'G':0}
print('Solution path:',aStarTsa(inadmissible, h, 'S', 'G'))






