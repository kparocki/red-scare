import networkx as nx
from interruptingcow import timeout

from common import djikstras, grapher
from dag import has_cycle
import os


def many_nx(s: str, t: str, adj_list: dict[str, set[str]], red: set[str]) -> int | None:
    """Finds the path from s to t with the most red nodes.
    Returns the number of red nodes on the path.
    If no path exists, returns -1.
    Runs Bellman-Ford if the graph has no negative cycles, otherwise exhaustive search.
    If the exhaustive search is terminated early, the function returns None."""
    G = nx.DiGraph()
    for v, neighbors in adj_list.items():
        G.add_node(v)
        for n in neighbors:
            G.add_edge(v, n, weight=-1 if n in red else 0)
    try:
        return -nx.shortest_path_length(
            G, s, t, method="bellman-ford", weight="weight"
        ) + int(s in red)
    except nx.NetworkXUnbounded:  # Negative cycle detected
        return many_exhaustive(s, t, G, red)
    except nx.NetworkXNoPath:
        return -1


def many_sp(s: str, t: str, G: dict[str, set[str]], red: set[str]) -> int:
    """
    Firstly constructs from the initial graph, a graph where entering a red node
    will have a cost of negative one and all other nodes remain at cost of 0 to enter.
    Subsequently applies Djikstras to find the shortest path and return the positive length
    of this path, which will directly correspond to the number of red nodes visited
    on the path with the largest total number of red nodes.
    """
    G_weighted = {
        k: set(
            (-1, n)
            if n in red  # following link to a red node = cost of 1
            else (0, n)  # following link to any other node = cost of 0
            for n in adj  # Iteration over each adjacent node of 'k'
        )
        for k, adj in G.items()  # Iterating over each node and set of neighbors
    }
    r = djikstras(G_weighted, s, t)

    if r:
        return -r + (int(s in red))
    else:
        return -1


def many_exhaustive(s: str, t: str, G: nx.DiGraph, red: set[str]) -> int | None:
    try:
        with timeout(5):
            paths = list(nx.all_simple_paths(G, source=s, target=t))
            if paths:
                return max(sum(1 for v in path if v in red) for path in paths)
            return -1
    except RuntimeError:
        return None


def main():
    files = os.listdir("../data")
    files.remove("README.md")

    def run_many(filename):
        G, _, (s, t), red = grapher(filename)
        return many_nx(s, t, G, red)

    for file in files:
        print(f"{file}: many = {run_many(file)}")


if __name__ == "__main__":
    main()
