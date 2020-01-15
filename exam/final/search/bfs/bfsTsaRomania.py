import collections
def bfsTsa(stateSpaceGraph, startState, goalState): 
    frontier = collections.deque([startState])
    print('Initial frontier:',list(frontier))
    input()
    while frontier: 
        node = frontier.popleft()
        if (node.endswith(goalState)): return node
        print('Exploring:',node[-1],'...')
        for child in stateSpaceGraph[node[-1]]: frontier.append(node+child)
        print(list(frontier))
        input()
romania = {
    'A':['S','T','Z'],'Z':['A','O'],'O':['S','Z'],
    'T':['A','L'],'L':['M','T'],'M':['D','L'],
    'D':['C','M'],'S':['A','F','O','R'],
    'R':['C','P','S'],'C':['D','P','R'],
    'F':['B','S'],'P':['B','C','R'],'B':[]
    }
print('Solution path:',bfsTsa(romania, 'A', 'B'))



