# To reproduce our results:

1.  Install the dependencies in `requirements.txt`

3.  Put the graph instance files in the empty `data/` directory

2.  Run `scripts/results.py` in a **UNIX** shell. (You may encounter compatibility issues with the `interruptingcow` library if run in a Windows terminal window)

You may run it without arguments and have a default timeout on the exhaustive search of 5 seconds:
```
python results.py
```
Our results were produced with a timeout of 60.
To obtain results with a specific timeout, specify it as the first argument to the program as follows:
```
python results.py 60
```

Results will be saved in `graph_results.csv`, runtimes of each problem will be saved in `timing_results.csv`

