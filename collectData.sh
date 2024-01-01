#!/bin/bash
#bash script to run N queens on many inputs and store data in data.csv
#data.csv contains n=4 to 34 for numthreads 15 to 55
#and n=4 to 37 for numThreads 56 to 60
#and n=4 to 36 for numThreads 61 to 66
#and n=4 to 34 for numThreads 67 to 75
#and n=4 to 38 for numThreads 76 to 80
#and n=4 to 38 for numThreads 81 to 85
#and n=4 to 38 for numThreads 86 to 90
cd src
MAX_N=38
LOW_N=4
# dont change LOW_N
LOW_NUM_THREADS=86
MAX_NUM_THREADS=90

for (( N = $LOW_N; N <= $MAX_N; N++ ))
do

    for (( numThreads = $LOW_NUM_THREADS ; numThreads <= $MAX_NUM_THREADS; numThreads++ )) 
    do
        python3 main.py $N $numThreads
    done
done
cd .. 
