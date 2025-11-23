import os
import csv

import networkx as nx
from interruptingcow import timeout

from util.common import grapher, bfs, djikstras
from none import noredgrapher
from few import few
from alternate import alternate
from many import many_nx, many_sp, many_exhaustive

def main():
    
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

    files = [n for n in os.listdir("../data") if n != "README.md"]
    files.sort() # To run in consistent order
    # Loops through all graphs
    for file in files:
        current_results = {
            "File": file,
            "None": None, 
            "Some": None, 
            "Many": None, 
            "Few": None, 
            "Alternate": None
        }
        print(file)

        # Initialises full graph
        G, _, _, red = grapher(file, data_path="../data/")
        
        #### None ####
        graph_no_reds, (s, t) = noredgrapher(file)
        path = bfs(graph_no_reds, s, t)
        current_results["None"] = len(path) - 1
    
        #### Many ####
        res = many_nx(s, t, G, red)
        current_results["Many"] = "!?" if res == None else res
    
        #### Few ####
        current_results["Few"] = few(s, t, G, red)

        #### Alternate ####
        current_results["Alternate"] = alternate(s, t, G, red)

        #### Some ####
        if current_results["Many"] != "!?":
            current_results["Some"] = True if current_results["Many"] > 0 else False
        elif current_results["Few"] > 0: 
            current_results["Some"] = True
        else:
            current_results["Some"] = "!?"
        
        # Collect graph data for all algos
        all_results.append(current_results)

    # Create the csv file and write results
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        writer.writeheader()
    
        writer.writerows(all_results)

if __name__ == "__main__":
    main()
