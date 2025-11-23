#### To reproduce our results:

1.  Install the dependencies in `requirements.txt`


2.  Run `results.py` in the scripts directory in a **UNIX** shell. (You may encounter compatibility issues with the interruptingcow library if run in a Windows terminal window)

You may run it without arguments and have a default timeout on the exhaustive search of 5 seconds:
```
python results.py
```
Or pass the number of seconds you wish to run the search of a single graph before terminating exhaustive search:
```
python results.py 15
```


3.  Results will be returned in `graph_results.csv`

