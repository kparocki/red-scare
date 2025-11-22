def bc(x):
    if x == "True":
        return True
    elif x == "False":
        return False
    else:
        return x
    
def ic(x):
    if x.isdigit():
        return int(x)
    elif x == "-1":
        return -1
    else:
        return x

def main():
    import pandas as pd
    results = pd.read_csv("../graph_results.csv", converters={
        "Some": bc,
        "Many": ic,
        "Alternate": bc
    })

    #results vs manual_vals
    manual = pd.read_csv("../../manual_validations.csv").drop(columns="Person")

    for _, row in manual.iterrows():
        file = row["File"]
        res = results[results["File"] == file].iloc[0]
        check = res == row
        if all(check):
            pass#print(file, "pass")
        else:
            print(file, "fail")
            for problem, b in check.items():
                if not b:
                    if res[problem] == "!?":
                        print(problem, "!?")
                        continue
                    print(problem, type(res[problem]), type(row[problem]))
                    print(res[problem], row[problem])
                    exit()

    #results vs brute
    from common import grapher
    from brute import allpaths
    import os
    #loops through all graphs
    for file in os.listdir("../../data"):
        if file == "README.md":
            continue
        graph, (n, m, r), (s, t), red = grapher(file)
        #above 50 it starts including grid graphs, which take forever
        if m <= 50:
            #number of red nodes in all possible paths
            paths = [len([1 for node in path if node in red]) for path in allpaths(graph, s, t)]
            #results for few, many, and some
            if paths:
                few = min(paths)
                many = max(paths)
                some = True if many > 0 else False
            else:
                few, many, some = -1, -1, False
            
            res = results[results["File"] == file].iloc[0]
            check = [res.iloc[4] == few, res.iloc[3] == many, res.iloc[2] == some]

            if all(check):
                pass#print(file, "pass")
            else:
                print(file, "fail")
                for i, c in enumerate(check):
                    if not c:
                        if i == 0:
                            print("Few", res.iloc[4], few)
                        elif i == 1:
                            print("Many", res.iloc[3], many)
                        else:
                            print("Some", res.iloc[2], some)
                exit()

if __name__ == "__main__":
    main()
