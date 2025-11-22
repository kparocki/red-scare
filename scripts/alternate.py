from util.common import bfs


def alternate(s: str, t: str, G: dict[str, set[str]], red: set[str]) -> bool:
    for node, neighbors in G.items():
        for neighbor in neighbors.copy():
            if (node in red) == (neighbor in red):
                G[node].remove(neighbor)
    return bool(bfs(G, s, t))


def main():
    from util.common import grapher
    import os

    files = os.listdir("../data")
    files.remove("README.md")

    def run_alternate(filename):
        G, _, (s, t), red = grapher(filename)
        return alternate(s, t, G, red)

    for file in files:
        print(f"{file}: alternate = {run_alternate(file)}")


if __name__ == "__main__":
    main()
