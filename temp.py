#graph constructor as adjacency lists
def grapher(file):
    f = open("data/" + file, "r").readlines()

    #number vertices, edges, reds
    n, m, r = map(int, f[0].strip().split())
    #start, end
    s, t = f[1].strip().split()
    
    #graph and red subset construction
    graph = dict()
    red = set()
    #vertices  (name or name *)  "not red / red"
    for node in f[2:n+2]:
        if node[-3:] == " *\n":
            node = node.strip("\n *")
            red.add(node)
            graph[node] = set()
        else:
            graph[node.strip()] = set()
    #edges  (u -- v or u -> v)  "undirected / directed"
    if f[n+2].split()[1] == "--":
        for edge in f[n+2:]:
            u, _, v = edge.split()
            graph[u].add(v)
            graph[v].add(u)
    else:
        for edge in f[n+2:]:
            u, _, v = edge.split()
            graph[u].add(v)
            
    return graph, [n, m, r], [s, t], red


#def noredgrapher(file):
        #problem None ignores red nodes
        #can implement as altered copy of grapher or alter grapher to take (file, nored)
#def graphermatrix(file):???
        #adjacency matrices are faster than adjacency lists for direct true/false edge-lookup, but not neighbor searches
        #probably not needed for any of the problems


from collections import deque
def bfs(graph, start, end):
    visited = set([start])
    queue = deque([[start, list()]])
    while queue:
        node, path = queue.popleft()
        if end not in graph[node]:
            for adj in graph[node]:
                if adj not in visited:
                    visited.add(adj)
                    queue.append([adj, path + [node]])
        else:
            return path + [node, end]
    return list()


def bfsalternating(graph, red, start, end):
    goal = end in red
    visited = set([start])
    queue = deque([[start, start in red]])
    while queue:
        node, state = queue.popleft()
        if state == goal or end not in graph[node]:
            for adj in graph[node]:
                if state != (adj in red) and adj not in visited:
                    visited.add(adj)
                    queue.append([adj, not state])
        else:
            return True
    return False


import os
for file in os.listdir("data"):
    print(file)
    graph, nmr, st, red = grapher(file)
    print(st[0], "-->", st[1])
    print(bfs(graph, st[0], st[1]))
    print(bfsalternating(graph, red, st[0], st[1]))
