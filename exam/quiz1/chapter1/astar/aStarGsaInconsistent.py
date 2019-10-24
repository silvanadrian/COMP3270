from heapq import heappush, heappop  
def aStarGsa(stateSpaceGraph, h, startState, goalState): 
    frontier = []
    heappush(frontier, (h[startState], startState))
    exploredSet = set()
    print('Initial frontier:',list(frontier)); input()
    while frontier:
        node = heappop(frontier)
        if (node[1].endswith(goalState)): return node
        if node[1][-1] not in exploredSet:
            print('Exploring:',node[1][-1],'at cost',node[0])
            exploredSet.add(node[1][-1])
            for child in stateSpaceGraph[node[1][-1]]:
                heappush(frontier, (node[0]+child[0]-h[node[1][-1]]+h[child[1]], node[1]+child[1]))
            print(list(frontier)); print(exploredSet); input()
inconsistent = {
    'S':[(1,'a'),(1,'b')],'a':[(1, 'c')], 'b':[(2, 'c')], 'c':[(3, 'G')], 'G':[]}
h = {'S':2,'a':4,'b':1,'c':1,'G':0}
print('Solution path:',aStarGsa(inconsistent, h, 'S', 'G'))






