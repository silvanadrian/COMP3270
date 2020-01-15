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
practice = {
    'S':[(3,'a'),(2,'d'),(10,'G')],'a':[(5,'b')],
    'd':[(1,'b'),(4,'e')],'G':[],'b':[(1,'e'),(2,'c')],
    'e':[(3,'G')],'c':[(4,'G')]}


quiz1_19 = {
    'A':[(1,'B'),(4,'C')],
    'B':[(1,'A'),(1,'C'),(5,'D')], 
    'C':[(4,'A'),(1,'B'),(3,'D')], 
    'D':[(5,'B'),(3,'C'),(8,'E'),(3,'F'),(9,'G')],
    'E':[(8,'D'),(2,'G')],
    'F':[(3,'D'),(5,'G')]
    }

h1 = {'A':9.5,'B':9,'C':8,'D':7,'E':1.5,'F':4,'G':0}
h2 = {'A':10,'B':12,'C':10,'D':8,'E':1,'F':4.5,'G':0}
# admissable consitent
h3 = {'A':10,'B':12,'C':10,'D':8,'E':1,'F':4.5,'G':0}


exam_14 = {
	'S': [(2,'A'),(3,'B')],
	'A':[(3,'C')],
    'B':[(1,'C'),(3,'D')], 
    'C':[(1,'D'),(3,'E')], 
    'D':[(2,'F')],
    'E':[(2,'G')],
    'F':[(1,'G')]
}

hexam = {'S':6,'A':4,'B':4,'C':4,'D':3.5,'E':1,'F':1,'G':0}

print('Solution path:',aStarGsa(exam_14, hexam, 'S', 'G'))






