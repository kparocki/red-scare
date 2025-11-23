from common import grapher


from collections import deque
#Brute-force searching all possible paths
def allpaths(graph, start, end):
    paths = list()
    queue = deque([[start, list(), set([start])]])
    while queue:
        node, path, visited = queue.popleft()
        #returns path if end node is a neighbor of current node
        for adj in graph[node]:
            if adj != end:
                if adj not in visited:
                    queue.append([adj, path + [node], visited.union({adj})])
            else:
                paths.append(path + [node, end])
    return paths


def main():
    import os
    #loops through all graphs
    for file in os.listdir("../../data"):
        if file == "README.md":
            continue
        graph, (n, m, r), (s, t), red = grapher(file)
        #above 50 it starts including grid graphs, which take forever
        if m <= 50:
            print(file)
            #number of red nodes in all possible paths
            paths = [len([1 for node in path if node in red]) for path in allpaths(graph, s, t)]
            #results for few, many, and some
            if paths:
                few = min(paths)
                many = max(paths)
                some = True if many > 0 else False
            else:
                few, many, some = -1, -1, False
            print(few, many, some)


if __name__ == "__main__":
    main()
