# N_Queens_AI
The local search used is parallel hill climbing with restarts after a certain number of iterations if the solution isn’t found. 

The basics of the algorithm I wrote are the following:
1. Start with a pretty good first guess. This means that the first guess should not have any queens in the same row or column (see getFirstListOfQueens(N) in Queen.py). It is possible that some queens have the same diagonals as others, which is okay. After all, the first guess cannot be perfect.

2. Look at the list of queens and check if there are errors by looking at every (pair) combination of queens. Build up a list of errors (including which pairs of queens threaten each other and what the error type is). The error to fix is chosen randomly (see queensMisplaced(queens) in main.py). If there is no error, return None. The current thread should add the queens list to a global variable of results (not before acquiring the lock of course). Then, the current thread should notify other threads that it found the solution (solution_found_event.set())

3. If there was an error, we must try to fix the error without creating too many others (ideally by decreasing the amount of errors instead of keeping it the same). This means that we need to analyze what possible options we have from here and pick the best one (see fixError() in main.py). If the error is that two queens are on the same row or col, that means that there exists at least one row or col that has no queens. Pick the row or col that minimizes the number of errors (see getBestChoice and numErrors(queens) in main.py). If the error is that two queens are on the same diagonal, pick a random location that would not increase the number of errors by more than 1. The reason why we shouldn’t pick a random location that keeps the errors the same is to try to avoid cycles. Additionally, sometimes making a worst choice can help fix the problem of being stuck at local optima.

4. Repeat steps 2 and 3 either until a solution is found or the max number of iterations is reached, in which case we should restart by calling getFirstListOfQueens to start with a good guess again. The reason for having a max amount of iterations is to prevent wasting time on an initial bad guess, cycle, or local optima (see worker_thread in main.py)


The program is run by executing the following command:
```bash
python3 main.py <N> <numThreads>
```



Here is a 3d graph plotting time in seconds as a function of N and numThreads (see collectData.sh, graphData.py and data.csv)

<img width="649" alt="Screenshot 2023-10-08 at 1 20 41 AM" src="https://github.com/vmic2002/N_Queens_AI/assets/89990471/3a7fb58b-23f7-416e-b48b-91c7c6684144">

The graph can be seen by running the following command:

```bash
python3 graphData.py
```


This program managed to solve N queens for the following N and numThreads: 

(The solution is described as an array where the index is the column and the value is the row)

N = 35  with 22 threads
[14, 2, 28, 16, 21, 11, 22, 26, 33, 12, 1, 15, 19, 0, 32, 30, 24, 3, 29, 13, 9, 6, 34, 25, 20, 17, 23, 27, 8, 10, 5, 7, 31, 4, 18]
367.6123378276825 seconds


N = 45 with 20 threads
[22, 26, 28, 32, 24, 33, 19, 44, 8, 36, 40, 30, 5, 7, 4, 31, 27, 12, 1, 18, 43, 3, 14, 37, 10, 6, 35, 39, 25, 20, 2, 11, 16, 21, 23, 9, 38, 15, 34, 0, 41, 17, 29, 13, 42]
1578.4577386379242 seconds


N = 50 with 24 threads
[5, 10, 42, 24, 15, 3, 31, 9, 45, 6, 36, 29, 44, 30, 17, 8, 49, 11, 34, 32, 21, 41, 13, 38, 2, 0, 48, 37, 40, 28, 19, 35, 16, 1, 26, 7, 43, 22, 20, 47, 23, 14, 12, 4, 39, 25, 46, 33, 27, 18]
1688.984313249588 seconds


N = 60 with 28 threads
[17, 55, 23, 30, 10, 47, 24, 44, 3, 59, 0, 2, 51, 37, 45, 31, 8, 58, 29, 41, 18, 28, 6, 42, 50, 11, 38, 7, 25, 52, 32, 14, 5, 9, 54, 34, 49, 4, 19, 43, 33, 56, 36, 15, 26, 16, 20, 1, 57, 27, 39, 21, 48, 53, 13, 40, 35, 22, 46, 12]
126.96703481674194 seconds


