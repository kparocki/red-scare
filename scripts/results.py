import os
import csv

import networkx as nx
from interruptingcow import timeout

from util.common import grapher, bfs, djikstras
from none import noredgrapher
from few import few
from alternate import alternate
from many import many_nx, many_sp, many_exhaustive
import sys

import time

def main():
    # Take argument as timeout if given, otherwise default to 5 second timeout on exhaustive search
    timeout_sec = int(sys.argv[1]) if len(sys.argv) > 1 else 5

    output_csv_file = "graph_results.csv"
    
    # List to hold the data for the CSV file
    all_results = []

    # Final column header format
    header = [
        "File", 
        "None", 
        "Some", 
        "Many", 
        "Few", 
        "Alternate"
    ]


    output_timings_file = "timing_results.csv"

    timing_results = []
    timing_header = [
        "File", 
        "None", 
        "Some", 
        "Many", 
        "Few", 
        "Alternate"
    ]

    files = [n for n in os.listdir("../data") if n != "README.md"]
    files.sort() # To run in consistent order

    # Loops through all graphs
    for file in files:
        print(file)
        current_results = {
            "File": file,
            "None": None, 
            "Some": None, 
            "Many": None, 
            "Few": None, 
            "Alternate": None
        }
        current_timings = {
            "File": file,
            "None": None, 
            "Some": None, 
            "Many": None, 
            "Few": None, 
            "Alternate": None
        }

        # Initialises full graph
        G, _, _, red = grapher(file, data_path="../data/")
        
        #### None ####
        graph_no_reds, (s, t) = noredgrapher(file)
        start = time.perf_counter()

        path = bfs(graph_no_reds, s, t)
        current_results["None"] = len(path) - 1

        end = time.perf_counter()
        current_timings["None"] = end - start
    
        #### Many ####
        start = time.perf_counter()

        res = many_nx(s, t, G, red, timeout_sec)
        current_results["Many"] = "!?" if res == None else res

        end = time.perf_counter()
        current_timings["Many"] = end - start
    
        #### Few ####
        start = time.perf_counter()

        current_results["Few"] = few(s, t, G, red)

        end = time.perf_counter()
        current_timings["Few"] = end - start

        #### Alternate ####
        start = time.perf_counter()

        current_results["Alternate"] = alternate(s, t, G, red)

        end = time.perf_counter()
        current_timings["Alternate"] = end - start

        #### Some ####
        start = time.perf_counter()

        if current_results["Many"] != "!?":
            current_results["Some"] = True if current_results["Many"] > 0 else False
        elif current_results["Few"] > 0: 
            current_results["Some"] = True
        else:
            current_results["Some"] = "!?"
        
        end = time.perf_counter()
        current_timings["Some"] = end - start

        # Collect graph data for all algos
        all_results.append(current_results)
        timing_results.append(current_timings)

    # Create the csv file and write results
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        writer.writeheader()
    
        writer.writerows(all_results)

    # Create the timings file and write results
    with open(output_timings_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=timing_header)
        
        writer.writeheader()
        
        writer.writerows(timing_results)

if __name__ == "__main__":
    main()
