import collections
def dfsGsa(stateSpaceGraph, startState, goalState): 
    frontier = collections.deque([startState])
    exploredSet = set()
    print('Initial frontier:',list(frontier))
    input()
    while frontier: 
        node = frontier.pop()
        if (node.endswith(goalState)): return node
        if node[-1] not in exploredSet:
            print('Exploring:',node[-1],'...')
            exploredSet.add(node[-1])
            for child in stateSpaceGraph[node[-1]]: frontier.append(node+child)
            print(list(frontier))
            print(exploredSet)
            input()
practice = {
    'S':['a','d','G'],'a':['b'], 'd':['b','e'],'G':[],'b':['e','c'],
    'e':['G'],'c':['G']}

quiz1 = {
    'S': ['a', 'c', 'd'],
    'a' : ['e'],
    'c' : ['e'],
    'd' : ['e', 'G'],
    'e' : ['f'],
    'f' : ['b', 'd'],
    'b' : ['e', 'G']
}
print('Solution path:',dfsGsa(quiz1, 'S', 'G'))






