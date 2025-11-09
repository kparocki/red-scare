import heapq

def djikstras(graph: dict[str, set[(int, str)]], start, end):
    """
    Takes a graph (directed or undirected) with weighted edges and uses Djikstras
    algorithm to find the shortest path from 'start' to 'end'.
    The graph is expected to be a dictionary with a node as the key and a set of outlink
    tuples with the name and weight for each outlink from the node.
    """
    # Create "min distance so far"
    dist_to = {start: 0} | {n : w for w, n in graph[start]}
    # Creat Min-Queue
    heap = list(graph[start])
    heapq.heapify(heap)

    while heap:
        # Get node with minimal dist
        w, node = heapq.heappop(heap)
        # Check if we have seen node before and new path is shorter
        if node in dist_to:
            if w < dist_to[node]: 
                # If shorter, update dist
                dist_to[node] = w
                # enqueue neighbors with accummulated path length only if
                # we have not reached end (only simple shortest paths!)
                if node != end:
                    for adj_w, adj_n in graph[node]:
                        # Increase "weight" of path by w+link_w
                        heapq.heappush(heap, (adj_w + w, adj_n))
        else:
            dist_to[node] = w

        
    if end in dist_to:
        return dist_to[end]
    else:
        return # -1 # No Path


def few(s: str, t: str, G: dict[str, set[str]], red: set[str]) -> bool:
    """
    Firstly constructs from the initial graph, a graph where entering a red node
    will have a cost of one and all other nodes remain at cost of 0 to enter.
    Subsequently applies Djikstras to find the shortest path and return the length
    of this path, which will directly correspond to the number of red nodes visited
    on the path with the fewest total number of red nodes.
    """
    # Linear in # of edges to do below transform
    G_weighted = { 
        k: set(
            (1, n) if n in red # following link to a red node = cost of 1
            else (0, n) # following link to any other node = cost of 0
            for n in adj # Iteration over each adjacent node of 'k'
        )
        for k, adj in G.items() # Iterating over each node and set of neighbors
    }
    r = djikstras(G_weighted, s, t)
    return r


def main():
    from temp import grapher
    import os

    files = os.listdir("data")
    files.remove("README.md")

    def run_few(filename):
        G, _, (s, t), red = grapher(filename)
        return few(s, t, G, red)

    for file in files:
        print(f"{file}: few = {run_few(file)}")


if __name__ == "__main__":
    main()