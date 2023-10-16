#!/bin/bash
#bash script to run N queens on many inputs and store data in data.csv
#data.csv contains n=4 to 34 for numthreads 15 to 50
cd src
MAX_N=50
LOW_N=4
# dont change LOW_N
LOW_NUM_THREADS=41
MAX_NUM_THREADS=50

for (( N = $LOW_N; N <= $MAX_N; N++ ))
do

    for (( numThreads = $LOW_NUM_THREADS ; numThreads <= $MAX_NUM_THREADS; numThreads++ )) 
    do
        python3 main.py $N $numThreads
    done
done
cd .. 
