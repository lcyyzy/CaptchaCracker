#!/bin/bash
par=20
prefix="./"
filename="cracker.py"
for (( i = 0; i < par; i++ )); do
	#statements
	runFile=${prefix}${i}'/'${filename}
	# ./test.py &
	${runFile} &
	# ./niggaRobber.py &
done
