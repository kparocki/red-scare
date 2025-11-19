# Our Ideas to Each Problem
*None*: (Daniel & Gaz) BFS to find shortest path in the graph where red nodes are removed (never remove and s, t)
*Few*: (Chris & Mie) Shortest path with weight 0 and 1 on edges in directed version (weight 1 to go into red node)
*Alternate*: (Gustav & Thomas) Make bipartite and BFS

*many*: longest path in acyclic graph
*some*: may be derived from many, some extra cases may by derived form non-zero answers to few

## Questions Meeting 1
- Do source and target being red matter in which problems?
    - In *None* the color of s & t is not considered, in all other problem the color of s & t matters, i.e. if s is a red node it will count as a red node on the s,t-path.
- None, our solution to makes sense
- Alternate, our solution is on the right track
- Few, our solution is on the right track
- Our input makes sense so far :D
- Report is very short with explanations on 5-8 lines per problem - results should be a snippet of the full results (full results should follow a sensible format the is understandable - CSV of results makes sense)
- our idea for many does make sense - we should be able to reason about what kind of graphs makes sense -> acyclic does make sense, are there other types of instances (should not be the focus this week though!)
- TAs will validate putting in "enough effort" -> current effort is fine, goal is to apply what we learned so far in the course. We just need to make a reasonable attempt and make reasonable arguments for choices etc. Would like to see attempt of NP-Hardness reduction (we can do this together all of us, would be fun!)!
- We seem on the right track

## Questions Meeting 2
- we recognize that many is a "longest path problem" -> is this what we are supposed to do a reduction on? What detail do we need to give to make this reduction?
    - many and longest path is a valid reduction - it can be many different NP Hard problems, we should follow the template and be good-to-go!
- should we be able to solve more than the acyclic cases for many in a "smart way"?
    - acyclic part is good - **remember cyclic when cycles are purely black is not a problem for the algorithm.**

- for some, we are thinking to use many in all acyclic cases and infer some extra cases using few (i.e. cases where no path exists or where the path with minimum amount of red vertices is >0) - does this make sense? are there other cases we should consider?
    - this makes sense - we will just describe in the report how we use X and Y to solve Z in this way - it is also still good to mention kinds of graphs that we can find solutions.

- take some of the smaller examples and do by hand, and reason about the correct solution, compare to output of the code. (5-6 different types) - we do not need extensive testing, but we should be able to write some assumptions based on validations done by hand.

- Remember README with description of how to recreate results.txt

## Questions Meeting 3
- What is a reasonable timeout for exhaustive search?
  - more than 5 seconds (maybe 10-15 seconds, maybe a minute or three?)
- Are there more cases than "graphs without negative cycles" that we can solve smartly for Many?
  - Give extra algorithms a shot if we have time
- Is it okay to hand in a link to cloneable github repo? or do you want a zipped folder in the handin?
  - Just a link to the github repo or zip - both are fine (also depends on how the submission is set up!) - no specific, just needs to be accessible
- Do you want empirical time measurements on all problems (as suggested by the template) or is the time complexity enough?
  - Yes!


# Plan
- Write up NP-Hardness proof for many
- Write report