from few import few
from none import noredgrapher
from temp import bfs

def main_none(file):
    graph, (s, t) = noredgrapher(file)
    #finds shortest path and subtracts the end node (aka, becomes number of edges)
    path = bfs(graph, s, t)
    return len(path) - 1

def valid(few_res, none_res):
    if few_res == -1:
        return none_res == -1
    if none_res == -1:
        return few_res != 0
    return few_res == 0 and none_res >= 1

def main():
    from temp import grapher
    import os

    files = os.listdir("data")
    files.remove("README.md")

    def run_few(filename):
        G, _, (s, t), red = grapher(filename)
        return few(s, t, G, red), s, t, red

    for file in files:
        f_res, s, t, red = run_few(file)
        n_res = main_none(file)
        reds_in_st = int(s in red) + int(t in red)
        v = valid(f_res-reds_in_st, n_res)
        if not v:
            print(f"{file}: few = {f_res}; none = {n_res}; valid = {valid(f_res-reds_in_st, n_res)}")


if __name__ == "__main__":
    main()