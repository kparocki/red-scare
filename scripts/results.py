import networkx as nx
from interruptingcow import timeout

#graph constructor as adjacency lists
def grapher(file):
    f = open("../data/" + file, "r").readlines()

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
            graph[node] = set()
        else:
            graph[node.strip()] = set()
    #edges  (u -- v or u -> v)  "undirected / directed"
    if m > 0:
        if f[n+2].split()[1] == "--":
            for edge in f[n+2:]:
                u, _, v = edge.split()
                graph[u].add(v)
                graph[v].add(u)
        else:
            for edge in f[n+2:]:
                u, _, v = edge.split()
                graph[u].add(v)
            
    return graph, (n, m, r), (s, t), red


from collections import deque
#BFS returning path
def bfs(graph, start, end):
    visited = set([start])
    queue = deque([[start, list()]])
    while queue:
        node, path = queue.popleft()
        #returns path if end node is a neighbor of current node
        if end not in graph[node]:
            for adj in graph[node]:
                if adj not in visited:
                    visited.add(adj)
                    queue.append([adj, path + [node]])
        else:
            return path + [node, end]
    return list()

#Alternate problem solution
def bfsalternating(graph, red, start, end):
    goal = end in red
    visited = set([start])
    queue = deque([[start, start in red]])
    while queue:
        node, state = queue.popleft()
        #only returns true if the end node is a neighboring node and the current node is the correct color
        if state == goal or end not in graph[node]:
            for adj in graph[node]:
                #only visits neighbors if they're the opposite color of the current node
                if state != (adj in red) and adj not in visited:
                    visited.add(adj)
                    queue.append([adj, not state])
        else:
            return True
    return False

def djikstras(graph: dict[str, set[(int, str)]], start, end):
    """
    Takes a graph (directed or undirected) with weighted edges and uses Djikstras
    algorithm to find the shortest path from 'start' to 'end'.
    The graph is expected to be a dictionary with a node as the key and a set of outlink
    tuples with the name and weight for each outlink from the node.

    Returns the length of the shortest path
    """
    import heapq
    # Create "min distance so far"
    dist_to = {start: 0}
    # Creat Min-Queue
    heap = list(graph[start])
    heapq.heapify(heap)

    while heap:
        # Get node with minimal dist
        w, node = heapq.heappop(heap)
        # Check if we have seen node before and new path is shorter
        if (node in dist_to and w < dist_to[node]) or node not in dist_to: 
                # If shorter, update dist
                dist_to[node] = w
                # enqueue neighbors with accummulated path length only if
                # we have not reached end (only simple shortest paths!)
                if node != end:
                    for adj_w, adj_n in graph[node]:
                        # Increase "weight" of path by w+link_w
                        heapq.heappush(heap, (adj_w + w, adj_n))

    if end in dist_to:
        return dist_to[end]
    else:
        return None # No Path


####### None ########
#graph constructor as adjacency lists ignoring red nodes
def noredgrapher(file):
    f = open("../data/" + file, "r").readlines()

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
    if m > 0:
        if f[n+2].split()[1] == "--":
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

####### Few ########
import sys
import multiprocessing
import time
from typing import Callable, Any, Generator

# --- 1. Windows Compatible Timeout Context Manager ---

class windows_compatible_timeout:
    """
    A context manager to run a function in a separate process with a timeout.
    This works on Windows by using process termination.
    It can only return the result if the function finishes successfully.
    """
    def __init__(self, seconds: int, target: Callable, args: tuple):
        self.seconds = seconds
        self.target = target
        self.args = args
        self.result_queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(
            target=self._run_target, 
            args=(self.result_queue,) + self.args
        )

    def _run_target(self, result_queue, *args):
        """Wrapper to run the target function and put its result into the queue."""
        try:
            result = self.target(*args)
            result_queue.put(result)
        except Exception as e:
            # Put the exception into the queue so the main process can catch it
            result_queue.put(e)

    def __enter__(self):
        self.process.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.join(timeout=self.seconds)
        
        if self.process.is_alive():
            # If the process is still alive after the timeout, terminate it
            self.process.terminate()
            self.process.join() # Clean up the terminated process
            
            # Raise the exception that the original 'interruptingcow' caught
            raise RuntimeError("Timeout exceeded (5 seconds).")
        
        # If the process finished normally, retrieve the result or exception
        if not self.result_queue.empty():
            retrieved_item = self.result_queue.get()
            if isinstance(retrieved_item, Exception):
                raise retrieved_item # Re-raise any exception from the child process
            # Store the result so the caller can access it (though not strictly needed here)
            self.result = retrieved_item
            
        return False # Do not suppress any exceptions (like NetworkXNoPath)


# Conditional definition of the 'timeout' utility
if sys.platform != 'win32':
    # On POSIX systems, stick to the original signal-based timeout for simplicity
    from interruptingcow import timeout
else:
    # On Windows, define the context manager used in many_exhaustive
    # to be a function that returns the multiprocessing wrapper
    def timeout(seconds):
        """Dummy function to match the original call signature, returns the process wrapper."""
        def decorator(func):
            return windows_compatible_timeout(seconds, func, tuple())
        return decorator

# --- 2. Redefine many_exhaustive to work with the new context ---
# This requires slight restructuring to run the code *inside* the context manager 
# as the 'target' of the multiprocessing process.

def _exhaustive_search_worker(s: str, t: str, G: nx.DiGraph, red: set[str]) -> int | None:
    """The actual logic to be run inside the separate process."""
    paths = list(nx.all_simple_paths(G, source=s, target=t))
    if paths:
        # Calculate the maximum number of red nodes in any simple path
        return max(sum(1 for v in path if v in red) for path in paths)
    return -1


def many_exhaustive(s: str, t: str, G: nx.DiGraph, red: set[str]) -> int | None:
    try:
        # The 'timeout' function/context manager setup is now more complex 
        # due to the multiprocessing requirement. We must pass the target function
        # and its arguments to the context manager setup.
        
        # Since the original used 'with timeout(5): paths = ...', we need to adapt.
        # The simplest way is to directly instantiate and call the context manager
        # if the code is running on Windows.
        if sys.platform == 'win32':
            # Setup the multiprocessing context
            timer = windows_compatible_timeout(5, _exhaustive_search_worker, (s, t, G, red))
            
            with timer:
                # The execution happens in the process, not here.
                # We wait for the result or exception in the __exit__ method.
                pass
            
            # If the timer completes without a TimeoutError, return the result
            return timer.result 
        
        # Original POSIX code using interruptingcow
        else:
            with timeout(5):
                return _exhaustive_search_worker(s, t, G, red)
            
    except RuntimeError:
        # This catches the TimeoutError re-raised by the context manager on either system
        return None

# --- 3. Original Functions (Unchanged but needed for context) ---

# NOTE: The helper function 'djikstras' is still undefined and required for 'many_sp'.
# We also assume 'adj_list' comes from a grapher function not shown here.

# The other functions remain as they were, assuming all necessary imports (like nx) are at the top.

def many_nx(s: str, t: str, adj_list: dict[str, set[str]], red: set[str]) -> int | None:
    """Finds the path from s to t with the most red nodes.
    ... (docstring truncated) ..."""
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

####### Few ########
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

###### Few ######

def alternate(s: str, t: str, G: dict[str, set[str]], red: set[str]) -> bool:
    for node, neighbors in G.items():
        for neighbor in neighbors.copy():
            if (node in red) == (neighbor in red):
                G[node].remove(neighbor)
    return bool(bfs(G, s, t))

Graph = dict[str, set[str]]
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
    import os
    import csv


    output_csv_file = "graph_results.csv"
    
    # List to hold the data for the CSV file
    all_results = []

    header = [
        "File", 
        "None", 
        "Some", 
        "Many", 
        "Few", 
        "Alternate"
    ]
    # Loops through all graphs
    for file in os.listdir("../data"):
        if file == "README.md":
            continue
        current_results = {
            "File": file,
            "None": None, 
            "Some": None, 
            "Many": None, 
            "Few": None, 
            "Alternate": None
        }
        print(file)
        G, nmr, st, red = grapher(file)
        
        #### None ####
        graph, (s, t) = noredgrapher(file)
        path = bfs(graph, s, t)
        current_results["None"] = len(path) - 1
    
        #### Some ####
        current_results["Some"] = "wip"
        #### Many ####
        current_results["Many"] = many_nx(s, t, G, red)
    

        #### Few ####
        current_results["Few"] = few(s, t, G, red)

        #### Alternate ####
        current_results["Alternate"] = alternate(s, t, G, red)

        # Collect data 
        all_results.append(current_results)

    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # Write the header row
        writer.writeheader()
        
        # Write all the data rows
        writer.writerows(all_results)
if __name__ == "__main__":
    main()
