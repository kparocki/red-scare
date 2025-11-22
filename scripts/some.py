import os
from util.common import grapher
import networkx as nx
from many import many_nx
from few import few

def run_some(filename:str) -> bool | str:
    '''Runs Many, which includes a check if a graph is acyclic or not.
    If Many finds a path with maximum number of red node that contains at least one red node, some returns True.
    If Many doesn't find a path or the maximum is zero, some returns False.
    For graphs that are not acyclic, many returns None. In this case, the algorthm computes Few.
    If Few finds a path with a minimum number of red nodes and it contains at least one red node, some returns True.
    If Few doesn't find a path, Some returns False.
    Otherwise (if Few returns 0) the solution cannot be determined, and a message about NP-hardness is returned.'''

    G, _, (s, t), red = grapher(filename)

    many_out = many_nx(s, t, G, red)

    if many_out == None: #exhaustive search terminated early

        few_out = few(s,t,G,red)     
        if few_out == -1: return False
        elif few_out > 0: return True
        else: # when the result is 0
            return "the problem is NP hard, cannot determine"
        
    if many_out > 0: return True
    else: # when the result is < 0 
       return False

def main():

    files = os.listdir("../data")
    files.remove("README.md")

    for file in files:
        print(f"{file}: some = {run_some(file)}")   

if __name__ == "__main__":
    main()
