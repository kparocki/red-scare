from util.common import djikstras, grapher
import os

def few(s: str, t: str, G: dict[str, set[str]], red: set[str]) -> bool:
    """
    Firstly constructs from the initial graph, a graph where entering a red node
    will have a cost of one and all other nodes remain at cost of 0 to enter.
    Subsequently applies Djikstras to find the shortest path and return the length
    of this path, which will directly correspond to the number of red nodes visited
    on the path with the fewest total number of red nodes.
    """
    G_weighted = { 
        k: set(
            (1, n) if n in red # following link to a red node = cost of 1
            else (0, n) # following link to any other node = cost of 0
            for n in adj # Iteration over each adjacent node of 'k'
        )
        for k, adj in G.items() # Iterating over each node and set of neighbors
    }
    r = djikstras(G_weighted, s, t)

    if r is None:
        return -1
    else:
        return r + int(s in red)


def main():
    files = os.listdir("../data")
    files.remove("README.md")

    def run_few(filename):
        G, _, (s, t), red = grapher(filename)
        return few(s, t, G, red)

    for file in files:
        print(f"{file}: few = {run_few(file)}")


if __name__ == "__main__":
    main()