#!/bin/bash

# Occasionally, when running all the levels Pygame would freeze if quiet=False. 
# Do avoid this (or to run a specific set of levels) you can 
# use a script to run each level in a loop

duration=4

for x in `seq 10 819`; do 
    #Run level $x
    #Collect the output in a variable
    python3 duck_hunt_main.py -d $duration -l $x

    #Get error code
    rc=$?; 
    if [ $rc -ne 0 ]; then
        echo "Return with an error for level $x, exit"
        break
    fi
done
