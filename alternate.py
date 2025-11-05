from temp import bfs


def alternate(s: str, t: str, G: dict[str, set[str]], red: dict[str, bool]) -> bool:
    for node, neighbors in G.items():
        for neighbor in neighbors.copy():
            if (node in red) == (neighbor in red):
                G[node].remove(neighbor)
    return bool(bfs(G, s, t))
