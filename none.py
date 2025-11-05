from temp import bfs


#graph constructor as adjacency lists
def noredgrapher(file):
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
        else:
            graph[node.strip()] = set()
    red.discard(s)
    red.discard(t)
    graph[s] = set()
    graph[t] = set()
    #edges  (u -- v or u -> v)  "undirected / directed"
    if m > 0 and f[n+2].split()[1] == "--":
        for edge in f[n+2:]:
            u, _, v = edge.split()
            if u not in red and v not in red:
                graph[u].add(v)
                graph[v].add(u)
    else:
        for edge in f[n+2:]:
            u, _, v = edge.split()
            if u not in red and v not in red:
                graph[u].add(v)
            
    return graph, (s, t)


def main():
    import os
    #loops through all graphs
    for file in os.listdir("data"):
        if file == "README.md":
            continue
        print(file)
        graph, (s, t) = noredgrapher(file)
        #finds shortest path and subtracts the end node (aka, becomes number of edges)
        path = bfs(graph, s, t)
        print(len(path) - 1)
        #checks path is consistent with edges in adjacency list
        #print(path)
        #for i, node in enumerate(path[:-1]):
            #if path[i+1] not in graph[node]:
                #print("Error")
                #print(node[i+1], "not in", graph[node])
                #exit()


if __name__ == "__main__":
    main()
