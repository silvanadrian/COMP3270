from heapq import heappush, heappop
def greedyTsa(stateSpaceGraph, h, startState, goalState): 
    frontier = []
    heappush(frontier, (h[startState], startState))
    print('Initial frontier:',list(frontier)); input()
    while frontier:
        node = heappop(frontier)
        if (node[1].endswith(goalState)): return node
        print('Exploring:',node[1][-1],'at cost',node[0])
        for child in stateSpaceGraph[node[1][-1]]:
            heappush(frontier, (h[child[1]], node[1]+child[1]))
        print(list(frontier)); input()
aStarMotivation = {
    'S':[(1,'a')],'a':[(1,'b'),(3,'d'),(8,'e')],
    'b':[(1,'c')],'c':[],'d':[(2,'G')],
    'e':[(1,'d')]}
aStarMotivationH = {
    'S':6,'a':5,'b':6,'c':7,'d':2,'e':1,'G':0}
print('Solution path:',greedyTsa(aStarMotivation, aStarMotivationH, 'S', 'G'))






