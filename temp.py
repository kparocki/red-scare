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
    if m > 0 and f[n+2].split()[1] == "--":
        for edge in f[n+2:]:
            u, _, v = edge.split()
            graph[u].add(v)
            graph[v].add(u)
    else:
        for edge in f[n+2:]:
            u, _, v = edge.split()
            graph[u].add(v)
            
    return graph, (n, m, r), (s, t), red


#def noredgrapher(file):
        #problem None ignores red nodes
        #can implement as altered copy of grapher or alter grapher to take (file, nored)
#def graphermatrix(file):???
        #adjacency matrices are faster than adjacency lists for direct true/false edge-lookup, but not neighbor searches
        #probably not needed for any of the problems


from collections import deque
#BFS returning path
def bfs(graph, start, end):
    visited = set([start])
    queue = deque([[start, list()]])
    while queue:
        node, path = queue.popleft()
        #returns path if end node is a neighbor of current node
        if end not in graph[node]:
            for adj in graph[node]:
                if adj not in visited:
                    visited.add(adj)
                    queue.append([adj, path + [node]])
        else:
            return path + [node, end]
    return list()

#Alternate problem solution
def bfsalternating(graph, red, start, end):
    goal = end in red
    visited = set([start])
    queue = deque([[start, start in red]])
    while queue:
        node, state = queue.popleft()
        #only returns true if the end node is a neighboring node and the current node is the correct color
        if state == goal or end not in graph[node]:
            for adj in graph[node]:
                #only visits neighbors if they're the opposite color of the current node
                if state != (adj in red) and adj not in visited:
                    visited.add(adj)
                    queue.append([adj, not state])
        else:
            return True
    return False

def djikstras(graph: dict[str, set[(int, str)]], start, end):
    """
    Takes a graph (directed or undirected) with weighted edges and uses Djikstras
    algorithm to find the shortest path from 'start' to 'end'.
    The graph is expected to be a dictionary with a node as the key and a set of outlink
    tuples with the name and weight for each outlink from the node.

    Returns the length of the shortest path
    """
    import heapq
    # Create "min distance so far"
    dist_to = {start: 0}
    # Creat Min-Queue
    heap = list(graph[start])
    heapq.heapify(heap)

    while heap:
        # Get node with minimal dist
        w, node = heapq.heappop(heap)
        # Check if we have seen node before and new path is shorter
        if (node in dist_to and w < dist_to[node]) or node not in dist_to: 
                # If shorter, update dist
                dist_to[node] = w
                # enqueue neighbors with accummulated path length only if
                # we have not reached end (only simple shortest paths!)
                if node != end:
                    for adj_w, adj_n in graph[node]:
                        # Increase "weight" of path by w+link_w
                        heapq.heappush(heap, (adj_w + w, adj_n))

    if end in dist_to:
        return dist_to[end]
    else:
        return -1 # No Path

def main():
    import os
    #loops through all graphs
    for file in os.listdir("data"):
        if file == "README.md":
            continue
        print(file)
        graph, nmr, st, red = grapher(file)
        print(st[0], "-->", st[1])
        print(bfs(graph, st[0], st[1]))
        print(bfsalternating(graph, red, st[0], st[1]))


if __name__ == "__main__":
    main()
