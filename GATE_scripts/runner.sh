#!/bin/bash

for p in $(seq 0 5 175)
do
	for i in {1..5}
	do
		startangle=$p
		endangle=$((p + 1))
		echo "$p $i $(date)" >>times
        	Gate -a [startangle,$startangle][endangle,$endangle] CTsimu.mac 2> /dev/null
        	echo "$p $i $(date)" >>times
	done
done

