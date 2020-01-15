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
practice = {
    'S':['a','d','G'],'a':['b'],
    'd':['b','e'],'G':[],'b':['e','c'],
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
print('Solution path:',bfsTsa(practice, 'S', 'G'))


