from Queen import *
import sys
from itertools import combinations
import random
import threading
import time

# Shared data structure to store results
results = []
results_lock = threading.Lock()


# Create an event to signal when a solution is found
solution_found_event = threading.Event()

def sameRow(q1, q2):
    return q1.row == q2.row

def sameCol(q1, q2):
    return q1.col == q2.col

def sameDiagonal(q1, q2):
    return abs(q1.row-q2.row)==abs(q1.col-q2.col) 

def queensMisplaced(queens):
    #RETURNS indices of WHAT PAIR OF QUEENS THREATEN EACH OTHER AS WELL AS THE ERROR ITSELF
    #Returns None if there are no errors (at optimum!)
    #KEEP LIST OF ALL ERRORS AND RETURN ONE AT RANDOM TO NOT BE STUCK IN CYCLES
    pairsOfQueens = list(combinations(queens, 2))
    allErrors = []#list of 3-tuples containing all errors
    for (q1, q2) in pairsOfQueens:
        #print(str(q1)+" "+str(q2))    
        if sameRow(q1,q2):
            allErrors.append((queens.index(q1), queens.index(q2), QueenError.SAME_ROW))
        elif sameCol(q1,q2):
            allErrors.append((queens.index(q1), queens.index(q2), QueenError.SAME_COL))
        elif sameDiagonal(q1,q2):
            allErrors.append((queens.index(q1), queens.index(q2), QueenError.SAME_DIAGONAL))
    if not allErrors:
        #allErrors is empty
        return None
    #print("All errors: "+str(allErrors))
    return random.choice(allErrors)

def fixError(queens, q1Index, q2Index, err, numErrs):
    #hill climbing happens here, for same row and same col errors pick new row or col that minimized num errors
    #if same diagonal randomly replace q1 without worsening num errors by more than 1
    if err == QueenError.SAME_ROW:
        bestChoice = getBestChoice(queens, q1Index, err)        
        #bestChoice is row that would yield the least amount of errors
        queens[q1Index].row = bestChoice
    elif err == QueenError.SAME_COL:
        bestChoice = getBestChoice(queens, q1Index, err)
        #bestChoice is col that would yield the least amount of errors
        queens[q1Index].col = bestChoice
    else:# err == QueensError.SAME_DIAGONAL:
        #pick random location (as long as no other queen is there)
        #PICK RANDOM LOCATION THAT MINIMIZES NUMERRORS
        newNumErrs = numErrs+2
        badPositions = []#to not randomly choose positions that were already tried
        while(newNumErrs>numErrs+1):#allow for max 1 more error
            newRow, newCol = getNewPosition(queens)
            if not ((newRow, newCol) in badPositions):
                badPositions.append((newRow, newCol))
                queensCopy = queens.copy()
                queensCopy[q1Index].row = newRow
                queensCopy[q1Index].col = newCol
                newNumErrs = numErrors(queensCopy)
                #if queens[q1Index].row==newRow and queens[q1Index].col==newCol:
                #    newNumErrs = numErrs+1#don't want to select same point to avoid cycles
                #print("newRow "+str(newRow)+" newCol "+str(newCol))
                #print("numerrs: "+str(newNumErrs))
                #input("press enter")
        queens[q1Index].row = newRow
        queens[q1Index].col = newCol
        #print("final: newRow "+str(newRow)+" newCol "+str(newCol))
        
            
def getNewPosition(queens):
    #returns new r,c such that no queen is already positioned there
    newPairFound = False
    while not newPairFound:
        newPairFound = True
        newRow = random.randrange(len(queens))
        newCol = random.randrange(len(queens))
        for q in queens:
            if q.row == newRow and q.col == newCol:
                newPairFound = False
                break
    return newRow, newCol
          
   

def getBestChoice(queens, q1Index, err):
    #returns best choice (row or col) that minimizes num errors
    #get list of all rows/cols that dont have a queen
    available = [r for r in range(len(queens))] 
    for q in queens:
        if err == QueenError.SAME_ROW:
            x=q.row
        else:#err==QueenError.SAME_COL
            x=q.col
        if x in available:
            available.remove(x)
    #available cannot be empty since two queens are on the same row/col so there must be at least one empty row/col
    #print(err)
    #print("Available : "+str(available))
    errors = []#errors[i]=numErrors if available[i] is chosen for queens[q1Index]
    queensCopy = queens.copy()
    for r in available:
        if err == QueenError.SAME_ROW:
            queensCopy[q1Index].row = r
        else:#err==QueenError.SAME_COL
            queensCopy[q1Index].col = r
        errors.append(numErrors(queensCopy))
    #print("Errors list: "+str(errors))
    bestChoice = available[errors.index(min(errors))]
    #print("Best choice: "+str(bestChoice))
    return bestChoice

 
def numErrors(queens):
    pairsOfQueens = list(combinations(queens, 2))
    result=0
    for (q1, q2) in pairsOfQueens:
        #print(str(q1)+" "+str(q2))
        if sameRow(q1,q2) or sameCol(q1,q2) or sameDiagonal(q1,q2):
            result+=1
    return result


def printQueens(queens):
    #for q in queens:
    #    print(q)
    result=[None]*len(queens)
    for q in queens:
        result[q.col]=q.row
    #print(result)
    return result

# Define a function that represents the work each thread is doing
def worker_thread(thread_id, N):
    queens = getFirstListOfQueens(N)
    #printQueens(queens)
    numErrs = numErrors(queens)
    #print("num errors: "+str(numErrs))
    x = queensMisplaced(queens)

    i = 0
    maxIterations=50

    while not solution_found_event.is_set():# Check if a solution is found
        
        if x==None:
            with results_lock:
                #print(f"Thread {thread_id} found the solution!")
                results.append(queens)
            solution_found_event.set()  # Signal that a solution is found
            break
    
            

        i+=1
        # Your thread's work here...
        #print(f"Thread {thread_id} is working...")
        q1Index, q2Index, err = x
        #print(str(queens[q1Index]) + ", " + str(queens[q2Index]) + " -> " + str(err))
        fixError(queens, q1Index, q2Index, err, numErrs)
        #print("After fixing error:")
        #printQueens(queens)
        numErrs = numErrors(queens)
        #print("num errors: "+str(numErrs))
        x = queensMisplaced(queens)
        #input("Press enter...")
        #print("----------------")
        if i>=maxIterations and x!=None:
            queens = getFirstListOfQueens(N)#restart with new board
            i=0
            numErrs = numErrors(queens)
            x = queensMisplaced(queens)


            

#print("N Queens Problem!")
if len(sys.argv)!= 3:
    print("Wrong arguments...")
    exit(1)
try:
    N=int(sys.argv[1])
except:
    print("Must enter positive number >=4")
    exit(1)
if N<4:
    print("Must enter positive number >=4")
    exit(1)

try:
    numThreads=int(sys.argv[2])
except:
    print("Second argument must be an int (number of threads)")
    exit(1)
if numThreads<1:
    print("Second argument must be >=1 (number of threads)")
    exit(1)


start_time = time.time()

# Create and start multiple threads
threads = []
for i in range(numThreads):  # Create numThreads threads
    thread = threading.Thread(target=worker_thread, args=(i,N))
    threads.append(thread)
    thread.start()

# Wait for any thread to finish
for thread in threads:
    thread.join()

total_time = time.time() - start_time
#print("\tSolution found:")
sol=printQueens(results[0])
print(str(N)+" queens "+str(numThreads)+" numThreads Executed in "+str(total_time)+" seconds "+str(sol))

#if len(results)==1:
#    print("Solution found:")
#    printQueens(results[0])
#else:
#    print("Num solutions found: "+str(len(results)))
#    for queens in results:
#        i+=1
#        print("Solution "+str(i)+":")
#        printQueens(queens)
#print()
data=f"{round(total_time,5)},{N},{numThreads},\"{sol}\"\n"



# Append-adds at last
file1 = open("../data.csv", "a")  # append mode
file1.write(data)
file1.close()
