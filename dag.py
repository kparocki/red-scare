Graph = dict[str, set[str]]

# Inspiration from https://www.geeksforgeeks.org/dsa/detect-cycle-in-a-graph/

def has_cycle(G: Graph) -> bool:
    visited = {v: False for v in G}
    stack: list[str] = []

    for v in G:
        if visited[v]:
            continue
        if dfs_is_cyclic(G, v, visited, stack):
            return True

    return False


def dfs_is_cyclic(G: Graph, v: str, visited: dict[str, bool], stack: list[str]) -> bool:
    if v in stack:
        return True
    if visited[v]:
        return False

    visited[v] = True
    stack.append(v)

    for neighbor in G[v]:
        if dfs_is_cyclic(G, neighbor, visited, stack):
            return True

    _ = stack.pop()
    return False


def main():
    cyclic_graph = {
        "1": {"2"},
        "2": {"3"},
        "3": {"1"},
    }

    acyclic_graph = {
        "1": {"2"},
        "2": {"3"},
        "3": {"4"},
        "4": {},
    }

    breakpoint()
    print(f"{cyclic_graph=} is {'cyclic' if has_cycle(cyclic_graph) else 'acyclic'}")
    print(f"{acyclic_graph=} is {'cyclic' if has_cycle(acyclic_graph) else 'acyclic'}")


if __name__ == "__main__":
    main()
