# N_Queens_AI
The local search used is parallel hill climbing with restarts after a certain number of iterations if the solution isn’t found. 

The basics of the algorithm I wrote are the following:
1. Start with a pretty good first guess. This means that the first guess should not have any queens in the same row or column (see getFirstListOfQueens(N) in Queen.py). It is possible that some queens have the same diagonals as others, which is okay. After all, the first guess cannot be perfect.

2. Look at the list of queens and check if there are errors by looking at every (pair) combination of queens. Build up a list of errors (including which pairs of queens threaten each other and what the error type is). The error to fix is chosen randomly (see queensMisplaced(queens) in main.py). If there is no error, return None. The current thread should add the queens list to a global variable of results (not before acquiring the lock of course). Then, the current thread should notify other threads that it found the solution (solution_found_event.set())

3. If there was an error, we must try to fix the error without creating too many others (ideally by decreasing the amount of errors). This means that we need to analyze what possible options we have from here and pick the best one (see fixError() in main.py). If the error is that two queens are on the same row or col, that means that there exists at least one row or col that has no queens. Pick the row or col that minimizes the number of errors (see getBestChoice and numErrors(queens) in main.py). If the error is that two queens are on the same diagonal, pick a random location that would not increase the number of errors by more than 1. The reason why we shouldn’t pick a random location that keeps the errors the same is to try to avoid cycles.

4. Repeat steps 2 and 3 either until a solution is found or the max number of iterations is reached, in which case we should restart by calling getFirstListOfQueens to start with a good guess again. The reason for having a max amount of iterations is to prevent wasting time on an initial bad guess, cycle, or local optima (see worker_thread in main.py)

The program is run by executing the following command:
```bash
python3 main.py <N> <numThreads>
```
This program managed to solve N queens for N=24 in 72.66055011749268 seconds.

The solution is described as an array where the index is the column and the value is the row:

[11, 21, 3, 16, 8, 10, 4, 2, 23, 12, 22, 17, 6, 20, 13, 1, 9, 19, 5, 15, 0, 18, 7, 14]
