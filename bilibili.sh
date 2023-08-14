#!/bin/bash
while IFS= read -r line; do
    python3 bilibili.py $line >> ./data/$line.txt
    echo "date,follower" > ./data/$line.csv
    tac ./data/$line.txt >> ./data/$line.csv
done < uid.txt
